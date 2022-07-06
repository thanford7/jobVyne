from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.employer import *
from jvapp.permissions.employer import IsAdminOrEmployerOrReadOnlyPermission
from jvapp.serializers.employer import get_serialized_employer, get_serialized_employer_job


class EmployerView(JobVyneAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request, employer_id=None):
        if employer_id:
            employer = self.get_employers(employer_id=employer_id)
            data = get_serialized_employer(employer)
        else:
            employers = self.get_employers(employer_filter=Q())
            data = [get_serialized_employer(e) for e in employers]

        return Response(status=status.HTTP_200_OK, data=data)
    
    @staticmethod
    def get_employers(employer_id=None, employer_filter=None):
        if employer_id:
            employer_filter = Q(id=employer_id)
        
        employers = Employer.objects.select_related('employerSize').filter(employer_filter)
        
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
