import json
import logging

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jobVyne.celery import app
from jvapp.apis._apiBase import ERROR_MESSAGES_KEY, JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.ats import get_ats_api
from jvapp.apis.employer import EmployerSubscriptionView, EmployerView
from jvapp.apis.job_seeker import ApplicationView
from jvapp.apis.user import UserView
from jvapp.management.commands.ats_data_pull import save_ats_data
from jvapp.models import Employer, EmployerAts, EmployerAuthGroup, EmployerSubscription, JobVyneUser, \
    UserEmployerPermissionGroup
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.permissions.general import IsAdmin
from jvapp.serializers.job_seeker import base_application_serializer
from jvapp.serializers.user import get_serialized_user
from jvapp.tasks import add, task_run_job_scrapers
from jvapp.utils.data import AttributeCfg, coerce_bool, set_object_attributes
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT
from scrape.scraper import run_job_scrapers
from scraper.scraper.runSpiders import run_crawlers


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
        employer_scrapers = Employer.objects.filter(has_job_scraper=True)
        return Response(status=status.HTTP_200_OK, data=[{
            'employer_id': employer.id,
            'employer_name': employer.employer_name,
            'last_job_scrape_success_dt': get_datetime_format_or_none(employer.last_job_scrape_success_dt),
            'has_job_scrape_failure': employer.has_job_scrape_failure
        } for employer in employer_scrapers])
    
    def post(self, request):
        employer_names = self.data.get('employer_names')
        is_run_all = self.data.get('is_run_all')
        if not (employer_names or is_run_all):
            return Response('You must provide a list of employer names', status=status.HTTP_400_BAD_REQUEST)
        # res = task_run_job_scrapers.delay(employer_names=employer_names)
        run_job_scrapers(employer_names=None if is_run_all else employer_names)
        # res = add.delay(2, 2)
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
        employers = EmployerView.get_employers(employer_filter=Q())
        return Response(status=status.HTTP_200_OK, data=[
            self.get_serialized_employer(employer) for employer in employers
        ])
    
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
        
        # Create account owner
        user = JobVyneUser.objects.create_user(
            self.data['owner_email'],
            first_name=self.data['owner_first_name'],
            last_name=self.data['owner_last_name'],
            user_type_bits=JobVyneUser.USER_TYPE_EMPLOYER,
            employer_id=employer.id,
            is_employer_owner=True
        )
        self.assign_employer_admin_permission(user, employer)
        
        # Send welcome email to owner
        UserView.send_password_reset_email(request, user.email, {
            'extra_email_context': {
                'supportEmail': EMAIL_ADDRESS_SUPPORT,
                'isNew': True
            }
        })
        
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
            
        if owner_id := self.data.get('account_owner_id'):
            new_account_owner = UserView.get_user(self.user, user_id=owner_id)
            account_owner = EmployerView.get_employer_account_owner(employer)
            if account_owner and new_account_owner != account_owner:
                account_owner.is_employer_owner = False
                account_owner.save()
            
            new_account_owner.is_employer_owner = True
            new_account_owner.save()
            self.assign_employer_admin_permission(new_account_owner, employer)

        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Employer successfully updated'
        })

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
        
        account_owner = EmployerView.get_employer_account_owner(employer)
        owner_data = {
            'owner_id': None,
            'owner_first_name': None,
            'owner_last_name': None,
            'owner_email': None
        }
        if account_owner:
            owner_data = {
                'owner_id': account_owner.id,
                'owner_first_name': account_owner.first_name,
                'owner_last_name': account_owner.last_name,
                'owner_email': account_owner.email
            }
        
        return {
            'id': employer.id,
            'name': employer.employer_name,
            'organization_type': employer.organization_type,
            'logo_url': employer.logo.url if employer.logo else None,
            'joined_date': get_datetime_format_or_none(employer.created_dt),
            'employee_count': employer.employee_count,
            'email_domains': employer.email_domains,
            'is_use_job_url': employer.is_use_job_url,
            **subscription_data,
            **owner_data
        }
    
    @staticmethod
    def update_employer(employer, data, files):
        set_object_attributes(employer, data, {
            'employer_name': AttributeCfg(form_name='name'),
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
        users = UserView.get_user(
            self.user, user_filter=Q(), is_check_permission=False,
        ).order_by(
            f'{"-" if coerce_bool(self.query_params["is_descending"]) else ""}{self.query_params.get("sort_order", "id")}',
            'id'  # used to ensure deterministic results
        )
        
        if employer_id := filters.get('employer_id'):
            users = users.filter(employer_id=employer_id)
        
        if not self.user.is_admin:
            if not employer_id:
                return Response('You must provide an employer ID', status=status.HTTP_400_BAD_REQUEST)
            if employer_id != self.user.employer_id:
                return Response('You do not have access to this employer', status=status.HTTP_401_UNAUTHORIZED)
       
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
            
        paged_users = Paginator(users, per_page=25)
        data = {
            'total_page_count': paged_users.num_pages,
            'total_user_count': paged_users.count,
            'users': [get_serialized_user(user, is_include_employer_info=True, is_include_personal_info=True) for user in paged_users.get_page(page_count)]
        }
        
        return Response(status=status.HTTP_200_OK, data=data)
