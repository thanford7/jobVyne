import base64
import json
import re
from dataclasses import dataclass
from datetime import date

import requests
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.apis.geocoding import get_location
from jvapp.models import EmployerAts, EmployerJob, JobDepartment
from jvapp.models.abstract import PermissionTypes
from jvapp.models.location import LocationLookup
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.datetime import get_datetime_or_none
from jvapp.utils.response import convert_resp_to_django_resp, is_good_response


@dataclass
class JobData:
    ats_job_key: str
    job_title: str
    job_description: str = None
    open_date: date = None
    close_date: date = None
    department_name: str = None
    employment_type: str = None
    salary_floor: float = None
    salary_ceiling: float = None
    salary_currency_type: str = None
    locations: list = None


def is_response_object(obj):
    return isinstance(obj, requests.Response)


class BaseAts:
    BATCH_SIZE = 500
    
    def __init__(self, ats_cfg):
        self.ats_cfg = ats_cfg
        self.request_headers = self.get_request_headers()
        self.location_lookups = self.get_location_lookups()
        
    def get_request_headers(self):
        return {}
    
    def get_current_jobs(self, employer_id):
        return {
            job.ats_job_key or f'JOBVYNE-{job.id}': job
            for job in EmployerJob.objects.prefetch_related('locations').filter(employer_id=employer_id, close_date__isnull=True)
        }
    
    def get_job_departments(self):
        return {dept.name: dept for dept in JobDepartment.objects.all()}
    
    def get_locations(self):
        pass
    
    def get_location_lookups(self):
        return {l.text: l.location for l in LocationLookup.objects.select_related('location').all()}
    
    def get_or_create_location(self, location_text):
        location = self.location_lookups.get(location_text)
        if not location:
            return get_location(location_text)
        return location
        
    def get_noramlized_job_data(self, job):
        return JobData()  # Override

    def save_jobs(self, employer_id, jobs):
        current_jobs = self.get_current_jobs(employer_id)
        job_departments = self.get_job_departments()
        process_count = 0
        jobs_count = len(jobs)
        JobLocationsModel = EmployerJob.locations.through
        create_jobs = []
        update_jobs = []
        create_job_locations = []
        clear_location_job_ids = []
        now = timezone.now()
        while process_count < jobs_count:
            batch_jobs = jobs[process_count:process_count + self.BATCH_SIZE]
            for job in batch_jobs:
                job_data = self.get_noramlized_job_data(job)
                current_job = current_jobs.get(job_data.ats_job_key) or EmployerJob(
                    employer_id=employer_id,
                    created_dt=now
                )
                current_job.modified_dt = now
                is_new = not bool(current_job.id)
                current_job.ats_job_key = job_data.ats_job_key
                current_job.job_title = job_data.job_title
                current_job.job_description = job_data.job_description
                current_job.open_date = job_data.open_date
                current_job.close_date = job_data.close_date
                job_department = None
                if job_data.department_name and not (job_department := job_departments.get(job_data.department_name)):
                    job_department = JobDepartment(name=job_data.department_name)
                    job_department.save()
                current_job.job_department = job_department
                current_job.employment_type = job_data.employment_type
                current_job.salary_floor = job_data.salary_floor
                current_job.salary_ceiling = job_data.salary_ceiling
                current_job.salary_currency_id = job_data.salary_currency_type
                if (not is_new) and {l.id for l in job_data.locations} != {l.id for l in current_job.locations.all()}:
                    clear_location_job_ids.append(current_job.id)
                    for location in job_data.locations:
                        create_job_locations.append(JobLocationsModel(location=location, employerjob=current_job))
                if is_new:
                    for location in job_data.locations:
                        create_job_locations.append(JobLocationsModel(location=location, employerjob=current_job))
            
                jobs_list = update_jobs if not is_new else create_jobs
                jobs_list.append(current_job)
                process_count += 1
            
            # Create and update jobs
            new_jobs = EmployerJob.objects.bulk_create(create_jobs)
            # Update job id so many to many models can be saved
            # bulk_create returns objects in the same order that they are provided
            for new_job, job in zip(new_jobs, create_jobs):
                job.id = new_job.id
            EmployerJob.objects.bulk_update(update_jobs, EmployerJob.UPDATE_FIELDS)
            
            # Remove and add new locations
            JobLocationsModel.objects.filter(employerjob_id__in=clear_location_job_ids).delete()
            JobLocationsModel.objects.bulk_create(create_job_locations)
            
            create_jobs = []
            update_jobs = []
            create_job_locations = []
            clear_location_job_ids = []
            
        # Close any jobs that weren't created/updated
        close_jobs = EmployerJob.objects.filter(modified_dt__lt=now, ats_job_key__isnull=False)
        for job in close_jobs:
            job.close_date = now.date()
        EmployerJob.objects.bulk_update(close_jobs, ['close_date'])


