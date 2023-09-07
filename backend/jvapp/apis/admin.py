import json
import logging

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import ERROR_MESSAGES_KEY, JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response, \
    get_success_response
from jvapp.apis.ats import get_ats_api
from jvapp.apis.employer import EmployerSubscriptionView, EmployerView
from jvapp.apis.job_seeker import ApplicationView
from jvapp.apis.user import UserView
from jvapp.management.commands.ats_data_pull import save_ats_data
from jvapp.models.employer import Employer, EmployerAts, EmployerAuthGroup, EmployerJob, EmployerSubscription
from jvapp.models.user import JobVyneUser, UserConnection, UserEmployerPermissionGroup
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.permissions.general import IsAdmin
from jvapp.serializers.job_seeker import base_application_serializer
from jvapp.serializers.user import get_serialized_user
from jvapp.tasks import task_run_job_scrapers
from jvapp.utils.data import AttributeCfg, coerce_bool, set_object_attributes
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.taxonomy import get_standardized_job_taxonomy, run_job_title_standardization, update_taxonomies
from scrape.custom_scraper.workableAts import parse_workable_xml_jobs
from scrape.scraper import run_job_scrapers


logger = logging.getLogger(__name__)


class AdminAtsFailureView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        failed_applications = self.get_failed_applications()
        
        return Response(status=status.HTTP_200_OK, data=[self.get_serialized_application(app) for app in failed_applications])
    
    def post(self, request):
        failed_applications = self.get_failed_applications()
        ats_cfgs = {
            ats_cfg.employer_id: ats_cfg for ats_cfg in EmployerAts.objects.all()
        }
        app_save_count = 0
        for app in failed_applications:
            if not app.employer_job.ats_job_key:
                continue
            ats_cfg = ats_cfgs.get(app.employer_job.employer_id)
            ats_api = get_ats_api(ats_cfg)
            try:
                applicant = JobVyneUser.objects.get(email=app.email)
            except JobVyneUser.DoesNotExist:
                applicant = None
            is_success = ApplicationView.save_application_to_ats(ats_api, applicant, app)
            
            if is_success:
                app.notification_ats_failure_dt = None
                app.notification_ats_failure_msg = None
                app.save()
            else:  # Stop trying to push applications if the connection is still failing
                break
            
            app_save_count += 1
            
        data = {}
        if app_save_count:
            data[SUCCESS_MESSAGE_KEY] = f'Successfully pushed {app_save_count} applications'
        
        app_unsave_count = len(failed_applications) - app_save_count
        if app_unsave_count:
            data[ERROR_MESSAGES_KEY] = [f'Failed to push {app_unsave_count} applications']
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def get_failed_applications(self):
        return ApplicationView.get_applications(
            self.user, application_filter=Q(notification_ats_failure_dt__isnull=False), is_ignore_permissions=True
        )
    
    def get_serialized_application(self, application):
        app_data = base_application_serializer(application)
        app_data['employer_name'] = application.employer_job.employer.employer_name
        app_data['employer_id'] = application.employer_job.employer_id
        app_data['title'] = application.employer_job.job_title
        return app_data
    
    
class AdminAtsJobsView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        save_ats_data()
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Updated all ATS jobs'
        })


class AdminJobScrapersView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        employer_scrapers = Employer.objects.select_related('applicant_tracking_system').filter(has_job_scraper=True)
        return Response(status=status.HTTP_200_OK, data=[{
            'employer_id': employer.id,
            'employer_name': employer.employer_name,
            'ats': employer.applicant_tracking_system.name if employer.applicant_tracking_system else None,
            'last_job_scrape_success_dt': get_datetime_format_or_none(employer.last_job_scrape_success_dt),
            'has_job_scrape_failure': employer.has_job_scrape_failure
        } for employer in employer_scrapers])
    
    def post(self, request):
        employer_names = self.data.get('employer_names')
        is_run_all = self.data.get('is_run_all')
        is_run_workable = self.data.get('is_run_workable')
        if not any((employer_names, is_run_all, is_run_workable)):
            return Response('You must provide a list of employer names', status=status.HTTP_400_BAD_REQUEST)
        if is_run_workable:
            parse_workable_xml_jobs()
        else:
            run_job_scrapers(employer_names=None if is_run_all else employer_names)
        # res = task_run_job_scrapers.delay(employer_names=employer_names)
        # logger.info(f'Sent add task: ID = {res.id}')
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully kicked off job scraper'
        })


