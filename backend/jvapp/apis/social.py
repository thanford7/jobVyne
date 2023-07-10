__all__ = ('SocialPlatformView', 'SocialLinkView', 'SocialLinkJobsView', 'ShareSocialLinkView')

import json
import logging
import math
from collections import defaultdict
from datetime import timedelta
from typing import Union

from django.db.models import Prefetch, Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.apis.taxonomy import TaxonomyJobTitleView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.employer import Employer, Taxonomy
from jvapp.models.job_seeker import JobApplication
from jvapp.models.location import Location, REMOTE_TYPES
from jvapp.models.social import *
from jvapp.models.tracking import Message, PageView
from jvapp.serializers.employer import get_serialized_employer, get_serialized_employer_job
from jvapp.serializers.social import *
from jvapp.utils.data import AttributeCfg, coerce_bool, coerce_int, set_object_attributes
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
            for social_link in self.get_link(self.user, social_link_filter=q_filter):
                serialized_link = get_serialized_social_link(social_link)
                # Only fetch job count for specific user because a database call
                # is required per social_link and is not performant
                if owner_id:
                    serialized_link['jobs_count'] = len(
                        SocialLinkJobsView.get_jobs_from_social_link(social_link))
                data.append(serialized_link)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request):
        new_link = SocialLink()
        new_link = self.create_or_update_link(new_link, self.data, self.user)
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
        employer_job_subscription = JobSubscriptionView.get_or_create_employer_subscription(employer.id)
        current_employee_links = {
            (sl.employer_id, sl.owner_id): sl for sl in
            SocialLink.objects.prefetch_related(
                'job_subscriptions'
            ).filter(owner_id__in=[e.id for e in employees], employer_id=employer.id)
            if (sl.employer_id and sl.owner_id)
        }
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
    def create_or_update_link(link, data, user=None):
        cfg = {
            'is_default': AttributeCfg(is_ignore_excluded=True),
            'name': AttributeCfg(form_name='link_name', is_ignore_excluded=True)
        }
        job_subscription_ids = tuple(sorted(data.get('job_subscription_ids', [])))
        
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
                SocialLink.objects.prefetch_related('job_subscriptions').filter(owner_id=data.get('owner_id'), employer_id=data.get('employer_id'))
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
        
        links = SocialLink.objects \
            .select_related('employer', 'owner') \
            .prefetch_related(
            'job_subscriptions',
            'job_subscriptions__filter_location',
            'job_subscriptions__filter_location__city',
            'job_subscriptions__filter_location__state',
            'job_subscriptions__filter_location__country',
            'job_subscriptions__filter_job',
            'job_subscriptions__filter_employer',
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
    
    EMPLOYERS_PER_PAGE = 20
    
    def get(self, request):
        from jvapp.apis.job_subscription import JobSubscriptionView
        from jvapp.apis.employer import EmployerJobApplicationRequirementView, EmployerJobView  # Avoid circular import
        page_count = coerce_int(self.query_params.get('page_count', 1))
        link_id = self.query_params.get('link_id')
        profession_key = self.query_params.get('profession_key')
        employer_key = self.query_params.get('employer_key')
        job_subscription_ids = self.query_params.get('job_subscription_ids')
        if not any([link_id, profession_key, employer_key, job_subscription_ids]):
            raise ValueError('A link ID, profession key, employer key, or job subscription id is required')
        
        logger.info('Fetching social link')
        link = SocialLinkView.get_link(
            self.user,
            link_id=link_id,
            is_use_permissions=False  # This is a public page
        ) if link_id else None
        
        jobs_filter = Q()
        if job_filters := self.query_params.get('job_filters'):
            job_filters = json.loads(job_filters)
            if job_ids := job_filters.get('job_ids'):
                jobs_filter &= Q(id__in=job_ids)
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
                job_filters.get('remote_type_bit'),
                job_filters.get('range_miles')
            )
        
        no_results_data = {
            'total_page_count': 0,
            'total_employer_job_count': 0,
            'jobs_by_employer': {},
        }
        if job_subscription_ids:
            job_subscriptions = JobSubscriptionView.get_job_subscriptions(subscription_filter=Q(id__in=job_subscription_ids))
            job_subscription_filter = JobSubscriptionView.get_combined_job_subscription_filter(job_subscriptions)
            jobs_filter &= job_subscription_filter
            jobs = EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)
        elif profession_key:
            try:
                taxonomy = TaxonomyJobTitleView.get_job_title_taxonomy(tax_key=profession_key)
            except Taxonomy.DoesNotExist:
                return Response(status=status.HTTP_200_OK, data=no_results_data)
            jobs_filter &= Q(taxonomy__taxonomy=taxonomy)
            jobs = EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)
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
            jobs = EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)
        else:
            jobs = self.get_jobs_from_social_link(link, extra_filter=jobs_filter)
        jobs_by_employer = {}
        if jobs:
            employer_ids = {j.employer_id for j in jobs}
            logger.info('Fetching application requirements')
            application_requirements = EmployerJobApplicationRequirementView.get_application_requirements(
                employer_ids=employer_ids)
            application_requirements_by_employer = defaultdict(list)
            for requirement in application_requirements:
                application_requirements_by_employer[requirement.employer_id].append(requirement)
            
            consolidated_app_requirements_by_employer = {}
            for employer_id, employer_requirements in application_requirements_by_employer.items():
                consolidated_app_requirements_by_employer[
                    employer_id] = EmployerJobApplicationRequirementView.get_consolidated_application_requirements(
                    employer_requirements)
            
            for job in jobs:
                if not (employer_jobs := jobs_by_employer.get(job.employer_id)):
                    employer_jobs = {
                        'employer_id': job.employer_id,
                        'employer_name': job.employer.employer_name,
                        'employer_key': job.employer.employer_key,
                        'employer_logo': job.employer.logo_square_88.url if job.employer.logo_square_88 else None,
                        'is_use_job_url': job.employer.is_use_job_url,
                        'jobs': defaultdict(lambda: defaultdict(list))
                    }
                    jobs_by_employer[job.employer_id] = employer_jobs
                
                serialized_job = get_serialized_employer_job(job)
                serialized_job['application_fields'] = EmployerJobApplicationRequirementView.get_job_application_fields(
                    job, consolidated_app_requirements_by_employer[job.employer_id]
                )
                job_department = job.job_department.name if job.job_department else None
                employer_jobs['jobs'][job_department or 'General'][job.job_title].append(serialized_job)
        
        jobs_by_employer = list(jobs_by_employer.values())
        
        total_jobs = len(jobs)
        start_employer_job_idx = (page_count - 1) * self.EMPLOYERS_PER_PAGE
        
        return Response(status=status.HTTP_200_OK, data={
            'total_page_count': math.ceil(len(jobs_by_employer) / self.EMPLOYERS_PER_PAGE),
            'total_employer_job_count': total_jobs,
            'jobs_by_employer': jobs_by_employer[
                                start_employer_job_idx:start_employer_job_idx + self.EMPLOYERS_PER_PAGE
                                ],
        })
    
    @staticmethod
    def get_jobs_from_social_link(link, extra_filter=None):
        from jvapp.apis.employer import EmployerJobView
        from jvapp.apis.job_subscription import JobSubscriptionView
        
        logger.info('Fetching job filter')
        job_filter = JobSubscriptionView.get_combined_job_subscription_filter(link.job_subscriptions.all())
        if extra_filter:
            job_filter &= extra_filter
        
        logger.info('Fetching jobs')
        return EmployerJobView.get_employer_jobs(employer_job_filter=job_filter)
    
    @staticmethod
    def get_location_filter(location_dict: Union[dict, None], remote_type_bit: int, range_miles: Union[int, None]):
        location_filter = Q()
        remote_type_bit = remote_type_bit or 0
        if location_dict and location_dict.get('city') and range_miles:
            start_point = Location.get_geometry_point(location_dict['latitude'], location_dict['longitude'])
            location_filter &= Q(locations__geometry__within_miles=(start_point, range_miles))
        elif location_dict:
            # If remote is allowed, we only want to filter on country, regardless of whether a state is set
            if (state := location_dict.get('state')) and not remote_type_bit & REMOTE_TYPES.YES.value:
                location_filter &= Q(locations__state__name=state)
            elif country := location_dict.get('country'):
                country_filter = Q(locations__country__name=country)
                if remote_type_bit & REMOTE_TYPES.YES.value:
                    # Some remote jobs don't have a country. In this case, we assume it's a global remote job
                    country_filter |= Q(locations__country__name__isnull=True)
                location_filter &= country_filter
        
        if remote_type_bit and (remote_type_bit == REMOTE_TYPES.NO.value):
            location_filter &= Q(locations__is_remote=False)
        
        if remote_type_bit and (remote_type_bit == REMOTE_TYPES.YES.value):
            location_filter &= Q(locations__is_remote=True)
        
        return location_filter


class SocialLinkPostJobsView(JobVyneAPIView):
    JOB_LOOKBACK_DAYS = 60
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
        jobs_filter &= Q(
            open_date__gte=timezone.now().date() - timedelta(days=SocialLinkPostJobsView.JOB_LOOKBACK_DAYS))
        
        # Don't post jobs that have already been posted
        job_post_filter = Q(job_post__channel=social_channel)
        if recipient_id:
            job_post_filter &= Q(job_post__recipient_id=recipient_id)
        elif owner_id:
            job_post_filter &= Q(job_post__owner_id=owner_id)
        else:
            job_post_filter &= Q(job_post__employer_id=employer_id)
        jobs_filter &= ~job_post_filter
        
        # Make sure we only use one post for a given job title
        # Some employers create a separate post for each location for a specific job
        jobs = {(job.employer_id, job.job_title): job for job in
                EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)}
        jobs = list(jobs.values())
        
        return jobs[:max_job_count]


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
