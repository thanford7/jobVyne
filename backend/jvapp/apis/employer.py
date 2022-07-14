from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models.abstract import PermissionTypes
from jvapp.models.employer import *
from jvapp.models.employer import EmployerAuthGroup
from jvapp.models.user import USER_MANAGEMENT_PERMISSIONS
from jvapp.permissions.employer import IsAdminOrEmployerOrReadOnlyPermission, IsAdminOrEmployerPermission
from jvapp.serializers.employer import get_serialized_auth_group, get_serialized_employer, get_serialized_employer_job


class EmployerView(JobVyneAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request, employer_id=None):
        if employer_id:
            employer = self.get_employers(employer_id=employer_id)
            can_view_users = self.user.has_employer_permission(USER_MANAGEMENT_PERMISSIONS, is_all_true=False)
            data = get_serialized_employer(employer)
        else:
            employers = self.get_employers(employer_filter=Q())
            data = [get_serialized_employer(e) for e in employers]

        return Response(status=status.HTTP_200_OK, data=data)
    
    @staticmethod
    def get_employers(employer_id=None, employer_filter=None):
        if employer_id:
            employer_filter = Q(id=employer_id)
        
        employers = Employer.objects\
            .select_related('employerSize')\
            .prefetch_related('employee', 'employee__permission_groups')\
            .filter(employer_filter)
        
        if employer_id:
            if not employers:
                raise Employer.DoesNotExist
            return employers[0]
        
        return employers


class EmployerJobView(JobVyneAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request, employer_job_id=None):
        if employer_job_id:
            job = self.get_employer_jobs(employer_job_id=employer_job_id)
            data = get_serialized_employer_job(job)
        elif employer_id := self.query_params.get('employer_id'):
            employer_id = employer_id[0]
            job_filter = Q(employer_id=employer_id)
            jobs = self.get_employer_jobs(employer_job_filter=job_filter)
            data = [get_serialized_employer_job(j) for j in jobs]
        else:
            return Response('A job ID or employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    @staticmethod
    def get_employer_jobs(employer_job_id=None, employer_job_filter=None):
        if employer_job_id:
            employer_job_filter = Q(id=employer_job_id)
        
        jobs = EmployerJob.objects\
            .select_related(
                'jobDepartment',
                'state',
                'country'
            )\
            .filter(employer_job_filter)
        
        if employer_job_id:
            if not jobs:
                raise EmployerJob.DoesNotExist
            return jobs[0]
        
        return jobs


class EmployerAuthGroupView(JobVyneAPIView):
    
    permission_classes = [IsAdminOrEmployerPermission]
    
    def get(self, request):
        auth_groups = self.get_auth_groups(employer_id=self.user.employer_id)
        return Response(
            status=status.HTTP_200_OK,
            data=[get_serialized_auth_group(ag) for ag in auth_groups]
        )
    
    @atomic
    def post(self, request):
        auth_group = EmployerAuthGroup(
            name=self.data['name'],
            employer_id=self.data['employer_id']
        )
        auth_group.jv_check_permission(PermissionTypes.CREATE.value, self.user)
        auth_group.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: f'{auth_group.name} group saved'
            }
        )
        
    
    @staticmethod
    def get_auth_groups(auth_group_filter=None, employer_id=None):
        auth_group_filter = auth_group_filter or Q()
        if employer_id:
            auth_group_filter &= (Q(employer_id=employer_id) | Q(employer_id__isnull=True))
        return EmployerAuthGroup.objects.prefetch_related('permissions').filter(auth_group_filter)
    
    