class AdminEmployerView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request, employer_id=None):
        employer_id = employer_id or self.data.get('employer_id')
        if employer_id:
            employer = EmployerView.get_employers(employer_id=employer_id)
            return Response(status=status.HTTP_200_OK, data=self.get_serialized_employer(employer))
        
        employer_filter = Q()
        if filters := self.query_params.get('filter_by'):
            filters = json.loads(filters)
            if employer_name_text := filters.get('employer_name_text'):
                employer_filter &= Q(employer_name__iregex=f'^.*{employer_name_text}.*$')
        
        employers = EmployerView.get_employers(employer_filter=employer_filter).order_by('id')
        paged_employers = Paginator(employers, per_page=20)
        page_count = self.query_params.get('page_count', 1)
        return Response(status=status.HTTP_200_OK, data={
            'total_employer_count': len(employers),
            'total_page_count': paged_employers.num_pages,
            'employers': [self.get_serialized_employer(e) for e in paged_employers.get_page(page_count)]
        })
    
    @atomic
    def post(self, request):
        # Create employer
        employer = Employer()
        self.update_employer(employer, self.data, self.files)
        
        # Add subscription
        if employee_seats := self.data.get('employee_seats'):
            EmployerSubscription(
                employer=employer,
                status=EmployerSubscription.SubscriptionStatus.ACTIVE.value,
                employee_seats=employee_seats
            ).save()
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Employer successfully created'
        })
    
    @atomic
    def put(self, request, employer_id=None):
        employer_id = employer_id or self.data.get('employer_id')
        if not employer_id:
            return Response('You must provide an employer ID', status=status.HTTP_400_BAD_REQUEST)

        employer = EmployerView.get_employers(employer_id=employer_id)
        self.update_employer(employer, self.data, self.files)
        
        employee_seats = self.data.get('employee_seats')
        subscription_status = self.data.get('subscription_status')
        if employee_seats or subscription_status:
            subscription = EmployerSubscriptionView.get_subscription(employer)
            if not subscription:
                subscription = EmployerSubscription(employer=employer)
            if subscription.stripe_key:
                return Response('You can\'t update a subscription for an employer on a paid plan', status=status.HTTP_400_BAD_REQUEST)
            subscription.employee_seats = employee_seats or subscription.employee_seats
            subscription.status = subscription_status or subscription.status
            subscription.save()
            
        # self.assign_employer_admin_permission(new_account_owner, employer)

        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Employer successfully updated'
        })

    def delete(self, request, employer_id):
        employer = Employer.objects.get(id=employer_id)
        employer.delete()
        return get_success_response(f'Employer - {employer.employer_name} - has been deleted')

    @staticmethod
    def get_serialized_employer(employer: Employer):
        subscription = EmployerSubscriptionView.get_subscription(employer)
        subscription_data = {
            'employee_seats': None,
            'subscription_status': None,
            'is_manual_subscription': True,
        }
        if subscription:
            subscription_data = {
                'employee_seats': subscription.employee_seats,
                'subscription_status': subscription.status,
                'is_manual_subscription': not subscription.stripe_key,
            }
        
        return {
            'id': employer.id,
            'name': employer.employer_name,
            'name_aliases': '|'.join(employer.employer_name_aliases) if employer.employer_name_aliases else None,
            'organization_type': employer.organization_type,
            'job_board_url': employer.main_job_board_link,
            'logo_url': employer.logo_square_88.url if employer.logo_square_88 else None,
            'joined_date': get_datetime_format_or_none(employer.created_dt),
            'email_domains': employer.email_domains,
            'is_use_job_url': employer.is_use_job_url,
            **subscription_data
        }
    
    @staticmethod
    def update_employer(employer, data, files):
        set_object_attributes(employer, data, {
            'employer_name': AttributeCfg(form_name='name'),
            'employer_name_aliases': AttributeCfg(form_name='name_aliases'),
            'email_domains': None,
            'is_use_job_url': None,
            'organization_type': None
        })
        
        if 'logo' in files:
            employer.logo = files.get('logo')[0] if files.get('logo') else None
        employer.save()
    
    @staticmethod
    def assign_employer_admin_permission(user, employer):
        admin_group = EmployerAuthGroup.objects.get(employer_id=None, name='Admin')
        user_admin_group_ids = {g.permission_group_id for g in user.employer_permission_group.all()}
        # Only assign permission if user doesn't have it already
        if admin_group.id not in user_admin_group_ids:
            UserEmployerPermissionGroup(
                user=user,
                employer=employer,
                permission_group=admin_group,
                is_employer_approved=True
            ).save()


