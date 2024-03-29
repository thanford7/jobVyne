__all__ = ('SocialPlatformView', 'SocialLinkView', 'SocialLinkJobsView', 'ShareSocialLinkView')

import json
import logging
from collections import defaultdict
from datetime import timedelta
from typing import Union

from django.core.paginator import Paginator
from django.db.models import Prefetch, Q, QuerySet
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, WARNING_MESSAGES_KEY, get_error_response
from jvapp.apis.taxonomy import TaxonomyJobProfessionView
from jvapp.models import JobVyneUser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.employer import ConnectionTypeBit, Employer, EmployerConnection, Taxonomy
from jvapp.models.job_seeker import JobApplication
from jvapp.models.job_subscription import JobSubscription
from jvapp.models.location import Location, REMOTE_TYPES
from jvapp.models.social import *
from jvapp.models.tracking import Message, PageView
from jvapp.models.user import UserConnection
from jvapp.serializers.employer import get_serialized_currency, get_serialized_employer_job
from jvapp.serializers.location import get_serialized_location
from jvapp.serializers.social import *
from jvapp.utils.data import AttributeCfg, coerce_bool, coerce_int, set_object_attributes
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.email import send_django_email
from jvapp.utils.message import send_sms_message
from jvapp.utils.sanitize import sanitize_html

logger = logging.getLogger(__name__)


class SocialPlatformView(JobVyneAPIView):
    
    def get(self, request):
        data = [get_serialized_social_platform(sp) for sp in SocialPlatform.objects.all()]
        return Response(status=status.HTTP_200_OK, data=data)


