import logging

from django.db.models import Prefetch, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import JobVyneUser
from jvapp.models.employer import ConnectionTypeBit, EmployerConnection
from jvapp.utils.data import coerce_int

logger = logging.getLogger(__name__)


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
            
        employer_connections_prefetch = Prefetch(
            'employer_connection',
            queryset=(
                EmployerConnection.objects
                .select_related('employer')
            )
        )

        members = (
            JobVyneUser.objects
            .select_related(
                'employer'
            )
            .prefetch_related(
                'job_search_levels',
                'job_search_industries',
                'job_search_professions',
                employer_connections_prefetch
            )
            .filter(user_filter).distinct()
        )
        
        logger.info('Fetching community members')
        serialized_members = [self.get_serialized_member(m, member_type) for m in members]
        serialized_members = [m for m in serialized_members if not member_type or (member_type & m['member_type_bits'])]
        serialized_members.sort(key=lambda x: x['id'], reverse=True)
        return Response(status=status.HTTP_200_OK, data=serialized_members)
    
    @staticmethod
    def get_employer_connection_text(employer_connections, employer_limit=4):
        filtered_connections = {}
        has_more = False
        for employer_connection in employer_connections:
            if filtered_connections.get(employer_connection['employer_name']):
                continue
            filtered_connections[employer_connection['employer_name']] = employer_connection['connection_type']
            if len(filtered_connections) == employer_limit:
                has_more = True
                break
        connection_text = ', '.join([
            f'{name}{" (hiring team)" if connection_type == ConnectionTypeBit.HIRING_MEMBER.value else ""}'
            for name, connection_type in filtered_connections.items()
        ])
        if has_more:
            connection_text += ', and more...'
            
        return connection_text
            
            
    
    @staticmethod
    def get_serialized_member(user: JobVyneUser, member_type_filter):
        employer_connections = []
        for ec in user.employer_connection.all():
            if ec.connection_type == ConnectionTypeBit.NO_CONNECTION.value:
                continue
            employer_connections.append({
                'employer_name': ec.employer.employer_name,
                'connection_type': ec.connection_type,
            })
        employer_connections.sort(key=lambda x: (x['connection_type'], x['employer_name']))
        member_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'linkedin_url': user.linkedin_url,
            'professional_site_url': user.professional_site_url,
            'profile_picture_url': user.profile_picture.url if user.profile_picture else None,
            'member_type_bits': 0,
            'employer_connection_count': len(set([ec['employer_name'] for ec in employer_connections])),
            'employer_connection_text': CommunityMemberView.get_employer_connection_text(employer_connections)
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
            member_data['job_search_levels'] = sorted([
                {'id': l.id, 'name': l.name, 'order': l.sort_order} for l in user.job_search_levels.all()
            ], key=lambda x: x['order']) if user.job_search_levels.all() else None
            member_data['job_search_industries'] = [
                {'id': i.id, 'name': i.name} for i in user.job_search_industries.all()
            ] if user.job_search_industries.all() else None
            member_data['job_search_professions'] = [
                {'id': p.id, 'name': p.name} for p in user.job_search_professions.all()
            ] if user.job_search_professions.all() else None
            member_data['job_search_qualifications'] = user.job_search_qualifications
            
        if user.is_can_contact:
            member_data['email'] = user.contact_email
            
        return member_data