class AdminUserView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def get(self, request):
        filters = json.loads(self.query_params['filters'])
        page_count = self.query_params['page_count']
        employer_id = filters.get('employer_id')
        if not self.user.is_admin:
            if not employer_id:
                return get_error_response('You must provide an employer ID')
            if employer_id != self.user.employer_id:
                return get_error_response('You do not have access to this employer')
        
        user_filter = Q()
        if employer_id:
            user_filter &= Q(employer_id=employer_id)
        users = UserView.get_user(
            self.user, user_filter=user_filter, is_check_permission=False, employer_id_permissions=employer_id
        ).order_by(
            f'{"-" if coerce_bool(self.query_params["is_descending"]) else ""}{self.query_params.get("sort_order", "id")}',
            'id'  # used to ensure deterministic results
        )
        
        # This differs from the employer_id filter because this is used to narrow results for admins
        # The employer_id filter is used for employers that should only be able to view their respective employees
        if employer_ids := filters.get('employerIds'):
            users = users.filter(employer_id__in=employer_ids)
        
        if search_text := filters.get('searchText'):
            search_filter = Q(first_name__iregex=f'^.*{search_text}.*$')
            search_filter |= Q(last_name__iregex=f'^.*{search_text}.*$')
            search_filter |= Q(email__iregex=f'^.*{search_text}.*$')
            search_filter |= Q(business_email__iregex=f'^.*{search_text}.*$')
            users = users.filter(search_filter)
        
        if user_type_bits := filters.get('userTypeBits'):
            users = users.filter(user_type_bits__lt=F('user_type_bits') + (1 * F('user_type_bits').bitand(user_type_bits)))
            
        if permission_group_ids := filters.get('permissionGroupIds'):
            users = users.filter(employer_permission_group__permission_group_id__in=permission_group_ids)

        if is_approval_required := filters.get('isApprovalRequired'):
            users = users.filter(is_approval_required__in=is_approval_required)
            
        if is_active := filters.get('isActive'):
            is_not_active = [not x for x in is_active]
            users = users.filter(is_employer_deactivated__in=is_not_active)
            
        if has_employee_seat := filters.get('hasEmployeeSeat'):
            users = users.filter(has_employee_seat__in=has_employee_seat)
            
        if profession_ids := filters.get('professionIds'):
            users = users.filter(profession_id__in=profession_ids)
            
        if is_account_owner := filters.get('isAccountOwner'):
            users = users.filter(is_employer_owner__in=is_account_owner)
            
        paged_users = Paginator(users, per_page=25)
        data = {
            'total_page_count': paged_users.num_pages,
            'total_user_count': paged_users.count,
            'users': [get_serialized_user(user, is_include_employer_info=True, is_include_personal_info=True) for user in paged_users.get_page(page_count)]
        }
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    
class AdminUserCreatedJobApprovalView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        job_ids = self.data['job_ids']
        is_approved = self.data['is_approved']
        if job_ids and (not isinstance(job_ids, list)):
            job_ids = [job_ids]
        
        jobs = EmployerJob.objects.filter(id__in=job_ids)
        for job in jobs:
            job.is_job_approved = is_approved
        
        EmployerJob.objects.bulk_update(jobs, ['is_job_approved'])
        
        return get_success_response(f'{len(jobs)} jobs were {"approved" if is_approved else "un-approved"}')
    
    
class AdminTaxonomyView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        update_taxonomies()
        run_job_title_standardization(is_non_standardized_only=not self.data['is_run_all'])
        return get_success_response('Taxonomy updated')
    
    
class AdminUserConnectionsView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        is_null_only = self.data.get('is_null_only')
        is_exclude_employer = self.data.get('is_exclude_employer')
        is_exclude_profession = self.data.get('is_exclude_profession')
        user_connections = AdminUserConnectionsView.get_user_connections(
            is_null_only=is_null_only,
            is_exclude_employer=is_exclude_employer,
            is_exclude_profession=is_exclude_profession
        )
        
        if not is_exclude_employer:
            employer_map = AdminUserConnectionsView.get_employer_map()
            AdminUserConnectionsView.update_employers(user_connections, employer_map, is_null_only=is_null_only)
            
        if not is_exclude_profession:
            AdminUserConnectionsView.update_professions(user_connections, is_null_only=is_null_only)
            
        return get_success_response('Updated user connections')
    
    @staticmethod
    def get_user_connections(is_null_only=False, is_exclude_employer=False, is_exclude_profession=False):
        connection_filter = None
        if is_null_only:
            if not is_exclude_employer:
                connection_filter = Q(employer__isnull=True)
            if not is_exclude_profession:
                if not connection_filter:
                    connection_filter = Q(profession__isnull=True)
                else:
                    connection_filter |= Q(profession__isnull=True)
        
        connection_filter = connection_filter or Q()
        return UserConnection.objects.filter(connection_filter)
    
    @staticmethod
    def get_employer_map():
        employer_map = {}
        for e in (
            Employer.objects
            .filter(organization_type=Employer.ORG_TYPE_EMPLOYER)
            .values('employer_name', 'employer_name_aliases', 'id')
        ):
            employer_map[e['employer_name'].lower()] = e['id']
            if aliases := e['employer_name_aliases']:
                for alias in aliases:
                    employer_map[alias.lower()] = e['id']
        return employer_map
    
    @staticmethod
    def update_employers(user_connections, employer_map, is_null_only=False):
        for connection in user_connections:
            if is_null_only and connection.employer_id:
                continue
            
            connection.employer_id = employer_map.get(connection.employer_raw.lower())
            connection.modified_dt = timezone.now()
            
        UserConnection.objects.bulk_update(user_connections, ['employer_id', 'modified_dt'])
        
    @staticmethod
    def update_professions(user_connections, is_null_only=False):
        update_user_connections = []
        for connection in user_connections:
            if is_null_only and connection.profession_id:
                continue
            
            connection.profession = get_standardized_job_taxonomy(connection.job_title)
            connection.modified_dt = timezone.now()
            update_user_connections.append(connection)
        
        UserConnection.objects.bulk_update(update_user_connections, ['profession', 'modified_dt'])