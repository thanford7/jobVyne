from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, WARNING_MESSAGES_KEY
from jvapp.apis.employer import EmployerJobView, EmployerView
from jvapp.models import JobApplication, Message, PageView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.social import *
from jvapp.serializers.employer import get_serialized_employer, get_serialized_employer_job
from jvapp.serializers.social import *
from jvapp.utils.data import AttributeCfg, set_object_attributes

__all__ = ('SocialPlatformView', 'SocialLinkFilterView', 'SocialLinkJobsView', 'ShareSocialLinkView')

from jvapp.utils.email import send_django_email
from jvapp.utils.sanitize import sanitize_html


class SocialPlatformView(JobVyneAPIView):
    
    def get(self, request):
        data = [get_serialized_social_platform(sp) for sp in SocialPlatform.objects.all()]
        return Response(status=status.HTTP_200_OK, data=data)
    
    
class SocialLinkFilterView(JobVyneAPIView):
    
    def get(self, request, link_filter_id=None):
        if link_filter_id:
            data = get_serialized_social_link_filter(self.get_link_filters(self.user, link_filter_id=link_filter_id))
        else:
            if owner_id := self.query_params.get('owner_id'):
                q_filter = Q(owner_id=owner_id)
            elif employer_id := self.query_params.get('employer_id'):
                q_filter = Q(employer_id=employer_id)
            else:
                return Response('You must provide an ID, owner ID, or employer ID', status=status.HTTP_400_BAD_REQUEST)
            
            data = []
            for link_filter in self.get_link_filters(self.user, link_filter_filter=q_filter):
                serialized_link_filter = get_serialized_social_link_filter(link_filter, is_include_performance=True)
                # Only fetch job count for specific user because a database call
                # is required per link_filter and is not performant
                if owner_id:
                    serialized_link_filter['jobs_count'] = len(SocialLinkJobsView.get_jobs_from_filter(link_filter))
                data.append(serialized_link_filter)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request):
        new_link = SocialLinkFilter()
        new_link, is_duplicate = self.create_or_update_link_filter(new_link, self.data, self.user)
        is_get_or_create = self.data.get('is_get_or_create')
        data = {}
        # Sometimes we want to silently get or create a link (e.g. when a user is sharing an individual job)
        if not is_get_or_create:
            if is_duplicate and not self.data.get('is_default'):
                data = {
                    WARNING_MESSAGES_KEY: ['A referral link with these filters already exists']
                }
            elif is_duplicate:
                data = {
                    SUCCESS_MESSAGE_KEY: 'A referral link with these filters already exists. The default property was updated'
                }
            else:
                data = {
                    SUCCESS_MESSAGE_KEY: 'Created a new referral link'
                }
        if is_get_or_create:
            data['link_filter'] = get_serialized_social_link_filter(new_link)
        else:
            data['id'] = new_link.id
        return Response(status=status.HTTP_200_OK, data=data)
    
    def put(self, request):
        if not (link_filter_id := self.data.get('link_filter_id')):
            return Response('A link filter ID is required', status=status.HTTP_400_BAD_REQUEST)
        link = self.get_link_filters(self.user, link_filter_id=link_filter_id)
        self.create_or_update_link_filter(link, self.data, self.user)

        # Need to refetch to get associated objects
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'The referral link was successfully updated'
        })
    
    @atomic
    def delete(self, request):
        link_filter_id = self.data.get('link_filter_id')
        link_filter_ids = [link_filter_id] if link_filter_id else self.data.get('link_filter_ids')
        if not link_filter_ids:
            return Response('A link filter ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        links = self.get_link_filters(self.user, link_filter_filter=Q(id__in=link_filter_ids))
        deleted_link_ids = []
        for link in links:
            link.jv_check_permission(PermissionTypes.DELETE.value, self.user)
            deleted_link_ids.append(link.id)
            link.delete()
        
        return Response(status=status.HTTP_200_OK, data=deleted_link_ids)
        
    @staticmethod
    @atomic
    def create_or_update_link_filter(link_filter, data, user=None):
        """ Create or update a link filter.
        :return {bool}: If True, the link filter is a duplicate
        """
        # Add owner and employer for new link
        cfg = {
            'is_default': AttributeCfg(is_ignore_excluded=True)
        }
        is_new = not link_filter.created_dt
        is_duplicate = False
        if is_new:
            cfg = {
                'owner_id': None,
                'employer_id': None,
                **cfg
            }
            
        set_object_attributes(link_filter, data, cfg)
        
        if user:
            permission_type = PermissionTypes.EDIT.value if link_filter.id else PermissionTypes.CREATE.value
            link_filter.jv_check_permission(permission_type, user)
        link_filter.save()
        
        if department_ids := data.get('department_ids'):
            link_filter.departments.set(department_ids)
            
        if city_ids := data.get('city_ids'):
            link_filter.cities.set(city_ids)
            
        if state_ids := data.get('state_ids'):
            link_filter.states.set(state_ids)
            
        if country_ids := data.get('country_ids'):
            link_filter.countries.set(country_ids)
            
        if job_ids := data.get('job_ids'):
            link_filter.jobs.set(job_ids)
        
        existing_filters = SocialLinkFilterView.get_user_existing_filters(
            user, link_filter.owner_id, current_link_filter_id=link_filter.id
        )
        
        # Remove default flag from previous filters
        if link_filter.is_default:
            for filter in existing_filters.values():
                if filter.is_default:
                    filter.is_default = False
                    filter.save()

        # Make sure this isn't a duplicate filter
        existing_filter = existing_filters.get(link_filter.get_unique_key())
        if existing_filter:
            # If this is a new filter, we don't have to worry about FK associations (e.g. job applications) and
            # can just delete the new filter to prevent a duplicate
            if is_new:
                existing_filter.is_default = link_filter.is_default
                existing_filter.is_primary = link_filter.is_primary
                existing_filter.save()
                link_filter.delete()
            else:
                raise ValueError('A referral link with these filters already exists')
            is_duplicate = True
        
        return (existing_filter or link_filter), is_duplicate
    
    @staticmethod
    def get_user_existing_filters(user, owner_id, current_link_filter_id=None):
        return {
            f.get_unique_key(): f for f in
            SocialLinkFilterView.get_link_filters(
                user, link_filter_filter=Q(owner_id=owner_id), is_use_permissions=False
            ) if (f.id != current_link_filter_id or not current_link_filter_id)
        }
            
    @staticmethod
    def get_link_filters(
            user, link_filter_id=None, link_filter_filter=None, start_dt=None, end_dt=None, is_use_permissions=True
    ):
        if link_filter_id:
            link_filter_filter = Q(id=link_filter_id)

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
            
        links = SocialLinkFilter.objects\
            .select_related('employer', 'owner')\
            .prefetch_related(
                'departments', 'cities', 'states', 'countries', 'jobs',
                app_prefetch, page_view_prefetch
            )\
            .filter(link_filter_filter)
        
        if is_use_permissions:
            links = SocialLinkFilter.jv_filter_perm(user, links)
        
        if link_filter_id:
            if not links:
                raise SocialLinkFilter.DoesNotExist
            return links[0]
        
        return links
    
    
class SocialLinkJobsView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, link_filter_id):
        page_count = self.query_params.get('page_count', 1)
        link_filter = SocialLinkFilterView.get_link_filters(
            self.user,
            link_filter_id=link_filter_id,
            is_use_permissions=False  # This is a public page
        )
        jobs = self.get_jobs_from_filter(link_filter)
        paged_jobs = Paginator(jobs, per_page=5)
        employer = EmployerView.get_employers(employer_id=link_filter.employer_id)
        return Response(status=status.HTTP_200_OK, data={
            'total_page_count': paged_jobs.num_pages,
            'jobs': [get_serialized_employer_job(j) for j in paged_jobs.get_page(page_count)],
            'employer': get_serialized_employer(employer),
            'owner_id': link_filter.owner_id,
            'is_active_employee': link_filter.owner.is_active_employee
        })
        
    @staticmethod
    def get_jobs_from_filter(link_filter):
        jobs_filter = Q(employer_id=link_filter.employer_id)
        jobs_filter &= Q(open_date__lte=timezone.now().date())
        
        if len(link_filter.departments.all()):
            jobs_filter &= Q(job_department_id__in=[d.id for d in link_filter.departments.all()])
            
        if len(link_filter.cities.all()):
            jobs_filter &= Q(locations__city_id__in=[c.id for c in link_filter.cities.all()])
            
        if len(link_filter.states.all()):
            jobs_filter &= Q(locations__state_id__in=[s.id for s in link_filter.states.all()])
            
        if len(link_filter.countries.all()):
            jobs_filter &= Q(locations__country_id__in=[c.id for c in link_filter.countries.all()])
            
        if len(link_filter.jobs.all()):
            jobs_filter &= Q(id__in=[j.id for j in link_filter.jobs.all()])
            
        return EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)
    
    
class ShareSocialLinkView(JobVyneAPIView):
    
    def post(self, request):
        job_link = SocialLinkFilterView.get_link_filters(self.user, link_filter_id=self.data['socialLinkId'])
        if self.user.id != job_link.owner_id:
            return Response('You do not have access to this job link', status=status.HTTP_401_UNAUTHORIZED)
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
