from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.apis.social import SocialLinkView
from jvapp.models import JobVyneUser
from jvapp.models.employer import ConnectionTypeBit
from jvapp.utils.data import coerce_int


class CommunityMemberView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    FILTER_MEMBERS_ALL = 'all'
    FILTER_MEMBERS_JOB_SEEKERS = 'job_seekers'
    FILTER_MEMBERS_HIRING_MANAGERS = 'hiring_managers'
    
    def get(self, request):
        employer_id = self.query_params.get('employer_id')
        profession = self.query_params.get('profession')
        member_type = coerce_int(self.query_params.get('member_type'), default=0)
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
                'job_search_professions',
                'job_connection',
                'job_connection__job',
                'job_connection__job__employer',
                'job_connection__job__locations',
            )
            .filter(user_filter).distinct()
        )
        serialized_members = [self.get_serialized_member(m, member_type) for m in members]
        serialized_members = [m for m in serialized_members if not member_type or (member_type & m['member_type_bits'])]
        serialized_members.sort(key=lambda x: x['id'])
        return Response(status=status.HTTP_200_OK, data=serialized_members)
    
    @staticmethod
    def get_serialized_member(user: JobVyneUser, member_type_filter):
        job_connections = []
        for jc in user.job_connection.all():
            if jc.connection_type == ConnectionTypeBit.NO_CONNECTION:
                continue
            # TODO: This is not performant. Think about how to optimize
            job_link = SocialLinkView.get_or_create_single_job_link(jc.job, owner_id=user.id)
            job_connections.append({
                'is_allow_contact': jc.is_allow_contact,
                'connection_type': jc.connection_type,
                'job_title': jc.job.job_title,
                'job_employer': jc.job.employer.employer_name,
                'job_employer_logo_url': jc.job.employer.logo_square_88.url if jc.job.employer.logo_square_88 else None,
                'job_location': jc.job.locations_text,
                'is_job_remote': jc.job.is_remote,
                'job_url': job_link.get_link_url()
            })
        job_connections.sort(key=lambda x: (x['connection_type'], x['job_title']))
        member_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'linkedin_url': user.linkedin_url,
            'professional_site_url': user.professional_site_url,
            'profile_picture_url': user.profile_picture.url if user.profile_picture else None,
            'member_type_bits': 0,
            'job_connections': job_connections
        }
        
        if user.employer:
            member_data['employer_name'] = user.employer.employer_name
            member_data['employer_logo_url'] = user.employer.logo.url if user.employer.logo else None
        
        if user.is_hiring_manager:
            member_data['member_type_bits'] |= JobVyneUser.MEMBER_TYPE_HIRING_MGR
            
        if all((
            not (member_type_filter & JobVyneUser.MEMBER_TYPE_HIRING_MGR),
            user.is_job_search_visible,
            user.job_search_type_bit & (JobVyneUser.JOB_SEARCH_TYPE_ACTIVE | JobVyneUser.JOB_SEARCH_TYPE_PASSIVE)
        )):
            member_data['member_type_bits'] |= JobVyneUser.MEMBER_TYPE_JOB_SEEKER
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
            
        if user.is_can_contact:
            member_data['email'] = user.email
            
        return member_data