class SocialLinkView(JobVyneAPIView):
    
    def get(self, request, link_id=None):
        if link_id:
            data = get_serialized_social_link(self.get_link(self.user, link_id=link_id))
        else:
            if owner_id := self.query_params.get('owner_id'):
                q_filter = Q(owner_id=owner_id)
            elif employer_id := self.query_params.get('employer_id'):
                q_filter = Q(employer_id=employer_id, owner_id__isnull=True, name__isnull=False)
            else:
                raise ValueError('You must provide an ID, owner ID, or employer ID')
            
            data = []
            logger.info('Fetching social links')
            social_links = self.get_link(self.user, social_link_filter=q_filter)
            logger.info(f'Serializing social links ({len(social_links)})')
            for social_link in social_links:
                logger.info('Serializing link')
                serialized_link = get_serialized_social_link(social_link)
                # Only fetch job count for specific user because a database call
                # is required per social_link and is not performant
                logger.info('Getting job count')
                if owner_id:
                    jobs, paginated_jobs = SocialLinkJobsView.get_jobs_from_social_link(social_link, is_include_fetch=False)
                    serialized_link['jobs_count'] = paginated_jobs.count
                data.append(serialized_link)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request):
        new_link = SocialLink()
        job_ids = None
        if job_id := self.data.get('job_id'):
            job_ids = [job_id]
        new_link = self.create_or_update_link(new_link, self.data, user=self.user, job_ids=job_ids)
        is_get_or_create = self.data.get('is_get_or_create')
        if is_get_or_create:
            data = {
                'social_link': get_serialized_social_link(new_link)
            }
        else:
            # Sometimes we want to silently get or create a link (e.g. when a user is sharing an individual job)
            data = {
                SUCCESS_MESSAGE_KEY: 'Created a new job link',
                'id': new_link.id
            }
        return Response(status=status.HTTP_200_OK, data=data)
    
    def put(self, request):
        if not (social_link_id := self.data.get('social_link_id')):
            return Response('A link filter ID is required', status=status.HTTP_400_BAD_REQUEST)
        link = self.get_link(self.user, link_id=social_link_id)
        self.create_or_update_link(link, self.data, self.user)
        
        # Need to refetch to get associated objects
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'The job link was successfully updated'
        })
    
    @atomic
    def delete(self, request):
        social_link_id = self.data.get('social_link_id')
        social_link_ids = [social_link_id] if social_link_id else self.data.get('social_link_ids')
        if not social_link_ids:
            return Response('A link filter ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        links = self.get_link(self.user, social_link_filter=Q(id__in=social_link_ids))
        for link in links:
            link.jv_check_permission(PermissionTypes.DELETE.value, self.user)
            link.is_archived = True
        SocialLink.objects.bulk_update(links, ['is_archived'])
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully archived job link'
        })
    
    @staticmethod
    def get_or_create_employee_referral_links(employees, employer):
        from jvapp.apis.job_subscription import JobSubscriptionView
        employer_job_subscription = JobSubscriptionView.get_or_create_employer_own_subscription(employer.id)
        current_employee_links = {
            (sl.employer_id, sl.owner_id): sl for sl in
            SocialLink.objects.prefetch_related(
                'job_subscriptions'
            ).filter(owner_id__in=[e.id for e in employees], employer_id=employer.id)
            if (sl.employer_id and sl.owner_id)
        }
        # TODO: Don't need to create referral links - just use the connection id in the url for each employee
        employee_links = []
        for employee in employees:
            if not employee.employer_id:
                raise ValueError('This user is not associated with an employer')
            if employee.employer_id != employer.id:
                raise ValueError('This user is associated with a different employer')
            employee_link = current_employee_links.get((employee.employer_id, employee.id))
            if not employee_link:
                employee_link = SocialLink(
                    owner_id=employee.id,
                    employer_id=employee.employer_id,
                    name=f'{employer.employer_name} Referral'
                )
                employee_link.save()
                employee_link.job_subscriptions.add(employer_job_subscription.id)
            elif (employer_job_subscription not in employee_link.job_subscriptions.all()):
                employee_link.job_subscriptions.add(employer_job_subscription.id)
            employee_links.append(employee_link)
        return employee_links
    
    @staticmethod
    def get_or_create_single_job_link(job, owner_id=None, employer_id=None):
        from jvapp.apis.job_subscription import JobSubscriptionView
        job_subscription = JobSubscriptionView.get_or_create_single_job_subscription(job.id)
        social_link = Q(job_subscriptions__id=job_subscription.id)
        if owner_id:
            social_link &= Q(owner_id=owner_id)
        elif employer_id:
            social_link &= Q(employer_id=employer_id)
        social_link = next((
            link for link in
            SocialLinkView.get_link(None, social_link_filter=social_link, is_use_permissions=False)
            if len(link.job_subscriptions.all()) == 1
        ), None)
        if not social_link:
            social_link = SocialLink(
                is_archived=True,  # We don't want to show the user these links directly
                owner_id=owner_id,
                employer_id=employer_id,
                name=f'Job: {job.job_title}'
            )
            social_link.save()
            social_link.job_subscriptions.add(job_subscription.id)
        
        return social_link
    
    @staticmethod
    @atomic
    def create_or_update_link(link, data, user=None, job_ids: list = None):
        cfg = {
            'is_default': AttributeCfg(is_ignore_excluded=True),
            'name': AttributeCfg(form_name='link_name', is_ignore_excluded=True)
        }
        job_subscription_ids = []
        if job_ids:
            from jvapp.apis.job_subscription import JobSubscriptionView
            for job_id in job_ids:
                job_subscription = JobSubscriptionView.get_or_create_single_job_subscription(job_id)
                job_subscription_ids.append(job_subscription.id)
        job_subscription_ids = tuple(sorted(job_subscription_ids or data.get('job_subscription_ids', [])))
        
        is_new = not link.created_dt
        
        # TODO: Handle un-archiving links
        # Add owner and employer for new link
        if is_new:
            cfg = {
                'owner_id': None,
                'employer_id': None,
                **cfg
            }
            existing_links_map = {
                tuple(sorted([js.id for js in sl.job_subscriptions.all()])): sl for sl in
                SocialLink.objects.prefetch_related('job_subscriptions').filter(owner_id=data.get('owner_id'),
                                                                                employer_id=data.get('employer_id'))
            }
            link = existing_links_map.get(job_subscription_ids, link)
        
        set_object_attributes(link, data, cfg)
        if user:
            permission_type = PermissionTypes.EDIT.value if link.id else PermissionTypes.CREATE.value
            link.jv_check_permission(permission_type, user)
        link.save()
        
        # Remove default flag from previous links
        if link.is_default:
            existing_default_links = SocialLinkView.get_link(
                user,
                social_link_filter=Q(owner_id=link.owner_id) & Q(employer_id=link.employer_id) & Q(
                    is_default=True) & ~Q(
                    id=link.id),
                is_use_permissions=False
            )
            for existing_link in existing_default_links:
                existing_link.is_default = False
                existing_link.save()
        
        if job_subscription_ids:
            link.job_subscriptions.set(job_subscription_ids)
        
        return link
    
    @staticmethod
    def get_link(
            user, link_id=None, social_link_filter=None, start_dt=None, end_dt=None, is_use_permissions=True
    ):
        if link_id:
            social_link_filter = Q(id=link_id)
        elif (not link_id) and social_link_filter:
            social_link_filter &= Q(is_archived=False)
        
        app_filter = Q()
        view_filter = Q()
        if start_dt:
            app_filter &= Q(created_dt__gte=start_dt)
            view_filter &= Q(access_dt__gte=start_dt)
        if end_dt:
            app_filter &= Q(created_dt__lte=end_dt)
            view_filter &= Q(access_dt__lte=end_dt)
        
        app_prefetch = Prefetch(
            'job_application',
            queryset=JobApplication.objects.select_related('employer_job').filter(app_filter)
        )
        
        page_view_prefetch = Prefetch(
            'page_view',
            queryset=PageView.objects.filter(view_filter)
        )
        
        subscriptions_prefetch = Prefetch(
            'job_subscriptions',
            queryset=JobSubscription.objects.prefetch_related(
                'filter_location',
                'filter_location__city',
                'filter_location__state',
                'filter_location__country',
                'filter_job',
                'filter_employer'
            )
        )
        
        links = SocialLink.objects \
            .select_related('employer', 'owner') \
            .prefetch_related(
            subscriptions_prefetch,
            app_prefetch,
            page_view_prefetch
        ) \
            .filter(social_link_filter)
        
        if is_use_permissions:
            links = SocialLink.jv_filter_perm(user, links)
        
        if link_id:
            if not links:
                raise SocialLink.DoesNotExist
            return links[0]
        
        return links


