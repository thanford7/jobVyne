import csv
import logging
import re
from io import StringIO

from django.db.models import Prefetch, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_error_response, get_success_response
from jvapp.apis.admin import AdminUserConnectionsView
from jvapp.models import JobVyneUser
from jvapp.models.employer import ConnectionTypeBit, EmployerConnection, EmployerJob, JobTaxonomy, Taxonomy
from jvapp.models.user import UserConnection
from jvapp.utils.data import coerce_int, get_text_without_emojis
from jvapp.utils.taxonomy import TAXONOMY_PROFESSION_TA, get_standardized_job_taxonomy

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
                .select_related('employer').filter(~Q(connection_type=ConnectionTypeBit.NO_CONNECTION.value))
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
        serialized_members.sort(key=lambda x: x['joined_dt'], reverse=True)
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
            'user_key': user.user_key,
            'joined_dt': user.created_dt,
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
    
    
class JobConnectionsView(JobVyneAPIView):
    
    def get(self, request):
        job_id = coerce_int(self.query_params.get('job_id'))
        user_id = coerce_int(self.query_params.get('user_id'))
        if not any((job_id, user_id)):
            return get_error_response('A job ID or user ID is required')
        
        if job_id:
            employer_connections_prefetch = Prefetch(
                'employer__user_connection',
                queryset=(
                    EmployerConnection.objects
                    .select_related('user', 'user__profession')
                    .prefetch_related('hiring_jobs')
                    .filter(~Q(connection_type=ConnectionTypeBit.NO_CONNECTION.value) & ~Q(user_id=self.user.id))
                ),
                to_attr='employer_connections'
            )
            user_connections_prefetch = Prefetch(
                'employer__connection',
                queryset=(
                    UserConnection.objects
                    .select_related('profession', 'employer', 'connection_user')
                    .all()
                ),
                to_attr='user_connections'
            )
            
            job = (
                EmployerJob.objects
                .prefetch_related(employer_connections_prefetch, user_connections_prefetch, 'taxonomy')
                .get(id=job_id)
            )
            employer_connections = [
                JobConnectionsView.get_serialized_employer_connection(ec, job, job.profession) for ec in job.employer.employer_connections
            ]
            user_connections = [
                JobConnectionsView.get_serialized_user_connection(uc, job_profession=job.profession) for uc in job.employer.user_connections
            ]
            
            all_connections = employer_connections + user_connections
            all_connections.sort(key=lambda x: (-x['is_same_profession'], x['connection_type']))
        
            return Response(status=status.HTTP_200_OK, data=all_connections)
        if user_id:
            user_connections = [
                JobConnectionsView.get_serialized_user_connection(uc) for uc in
                UserConnection.objects.select_related('profession', 'employer').filter(owner_id=user_id)
            ]
            return Response(status=status.HTTP_200_OK, data=user_connections)
    
    def post(self, request):
        raw_file = self.files['connections_file'][0]
        csv_text = raw_file.read().decode('utf-8')
        employer_map = AdminUserConnectionsView.get_employer_map()
        current_connections = {
            (conn.linkedin_handle, conn.employer_raw): conn for conn in UserConnection.objects.filter(owner=self.user)
        }
        with StringIO(csv_text) as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read())
            csv_file.seek(0)
            reader = csv.reader(csv_file, dialect=dialect)
            headers = []
            # Find the header row and get the values
            for row in reader:
                if (not row) or (row[0].lower() != 'first name'):
                    continue
                for cell in row:
                    headers.append('_'.join([x.lower() for x in cell.split(' ')]))
                break
            
            new_user_connections = []
            for row in reader:
                value_map = {header: val for (header, val) in zip(headers, row)}
                if not all((value_map['company'], value_map['first_name'])):
                    continue
                linkedin_url_match = re.match('^.*?linkedin.com/in/(?P<handle>.+?)$', value_map['url'])
                linkedin_handle = linkedin_url_match.group('handle')
                employer_raw = value_map['company']
                if existing_connection := current_connections.get((linkedin_handle, employer_raw)):
                    continue
                
                connection_user = None
                if email := value_map.get('email'):
                    try:
                        connection_user = JobVyneUser.objects.get(Q(email=email) | Q(business_email=email))
                    except JobVyneUser.DoesNotExist:
                        pass
                
                user_connection = UserConnection(
                    owner=self.user,
                    connection_user=connection_user,
                    first_name=get_text_without_emojis(value_map['first_name']),
                    last_name=get_text_without_emojis(value_map['last_name']),
                    email=email,
                    linkedin_handle=linkedin_url_match.group('handle'),
                    employer_raw=employer_raw,
                    employer_id=employer_map.get(employer_raw.lower()),
                    job_title=value_map['position'],
                    profession=get_standardized_job_taxonomy(value_map['position']),
                    created_dt=timezone.now(),
                    modified_dt=timezone.now()
                )
                new_user_connections.append(user_connection)
                current_connections[(user_connection.linkedin_handle, user_connection.employer_raw)] = user_connection
            UserConnection.objects.bulk_create(new_user_connections, ignore_conflicts=True)
        return get_success_response('Imported LinkedIn contacts')
    
    @staticmethod
    def get_serialized_employer_connection(employer_connection, job, job_profession):
        connection_type = employer_connection.connection_type
        is_hiring_team = job.id in [j.id for j in employer_connection.hiring_jobs.all()]
        if connection_type == ConnectionTypeBit.CURRENT_EMPLOYEE.value and is_hiring_team:
            connection_type = ConnectionTypeBit.HIRING_MEMBER.value
            
        is_same_profession = False
        if job_profession and employer_connection.user.profession:
            is_same_profession = job_profession.id == employer_connection.user.profession.id
        
        return {
            'connection_type': connection_type,
            'full_name': employer_connection.user.full_name,
            'user_key': employer_connection.user.user_key,
            'linkedin_url': employer_connection.user.linkedin_url,
            'is_same_profession': is_same_profession,
            'profession': {
                'name': employer_connection.user.profession.name,
                'key': employer_connection.user.profession.key,
            } if employer_connection.user.profession else None
        }
    
    @staticmethod
    def get_serialized_user_connection(user_connection, job_profession=None):
        user_connection_data = {
            'connection_type': ConnectionTypeBit.CURRENT_EMPLOYEE.value,
            'full_name': user_connection.full_name,
            'connection_user_key': user_connection.connection_user.user_key if user_connection.connection_user else None,
            'owner': {
                'user_key': user_connection.owner.user_key,
                'full_name': user_connection.owner.full_name
            },
            'linkedin_url': f'https://www.linkedin.com/in/{user_connection.linkedin_handle}',
            'job_title': user_connection.job_title,
            'profession': {
                'name': user_connection.profession.name,
                'key': user_connection.profession.key,
            } if user_connection.profession else None,
            'is_ta': user_connection.profession.key == TAXONOMY_PROFESSION_TA if user_connection.profession else False,
            'employer_raw': user_connection.employer_raw,
            'employer': {
                'name': user_connection.employer.employer_name,
                'key': user_connection.employer.employer_key
            } if user_connection.employer else None
        }
        
        if job_profession:
            is_same_profession = False
            if job_profession and user_connection.profession:
                is_same_profession = job_profession.id == user_connection.profession.id
            user_connection_data['is_same_profession'] = is_same_profession
            
        return user_connection_data
