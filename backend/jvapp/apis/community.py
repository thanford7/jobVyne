from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.apis.user import UserView
from jvapp.models import JobVyneUser



class CommunityMemberView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    FILTER_MEMBERS_ALL = 'all'
    FILTER_MEMBERS_JOB_SEEKERS = 'job_seekers'
    FILTER_MEMBERS_HIRING_MANAGERS = 'hiring_managers'
    
    def get(self, request):
        employer_id = self.query_params.get('employer_id')
        profession = self.query_params.get('profession')
        assert any((employer_id, profession))
        
        if employer_id:
            user_filter = Q(membership_groups__id=employer_id) | Q(membership_employers__id=employer_id)
        else:
            user_filter = Q(membership_professions__key=profession)

        members = (
            JobVyneUser.objects
            .select_related(
                'employer',
                'job_search_level'
            )
            .prefetch_related(
                'job_search_industries',
                'job_search_professions'
            )
            .filter(user_filter).distinct()
        )
        return Response(status=status.HTTP_200_OK, data=[self.get_serialized_member(m) for m in members])
    
    @staticmethod
    def get_serialized_member(user: JobVyneUser, can_contact=False):
        member_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'linkedin_url': user.linkedin_url,
            'professional_site_url': user.professional_site_url,
            'profile_picture_url': user.profile_picture.url if user.profile_picture else None,
            'member_type': 'Community member'
        }
        
        if user.employer:
            member_data['employer_name'] = user.employer.employer_name
            member_data['employer_logo_url'] = user.employer.logo.url if user.employer.logo else None
            
        if user.is_job_search_visible and (user.job_search_type_bit & (JobVyneUser.JOB_SEARCH_TYPE_ACTIVE | JobVyneUser.JOB_SEARCH_TYPE_PASSIVE)):
            member_data['member_type'] = 'Job seeker'
            member_data['search_type'] = user.job_search_type_bit
            member_data['job_search_level'] = {
                'id': user.job_search_level.id,
                'level': user.job_search_level.name
            } if user.job_search_level else None
            member_data['job_search_industries'] = [
                {'id': i.id, 'name': i.name} for i in user.job_search_industries.all()
            ] if user.job_search_industries.all() else None
            member_data['job_search_professions'] = [
                {'id': p.id, 'name': p.name} for p in user.job_search_professions.all()
            ] if user.job_search_professions.all() else None
            member_data['job_search_qualifications'] = user.job_search_qualifications
            
        # TODO: Add data for hiring managers
        
        if can_contact:
            member_data['email'] = user.email
            
        return member_data
