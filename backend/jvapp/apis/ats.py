import base64
import json
import re

import requests
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import EmployerAts, EmployerJob, JobDepartment
from jvapp.models.abstract import PermissionTypes
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.datetime import get_datetime_or_none
from jvapp.utils.response import convert_resp_to_django_resp, is_good_response


def is_response_object(obj):
    return isinstance(obj, requests.Response)


class BaseAts:
    def __init__(self, ats_cfg):
        self.ats_cfg = ats_cfg
        self.request_headers = self.get_request_headers()
        
    def get_request_headers(self):
        return {}
    
    def get_current_jobs(self, employer_id):
        return {
            job.ats_job_key or f'JOBVYNE-{job.id}': job
            for job in EmployerJob.objects.filter(employer_id=employer_id, close_date__isnull=True)
        }
    
    def get_job_departments(self):
        return {dept.name: dept for dept in JobDepartment.objects.all()}

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

    def save_jobs(self, employer_id, jobs):
        current_jobs = self.get_current_jobs(employer_id)
        job_departments = self.get_job_departments()
        create_jobs = []
        update_jobs = []
        for job in jobs:
            current_job = current_jobs.get(job['id']) or EmployerJob(employer_id=employer_id)
            current_job.ats_job_key = job['id']
            current_job.job_title = job['name']
            current_job.job_description = job['content']
            current_job.open_date = self.parse_datetime_str(job['opened_at'], as_date=True)
            current_job.close_date = self.parse_datetime_str(job['closed_at'], as_date=True)
            job_department_name = job['departments'][0]['name'] if job['departments'] else None
            job_department = None
            if job_department_name and not (job_department := job_departments.get(job_department_name)):
                job_department = JobDepartment(name=job_department_name)
                job_department.save()
            current_job.job_department = job_department
            
            # TODO: Need to make custom fields configurable for each employer
            current_job.employment_type = job['custom_fields'].get('employment_type')
            salary_range = job['custom_fields'].get('salary_range')
            if salary_range:
                current_job.salary_floor = salary_range.get('min_value')
                current_job.salary_ceiling = salary_range.get('max_value')
                current_job.salary_currency_id = salary_range.get('unit')
            # locations
            jobs_list = update_jobs if current_job.id else create_jobs
            jobs_list.append(current_job)
            
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
    
    @staticmethod
    def parse_datetime_str(dt, as_date=False):
        return get_datetime_or_none(dt, format='', as_date=as_date)


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
        
        # If we get a response back, something has gone wrong
        if is_response_object(jobs):
            return convert_resp_to_django_resp(jobs)
        
        return Response(status=status.HTTP_200_OK, data=jobs)