class SocialLinkJobsView(JobVyneAPIView):
    permission_classes = [AllowAny]
    LOOKBACK_DAYS = 90
    JOBS_PER_PAGE = 36
    
    def get(self, request):
        from jvapp.apis.job_subscription import JobSubscriptionView
        from jvapp.apis.employer import EmployerJobView  # Avoid circular import
        page_count = coerce_int(self.query_params.get('page_count', 1))
        link_id = self.query_params.get('link_id')
        profession_key = self.query_params.get('profession_key')
        employer_key = self.query_params.get('employer_key')
        user_key = self.query_params.get('user_key')
        job_key = self.query_params.get('job_key')
        job_subscription_ids = self.query_params.getlist('job_subscription_ids[]') or self.query_params.get(
            'job_subscription_ids')
        
        # TODO: Add recommended jobs based on page owner's profession
        if page_owner_user_id := self.query_params.get('connection_id'):
            try:
                page_owner_user = JobVyneUser.objects.select_related('profession').get(id=page_owner_user_id)
            except JobVyneUser.DoesNotExist:
                pass
        
        logger.info('Fetching social link')
        link = None
        warning_message = None
        if link_id:
            try:
                link = SocialLinkView.get_link(
                    self.user,
                    link_id=link_id,
                    is_use_permissions=False  # This is a public page
                )
            except SocialLink.DoesNotExist:
                warning_message = 'This link is no longer active.'
        
        jobs_filter = Q()
        if job_filters := self.query_params.get('job_filters'):
            job_filters = json.loads(job_filters)
            if job_ids := job_filters.get('job_ids'):
                jobs_filter &= Q(id__in=job_ids)
            if job_profession_ids := job_filters.get('job_profession_ids'):
                if not isinstance(job_profession_ids, list):
                    job_profession_ids = [job_profession_ids]
                job_professions = Taxonomy.objects.prefetch_related('sub_taxonomies').filter(id__in=job_profession_ids)
                total_professions = JobSubscriptionView.get_parent_and_child_professions(job_professions)
                jobs_filter &= (
                    Q(taxonomy__taxonomy_id__in=[p.id for p in total_professions])
                )
            if search_regex := job_filters.get('search_regex'):
                jobs_filter &= (
                        Q(job_title__iregex=f'^.*{search_regex}.*$') |
                        Q(employer__employer_name__iregex=f'^.*{search_regex}.*$')
                )
            if minimum_salary := job_filters.get('minimum_salary'):
                # Some jobs have a salary floor but no ceiling so we check for both
                jobs_filter &= (Q(salary_ceiling__gte=minimum_salary) | Q(salary_floor__gte=minimum_salary))
            
            jobs_filter &= SocialLinkJobsView.get_location_filter(
                job_filters.get('location'),
                coerce_int(job_filters.get('remote_type_bit')),
                job_filters.get('range_miles')
            )
        
        no_results_data = {
            'total_page_count': 0,
            'total_employer_job_count': 0,
            'jobs': [],
        }
        if job_subscription_ids:
            if not isinstance(job_subscription_ids, list):
                job_subscription_ids = [job_subscription_ids]
            # Make sure subscription IDs are valid
            # TODO: Return a warning message if a subscription ID isn't valid
            job_subscription_ids = [jid for jid in [coerce_int(jid) for jid in job_subscription_ids] if jid]
        
        is_jobs_closed = False
        is_single_job = False
        jobs = QuerySet()
        common_job_getter_kwargs = dict(
            is_include_fetch=True, applicant_user=self.user,
            is_allow_unapproved=True, jobs_per_page=self.JOBS_PER_PAGE, page_count=page_count
        )
        if not any((link_id, profession_key, employer_key, user_key, job_key, job_subscription_ids)):
            jobs, paginated_jobs = EmployerJobView.get_employer_jobs(
                employer_job_filter=jobs_filter, lookback_days=self.LOOKBACK_DAYS, **common_job_getter_kwargs
            )
            
        if job_subscription_ids:
            job_subscriptions = JobSubscriptionView.get_job_subscriptions(
                subscription_filter=Q(id__in=job_subscription_ids))
            job_subscription_filter = JobSubscriptionView.get_combined_job_subscription_filter(job_subscriptions)
            jobs_filter &= job_subscription_filter
            
            # User entered jobs may be posted to social channels like Slack with a link
            # They might not yet be approved, but we still want users to have access to the job
            # As long as this is a direct link to the job, we will display it
            is_single_job = len(job_subscriptions) == 1 and job_subscriptions[0].is_single_job_subscription
            jobs, paginated_jobs = EmployerJobView.get_employer_jobs(
                employer_job_filter=jobs_filter, **common_job_getter_kwargs
            )
            if not jobs and all((j.is_job_subscription for j in job_subscriptions)):
                is_jobs_closed = True
        elif profession_key:
            try:
                profession = TaxonomyJobProfessionView.get_job_profession_taxonomy(
                    tax_key=profession_key, is_include_subs=True
                )
                profession_ids = [profession['id']] + [sp['id'] for sp in profession['sub_professions']]
            except Taxonomy.DoesNotExist:
                return Response(status=status.HTTP_200_OK, data=no_results_data)
            jobs_filter &= Q(taxonomy__taxonomy_id__in=profession_ids)
            jobs, paginated_jobs = EmployerJobView.get_employer_jobs(
                employer_job_filter=jobs_filter, lookback_days=self.LOOKBACK_DAYS, **common_job_getter_kwargs
            )
        elif employer_key:
            try:
                employer = Employer.objects.get(employer_key=employer_key)
            except Employer.DoesNotExist:
                return Response(status=status.HTTP_200_OK, data=no_results_data)
            if coerce_bool(self.query_params.get('is_employer')):
                jobs_filter &= Q(employer=employer)
            else:
                job_subscriptions = JobSubscriptionView.get_job_subscriptions(employer_id=employer.id)
                job_subscription_filter = JobSubscriptionView.get_combined_job_subscription_filter(job_subscriptions)
                jobs_filter &= job_subscription_filter
            jobs, paginated_jobs = EmployerJobView.get_employer_jobs(
                employer_job_filter=jobs_filter, **common_job_getter_kwargs
            )
        elif user_key:
            try:
                employer_connection_prefetch = Prefetch(
                    'employer_connection',
                    queryset=EmployerConnection.objects.filter(
                        ~Q(connection_type=ConnectionTypeBit.NO_CONNECTION.value)),
                    to_attr='employer_connections'
                )
                user_connection_prefetch = Prefetch(
                    'owner_connection',
                    queryset=UserConnection.objects.filter(employer_id__isnull=False),
                    to_attr='user_connections'
                )
                user = (
                    JobVyneUser.objects
                    .select_related('home_location', 'home_location__city', 'home_location__state',
                                    'home_location__country')
                    .prefetch_related(employer_connection_prefetch, user_connection_prefetch)
                    .get(user_key=user_key)
                )
                connection_employer_ids = (
                        [ec.employer_id for ec in user.employer_connections]
                        + [uc.employer_id for uc in user.user_connections]
                )
                jobs_filter &= Q(employer_id__in=set(connection_employer_ids))
                
                # Limit jobs to close to the user's home location
                # This is important for large global companies. For example if the user is connected to Google
                # and lives in the US, it's not likely they can help connect someone to Google in India
                if user.home_location:
                    jobs_filter &= SocialLinkJobsView.get_location_filter(
                        {
                            'city': user.home_location.city.name if user.home_location.city else None,
                            'state': user.home_location.state.name if user.home_location.state else None,
                            'country': user.home_location.country.name if user.home_location.country else None
                        },
                        0,
                        None
                    )
                
                jobs, paginated_jobs = EmployerJobView.get_employer_jobs(
                    employer_job_filter=jobs_filter, lookback_days=self.LOOKBACK_DAYS, **common_job_getter_kwargs
                )
            except JobVyneUser.DoesNotExist:
                return Response(status=status.HTTP_200_OK, data=no_results_data)
        elif link_id:
            if not link:
                no_results_data[WARNING_MESSAGES_KEY] = [warning_message]
                return Response(status=status.HTTP_200_OK, data=no_results_data)
            jobs, paginated_jobs = self.get_jobs_from_social_link(
                link, extra_filter=jobs_filter, is_include_fetch=True, user=self.user,
                jobs_per_page=self.JOBS_PER_PAGE, page_count=page_count
            )
        elif job_key:
            jobs, paginated_jobs = EmployerJobView.get_employer_jobs(
                employer_job_filter=Q(job_key=job_key), lookback_days=self.LOOKBACK_DAYS, **common_job_getter_kwargs
            )
        
        employer_ids = set([j.employer_id for j in jobs])
        employer_connections = (
            EmployerConnection.objects
            .select_related('user')
            .prefetch_related('hiring_jobs')
            .filter(employer_id__in=employer_ids, user__is_share_connections=True)
            .filter(~Q(connection_type=ConnectionTypeBit.NO_CONNECTION.value))
        )
        employer_connections_map = defaultdict(list)
        for conn in employer_connections:
            employer_connections_map[conn.employer_id].append(conn)
        
        user_connections = (
            UserConnection.objects
            .select_related('owner', 'profession', 'employer', 'connection_user')
            .filter(employer_id__in=employer_ids, owner__is_share_connections=True)
        )
        user_connections_map = defaultdict(list)
        for conn in user_connections:
            user_connections_map[conn.employer_id].append(conn)
        
        data = {
            'total_page_count': paginated_jobs.num_pages,
            'total_job_count': paginated_jobs.count,
            'jobs': [self.get_serialized_job(job, employer_connections_map, user_connections_map, self.user) for job in jobs],
            'is_jobs_closed': is_jobs_closed,
            'is_single_job': is_single_job
        }
        if warning_message:
            data[WARNING_MESSAGES_KEY] = [warning_message]
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    @staticmethod
    def get_serialized_job(job, employer_connections, user_connections, user):
        from jvapp.apis.community import JobConnectionsView
        job_data = {
            'employer': {
                'id': job.employer_id,
                'name': job.employer.employer_name,
                'key': job.employer.employer_key,
                'logo': job.employer.logo_square_88.url if job.employer.logo_square_88 else None,
                'description': job.employer.description,
                'ats_name': job.employer.applicant_tracking_system.name if job.employer.applicant_tracking_system else None,
                # 'industry': job.employer.industry,
                # 'employee_count_min': job.employer.size_min,
                # 'employee_count_max': job.employer.size_max,
                # 'year_founded': job.employer.year_founded,
                'website': job.employer.website_domain,
                # 'ownership_type': job.employer.ownership_type,
                # 'linkedin_handle': job.employer.linkedin_handle
            },
            'id': job.id,
            'ats_job_key': job.ats_job_key,
            'is_use_job_url': job.employer.is_use_job_url,
            'application_url': job.application_url,
            'job_title': job.job_title,
            'job_description': job.job_description,
            'job_description_summary': job.job_description_summary,
            'responsibilities': job.responsibilities,
            'qualifications': job.qualifications,
            'technical_qualifications': job.technical_qualifications,
            'is_remote': job.is_remote,
            'open_date': get_datetime_format_or_none(job.open_date),
            'salary_currency': get_serialized_currency(job.salary_currency),
            'salary_floor': job.salary_floor,
            'salary_ceiling': job.salary_ceiling,
            'salary_interval': job.salary_interval,
            'salary_text': job.salary_text,
            'employment_type': job.employment_type,
            'locations': [get_serialized_location(l) for l in job.locations.all()],
            'locations_text': job.locations_text,
            'profession': job.profession.name if job.profession else 'Unknown',
            'own_connection': 0
        }
        
        general_connections = defaultdict(int)
        for conn in (employer_connections.get(job.employer_id) or []):
            is_owner = False
            if user and user.id == conn.user_id:
                is_owner = True
            is_hiring_team = job.id in [hiring_job.id for hiring_job in conn.hiring_jobs.all()]
            connection_type = conn.connection_type
            if is_hiring_team and conn.connection_type == ConnectionTypeBit.CURRENT_EMPLOYEE.value:
                connection_type = ConnectionTypeBit.HIRING_MEMBER.value
            if is_owner:
                job_data['own_connection'] = conn.connection_type
                continue
            
            general_connections[connection_type] += 1
        
        job_data['general_connections'] = []
        for connection_type, connection_count in general_connections.items():
            job_data['general_connections'].append({'connection_type': connection_type, 'connection_count': connection_count})
        
        job_data['general_connections'].sort(key=lambda x: x['connection_type'])
        
        user_employer_connections = user_connections.get(job.employer_id)
        if not user_employer_connections:
            job_data['user_connections'] = []
        else:
            same_profession_key = 'same_profession'
            ta_profession_key = 'ta_profession'
            other_profession_key = 'other_profession'
            user_connections_count = {
                same_profession_key: 0,
                ta_profession_key: 0,
                other_profession_key: 0
            }
            for conn in user_employer_connections:
                serialized_connection = JobConnectionsView.get_serialized_user_connection(conn, job.profession)
                if serialized_connection.get('is_same_profession'):
                    user_connections_count[same_profession_key] += 1
                elif serialized_connection['is_ta']:
                    user_connections_count[ta_profession_key] += 1
                else:
                    user_connections_count[other_profession_key] += 1
            
            job_data['user_connections'] = [
                {'type': key, 'count': count, 'sort_idx': 1 if key == same_profession_key else (2 if key == ta_profession_key else 3)}
                for (key, count) in user_connections_count.items() if count
            ]
            job_data['user_connections'].sort(key=lambda x: x['sort_idx'])
        
        if hasattr(job, 'user_job_applications'):
            if job_application := next((app for app in job.user_job_applications), None):
                job_data['application'] = {
                    'id': job_application.id,
                    'created_dt': job_application.created_dt,
                    'is_external': job_application.is_external_application,
                    'status': job_application.application_status,
                }
        
        return job_data
    
    @staticmethod
    def get_jobs_from_social_link(link, extra_filter=None, is_include_fetch=True, user=None, jobs_per_page=25, page_count=1):
        from jvapp.apis.employer import EmployerJobView
        from jvapp.apis.job_subscription import JobSubscriptionView
        
        logger.info('Fetching job filter')
        job_filter = JobSubscriptionView.get_combined_job_subscription_filter(link.job_subscriptions.all())
        if extra_filter:
            job_filter &= extra_filter
        
        logger.info('Fetching jobs')
        return EmployerJobView.get_employer_jobs(
            employer_job_filter=job_filter, is_include_fetch=is_include_fetch, applicant_user=user,
            jobs_per_page=jobs_per_page, page_count=page_count
        )
    
    @staticmethod
    def get_location_filter(location_dict: Union[dict, None], remote_type_bit: int, range_miles: Union[int, None]):
        location_filter = None
        remote_type_bit = remote_type_bit or 0
        location_dict = location_dict or {}
        city = location_dict.get('city')
        state = location_dict.get('state')
        country = location_dict.get('country')
        if city and range_miles:
            start_point = Location.get_geometry_point(location_dict['latitude'], location_dict['longitude'])
            location_filter = (
                    Q(locations__geometry__within_miles=(start_point, range_miles)) |
                    (Q(locations__city__name__isnull=True) & Q(locations__state__name=state)) |
                    (Q(locations__city__name__isnull=True) & Q(locations__state__name__isnull=True) & Q(
                        locations__country__name=country))
            )
        elif state or country:
            if state:
                location_filter = (
                        Q(locations__state__name=state) |
                        (Q(locations__state__name__isnull=True) & Q(locations__country__name=country))
                )
            elif country:
                location_filter = Q(locations__country__name=country)
        
        remote_filter = None
        if (not remote_type_bit and location_filter) or (remote_type_bit & REMOTE_TYPES.YES.value):
            remote_filter = Q(locations__is_remote=True)
            if country:
                # Some remote jobs don't have a country. In this case, we assume it's a global remote job
                remote_filter &= (Q(locations__country__name=country) | Q(locations__country__name__isnull=True))
        
        if remote_type_bit and (remote_type_bit & REMOTE_TYPES.NO.value) and not (
                remote_type_bit & REMOTE_TYPES.YES.value):
            remote_filter = Q(locations__is_remote=False)
        
        if remote_filter and location_filter:
            if remote_type_bit:
                location_filter &= remote_filter
            else:
                location_filter |= remote_filter
        elif remote_filter or location_filter:
            location_filter = location_filter or remote_filter
        else:
            location_filter = Q()
        
        return location_filter


