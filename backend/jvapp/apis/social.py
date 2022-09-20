from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.apis.employer import EmployerJobView, EmployerView
from jvapp.apis.user import UserView
from jvapp.models import JobApplication, PageView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.social import *
from jvapp.serializers.employer import get_serialized_employer, get_serialized_employer_job
from jvapp.serializers.social import *
from jvapp.utils.data import set_object_attributes

__all__ = ('SocialPlatformView', 'SocialLinkFilterView', 'SocialLinkJobsView')


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
            
            data = [
                get_serialized_social_link_filter(lf, is_include_performance=True) for lf
                in self.get_link_filters(self.user, link_filter_filter=q_filter)
            ]
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request):
        newLink = SocialLinkFilter()
        self.create_or_update_link_filter(newLink, self.data, self.user)
        
        # Need to refetch to get associated objects
        newLink = self.get_link_filters(self.user, link_filter_id=newLink.id)
        return Response(status=status.HTTP_200_OK, data=get_serialized_social_link_filter(newLink))
    
    def put(self, request):
        if not (link_filter_id := self.data.get('link_filter_id')):
            return Response('A link filter ID is required', status=status.HTTP_400_BAD_REQUEST)
        link = self.get_link_filters(self.user, link_filter_id=link_filter_id)
        self.create_or_update_link_filter(link, self.data, self.user)

        # Need to refetch to get associated objects
        link = self.get_link_filters(self.user, link_filter_id=link_filter_id)
        return Response(status=status.HTTP_200_OK, data=get_serialized_social_link_filter(link))
    
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
    def create_or_update_link_filter(link_filter, data, user):
        cfg = {}
        if not link_filter.created_dt:
            cfg['owner_id'] = None
            cfg['employer_id'] = None
            cfg['platform_id'] = None
        set_object_attributes(link_filter, data, cfg)
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
            .select_related('employer', 'platform', 'owner')\
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
        profile = UserView.get_user(self.user, user_id=link_filter.owner_id, is_check_permission=False)
        return Response(status=status.HTTP_200_OK, data={
            'total_page_count': paged_jobs.num_pages,
            'jobs': [get_serialized_employer_job(j) for j in paged_jobs.get_page(page_count)],
            'employer': get_serialized_employer(employer),
            'profile': {
                'id': profile.id,
                'profile_picture_url': profile.profile_picture.url if profile.profile_picture else None,
                'first_name': profile.first_name,
                'last_name': profile.last_name
            }
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
