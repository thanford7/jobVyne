__all__ = ['JobsView']

import json

from django.core.paginator import Paginator
from django.db.models import F, Q
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.apis.employer import EmployerJobView
from jvapp.models.employer import Employer
from jvapp.serializers.employer import get_serialized_employer_job
from jvapp.serializers.location import get_serialized_location
from jvapp.utils.data import coerce_bool


class JobsView(JobVyneAPIView):
    
    DEFAULT_SORT_ORDER = ('-open_date', 'employer__employer_name', 'job_department__name', 'job_title')
    SORT_MAP = {
        'employer_name': ('employer__employer_name', ),
        'job_department': ('job_department__name', ),
        'job_title': ('job_title', ),
        'employment_type': ('employment_type', )
    }
    
    def get(self, request):
        pagination = json.loads(self.query_params['pagination'])
        filter_params = json.loads(self.query_params['filterParams'])
        
        # Only grab employers (not professional organizations or agencies)
        employer_filter = Q(organization_type=1 * F('organization_type').bitand(Employer.ORG_TYPE_EMPLOYER))
        employers = Employer.objects.filter(employer_filter)
        
        raw_sort_order = pagination['sortBy']
        if not raw_sort_order:
            sort_order = self.DEFAULT_SORT_ORDER
        else:
            sort_keys = self.SORT_MAP[raw_sort_order]
            is_descending = coerce_bool(pagination['descending'])
            sort_order = []
            for key in sort_keys:
                sort_order.append(f'{"-" if is_descending else ""}{key}')
        
        # Filter jobs
        job_filter = Q()
        if employer_ids := filter_params.get('employers'):
            job_filter &= Q(employer_id__in=employer_ids)
        if job_department_ids := filter_params.get('job_departments'):
            job_filter &= Q(job_department_id__in=job_department_ids)
        if job_title := filter_params.get('job_title'):
            job_filter &= Q(job_title__iregex=f'^.*{job_title}.*$')
        if location_ids := filter_params.get('locations'):
            job_filter &= Q(locations_id__in=location_ids)
        if employment_types_filter := filter_params.get('employment_types'):
            job_filter &= Q(employment_type__in=employment_types_filter)
        jobs, paginated_jobs = EmployerJobView.get_employer_jobs(
            job_filter, order_by=sort_order, jobs_per_page=pagination['rowsPerPage'], page_count=pagination['page'],
        )

        return Response(status=status.HTTP_200_OK, data={
            'total_page_count': paginated_jobs.num_pages,
            'total_job_count': paginated_jobs.count,
            'jobs': [get_serialized_employer_job(job) for job in jobs],
            'employers': sorted([{
                'id': e.id,
                'name': e.employer_name
            } for e in employers], key=lambda x: x['name'])
        })
    