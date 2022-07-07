from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.social import *
from jvapp.serializers.social import *
from jvapp.utils.data import set_object_attributes


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
                get_serialized_social_link_filter(lf) for lf
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
        cfg = {'cities': None}
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
            
        if state_ids := data.get('state_ids'):
            link_filter.states.set(state_ids)
            
        if country_ids := data.get('country_ids'):
            link_filter.countries.set(country_ids)
            
        if job_ids := data.get('job_ids'):
            link_filter.jobs.set(job_ids)
            
    @staticmethod
    def get_link_filters(user, link_filter_id=None, link_filter_filter=None):
        if link_filter_id:
            link_filter_filter = Q(id=link_filter_id)
            
        links = SocialLinkFilter.objects\
            .select_related('employer', 'platform')\
            .prefetch_related('departments', 'states', 'countries', 'jobs')\
            .filter(link_filter_filter)
        
        links = SocialLinkFilter.jv_filter_perm(user, links)
        
        if link_filter_id:
            if not links:
                raise SocialLinkFilter.DoesNotExist
            return links[0]
        
        return links