class GreenhouseAts(BaseAts):
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    jobs_url = 'https://harvest.greenhouse.io/v1/jobs'
    job_posts_url = 'https://harvest.greenhouse.io/v1/job_posts'
    job_stages_url = 'https://harvest.greenhouse.io/v1/job_stages'
    
    def get_paginated_data(self, url, params):
        data = []
        has_next_page = True
        page = 1
        while has_next_page:
            resp = requests.get(
                url,
                headers=self.request_headers,
                params={
                    'page': page,
                    'per_page': 500,
                    **params
                }
            )
            if not is_good_response(resp):
                return resp
            data += self.get_resp_data(resp)
            has_next_page = self.has_next_page(resp, page)
            page += 1
        return data
    
    def get_jobs(self):
        posts = self.get_job_posts()
        if is_response_object(posts):
            return posts
        posts = {post['job_id']: post for post in posts}
        
        jobs = self.get_paginated_data(self.jobs_url, {
            'status': 'open'
        })
        for job in jobs:
            post = posts.get(job['id'])
            if not post:
                continue
            job['content'] = post['content']
            job['questions'] = post['questions']
        return [job for job in jobs if not job['confidential']]
    
    def get_job_posts(self):
        return self.get_paginated_data(
            self.job_posts_url,
            {'active': 'true', 'live': 'true', 'full_content': 'true'}
        )
    
    def get_noramlized_job_data(self, job):
        # TODO: Need to make custom field keys configurable for each employer
        custom_fields = job['custom_fields']
        salary_range = custom_fields.get('salary_range')
        locations = [self.get_or_create_location(office['location']['name']) for office in job['offices']]
        data = JobData(
            ats_job_key=str(job['id']),
            job_title=job['name'],
            job_description=job['content'],
            open_date=self.parse_datetime_str(job['opened_at'], as_date=True),
            close_date=self.parse_datetime_str(job['closed_at'], as_date=True),
            department_name=job['departments'][0]['name'] if job['departments'] else None,
            employment_type=custom_fields.get('employment_type'),
            salary_floor=salary_range.get('min_value') if salary_range else None,
            salary_ceiling=salary_range.get('max_value') if salary_range else None,
            salary_currency_type=salary_range.get('unit') if salary_range else None,
            locations=[l for l in locations if l]
        )
        return data

    def get_request_headers(self):
        encoded_api_key_b = base64.b64encode(f'{self.ats_cfg.api_key}:'.encode())  # Must be in bytes to encode
        encoded_api_key = str(encoded_api_key_b, encoding='utf-8')  # Convert back to string val so it can be concattenated
        return {
            'On-Behalf-Of': self.ats_cfg.email,
            'Authorization': f'Basic {encoded_api_key}'
        }
    
    @staticmethod
    def get_resp_data(resp):
        return json.loads(resp.text)
    
    @staticmethod
    def has_next_page(resp, page):
        if not hasattr(resp, 'links'):
            return False
        last_page_match = re.match('^.*?page=(?P<page>[0-9]+).*?$', resp.links['last']['url'])
        last_page = int(last_page_match.group('page'))
        return page < last_page
    
    def parse_datetime_str(self, dt, as_date=False):
        return get_datetime_or_none(dt, format=self.datetime_format, as_date=as_date)


ats_map = {
    'greenhouse': GreenhouseAts
}


class AtsJobsView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def put(self, request):
        if not (ats_id := self.data.get('ats_id')):
            return Response('An ATS ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        ats_cfg = EmployerAts.objects.get(id=ats_id)
        ats_cfg.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        ats_api = ats_map[ats_cfg.name](ats_cfg)
        
        jobs = ats_api.get_jobs()
        ats_api.save_jobs(ats_cfg.employer_id, jobs)
        
        # If we get a response back, something has gone wrong
        if is_response_object(jobs):
            return convert_resp_to_django_resp(jobs)
        
        return Response(status=status.HTTP_200_OK)