class SocialLinkPostJobsView(JobVyneAPIView):
    JOB_LOOKBACK_DAYS = 20
    MAX_JOBS = 10
    
    def get(self, request):
        max_jobs = self.query_params.get('max_job_count') or self.MAX_JOBS
        employer_id = self.query_params.get('employer_id')
        user_id = self.query_params.get('user_id')
        if not any((employer_id, user_id)):
            raise ValueError('An employer ID or user ID is required')
        
        job_subscriptions = None
        if social_link_id := self.query_params.get('social_link_id'):
            social_link = SocialLinkView.get_link(self.user, link_id=social_link_id)
            job_subscriptions = social_link.job_subscriptions.all()
        
        jobs = self.get_jobs_for_post(
            max_jobs,
            self.query_params['social_channel'],
            employer_id=employer_id,
            owner_id=user_id,
            job_subscriptions=job_subscriptions
        )
        
        return Response(status=status.HTTP_200_OK, data=[
            get_serialized_employer_job(j) for j in jobs
        ])
    
    @staticmethod
    def get_jobs_for_post(max_job_count, social_channel, employer_id=None, owner_id=None, recipient_id=None,
                          job_subscriptions=None):
        from jvapp.apis.employer import EmployerJobView
        from jvapp.apis.job_subscription import JobSubscriptionView
        
        """
        Owners and employers create job subscriptions which filter the relevant jobs to them and their users
        Recipients are part of a channel that an owner or employer uses (e.g. a recipient is part of a Slack group
        managed by an employer).
        Jobs are narrowed down by an employer or owner's subscriptions
        Then we check that:
            (1a) The employer or owner has not PUSHED a post to a given channel
            (1b) The recipient has not RECEIVED a post to a given channel
        """
        
        if not any((employer_id, owner_id, recipient_id)):
            raise ValueError('An employer ID, owner ID, or recipient ID is required')
        
        # Get job subscriptions
        if not job_subscriptions:
            if owner_id:
                job_subscriptions = JobSubscriptionView.get_job_subscriptions(user_id=owner_id)
                jobs_filter = JobSubscriptionView.get_combined_job_subscription_filter(job_subscriptions)
                if not jobs_filter:
                    raise ValueError('User does not have any job subscriptions')
            else:
                jobs_filter = Q(employer_id=employer_id)
                job_subscriptions = JobSubscriptionView.get_job_subscriptions(employer_id=employer_id)
                if job_subscription_filter := JobSubscriptionView.get_combined_job_subscription_filter(
                        job_subscriptions):
                    jobs_filter = (jobs_filter | job_subscription_filter)
        else:
            jobs_filter = JobSubscriptionView.get_combined_job_subscription_filter(job_subscriptions)
        
        # Only post recent jobs
        recent_jobs_filter = Q(
            open_date__gte=timezone.now().date() - timedelta(days=SocialLinkPostJobsView.JOB_LOOKBACK_DAYS))
        
        # Don't post jobs that have already been posted
        job_post_filter = Q(job_post__channel=social_channel)
        if recipient_id:
            job_post_filter &= Q(job_post__recipient_id=recipient_id)
        elif owner_id:
            job_post_filter &= Q(job_post__owner_id=owner_id)
        else:
            job_post_filter &= Q(job_post__employer_id=employer_id)
        
        # Recipients may have their own preferred jobs which will be different than an
        # employer or owner's subscriptions. We prioritize these jobs first
        preferred_jobs = []
        if recipient_id:
            home_location_prefetch = Prefetch(
                'home_location',
                queryset=Location.objects.select_related('city', 'state', 'country')
            )
            owner = (
                JobVyneUser.objects
                .prefetch_related(
                    'membership_employers',
                    'job_search_professions',
                    'job_search_professions__sub_taxonomies',
                    home_location_prefetch
                )
                .get(id=recipient_id)
            )
            preferred_jobs_filter = owner.preferred_jobs_filter
            preferred_jobs_filter &= recent_jobs_filter
            preferred_jobs_filter &= ~job_post_filter
            preferred_jobs, _ = EmployerJobView.get_employer_jobs(employer_job_filter=preferred_jobs_filter, jobs_per_page=100)
            preferred_jobs = SocialLinkPostJobsView.get_unique_jobs(preferred_jobs)[:max_job_count]
            preferred_jobs = SocialLinkPostJobsView.get_even_employer_distribution_jobs(preferred_jobs, max_job_count)
            
            # If we already have the max number of jobs we stop here
            if len(preferred_jobs) == max_job_count:
                return preferred_jobs
        
        # Add in other (less relevant) jobs
        jobs_filter &= recent_jobs_filter
        jobs_filter &= ~job_post_filter
        
        jobs, _ = EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter, jobs_per_page=100)
        jobs = SocialLinkPostJobsView.get_unique_jobs(jobs)
        max_non_preferred_jobs = max_job_count - len(preferred_jobs)
        jobs = SocialLinkPostJobsView.get_even_employer_distribution_jobs(jobs, max_non_preferred_jobs)
        
        return preferred_jobs + jobs[:max_non_preferred_jobs]
    
    @staticmethod
    def get_unique_jobs(jobs):
        # Make sure we only use one post for a given job title
        # Some employers create a separate post for each location for a specific job
        jobs = {(job.employer_id, job.job_title): job for job in jobs}
        return list(jobs.values())
    
    @staticmethod
    def get_even_employer_distribution_jobs(jobs, job_limit):
        # Some employers post a bunch of jobs at the same time
        # We want to make sure we don't post jobs just for one employer
        employer_jobs = defaultdict(list)
        for job in jobs:
            employer_jobs[job.employer_id].append(job)
        
        distributed_jobs = []
        remove_employer_ids = []
        employer_ids = set(employer_jobs.keys())
        while len(distributed_jobs) < job_limit and employer_ids:
            for employer_id in employer_ids:
                distributed_jobs.append(employer_jobs[employer_id].pop())
                if not len(employer_jobs[employer_id]):
                    remove_employer_ids.append(employer_id)
            for employer_id in remove_employer_ids:
                employer_ids.remove(employer_id)
                remove_employer_ids = []
        
        return distributed_jobs


class ShareSocialLinkView(JobVyneAPIView):
    
    def post(self, request):
        job_link = SocialLinkView.get_link(self.user, link_id=self.data['socialLinkId'])
        if self.user.id != job_link.owner_id:
            return get_error_response('You do not have access to this job link')
        share_type = self.data['shareType']
        if share_type == Message.MessageType.EMAIL.value:
            send_django_email(
                self.data['emailSubject'], 'emails/base_general_email.html',
                to_email=self.data['toEmail'], from_email=self.data['fromEmail'],
                html_body_content=sanitize_html(f'<p>{self.data["emailBody"]}</p>', is_email=True),
                django_context={
                    'is_exclude_final_message': True
                }
            )
            
            return Response(status=status.HTTP_200_OK, data={
                SUCCESS_MESSAGE_KEY: f'Message sent to {self.data["toEmail"]}'
            })
        elif share_type == Message.MessageType.SMS.value:
            send_sms_message(self.data['textBody'], self.data['phoneNumber'])
            return Response(status=status.HTTP_200_OK, data={
                SUCCESS_MESSAGE_KEY: f'Message sent to {self.data["phoneNumber"]}'
            })
