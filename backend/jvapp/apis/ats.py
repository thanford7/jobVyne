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
from jvapp.utils.response import is_good_response
from jvapp.utils.sanitize import get_replace_tag_html, make_links_secure, sanitizer


class AtsError(Exception):
    pass


def get_resp_error_message(resp):
    return f'({resp.status_code}) {resp.text}'


def get_base64_encoded_str(text):
    # Must be in bytes to encode
    if not isinstance(text, bytes):
        text = text.encode()
    encoded_text = base64.b64encode(text)
    return str(encoded_text, encoding='utf-8')  # Convert back to string val


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
    JOBVYNE_TAG = 'JOBVYNE'
    
    def __init__(self, ats_cfg):
        self.ats_cfg = ats_cfg
        self.location_lookups = self.get_location_lookups()
        self.ats_user_id = self.get_ats_user_id()
    
    def get_request_headers(self):
        return {}
    
    @staticmethod
    def get_resp_data(resp):
        return json.loads(resp.text)
    
    def get_current_jobs(self, employer_id):
        return {
            job.ats_job_key or f'JOBVYNE-{job.id}': job
            for job in
            EmployerJob.objects.prefetch_related('locations').filter(employer_id=employer_id, close_date__isnull=True)
        }
    
    def get_job_departments(self):
        return {dept.name.lower(): dept for dept in JobDepartment.objects.all()}
    
    def get_locations(self):
        pass
    
    def get_location_lookups(self):
        return {l.text: l.location for l in LocationLookup.objects.select_related('location').all()}
    
    def get_or_create_location(self, location_text):
        location = self.location_lookups.get(location_text)
        if not location:
            return get_location(location_text)
        return location
    
    def get_referrer_name_from_application(self, application):
        referrer = application.social_link_filter.owner
        return f'{referrer.first_name} {referrer.last_name}'
    
    def get_job_title_from_application(self, application):
        return application.employer_job.job_title
    
    def get_ats_user_id(self):
        raise NotImplementedError()
    
    def get_custom_fields(self):
        raise NotImplementedError()
    
    def get_noramlized_job_data(self, job):
        raise NotImplementedError()
    
    def get_job_stages(self):
        raise NotImplementedError()
    
    def create_application(self, application):
        raise NotImplementedError()
    
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
                if job_data.job_description:
                    current_job.job_description = get_replace_tag_html(
                        sanitizer.clean(job_data.job_description),
                        {'h1': 'h6', 'h2': 'h6', 'h3': 'h6', 'h4': 'h6', 'h5': 'h6'}
                    )
                    current_job.job_description = make_links_secure(current_job.job_description)
                else:
                    current_job.job_description = None
                current_job.open_date = job_data.open_date
                current_job.close_date = job_data.close_date
                job_department = None
                if job_data.department_name and not (job_department := job_departments.get(job_data.department_name.lower())):
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
    candidates_url = 'https://harvest.greenhouse.io/v1/candidates'
    custom_fields_url = 'https://harvest.greenhouse.io/v1/custom_fields/job'
    jobs_url = 'https://harvest.greenhouse.io/v1/jobs'
    job_posts_url = 'https://harvest.greenhouse.io/v1/job_posts'
    job_stages_url = 'https://harvest.greenhouse.io/v1/job_stages'
    users_url = 'https://harvest.greenhouse.io/v1/users'
    
    def get_paginated_data(self, url, params):
        data = []
        has_next_page = True
        page = 1
        while has_next_page:
            resp = requests.get(
                url,
                headers=self.get_request_headers(),
                params={
                    'page': page,
                    'per_page': 500,
                    **params
                }
            )
            if not is_good_response(resp):
                raise AtsError(f'Could not fetch data: {get_resp_error_message(resp)}')
            data += self.get_resp_data(resp)
            has_next_page = self.has_next_page(resp, page)
            page += 1
        return data
    
    def get_data(self, url, params):
        resp = requests.get(
            url,
            headers=self.get_request_headers(),
            params=params
        )
        if not is_good_response(resp):
            raise AtsError(f'Could not fetch data: {get_resp_error_message(resp)}')
        return self.get_resp_data(resp)
    
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
    
    def get_job_stages(self):
        return self.get_paginated_data(self.job_stages_url, {})
    
    def get_noramlized_job_data(self, job):
        custom_fields = job['custom_fields']
        employment_type_key = self.ats_cfg.employment_type_field_key or 'employment_type'
        salary_range_key = self.ats_cfg.salary_range_field_key or 'salary_range'
        salary_range = custom_fields.get(salary_range_key)
        locations = [self.get_or_create_location(office['location']['name']) for office in job['offices']]
        data = JobData(
            ats_job_key=str(job['id']),
            job_title=job['name'],
            job_description=job.get('content', ''),
            open_date=self.parse_datetime_str(job['opened_at'], as_date=True),
            close_date=self.parse_datetime_str(job['closed_at'], as_date=True),
            department_name=job['departments'][0]['name'] if job['departments'] else None,
            employment_type=custom_fields.get(employment_type_key),
            salary_floor=salary_range.get('min_value') if salary_range else None,
            salary_ceiling=salary_range.get('max_value') if salary_range else None,
            salary_currency_type=salary_range.get('unit') if salary_range else None,
            locations=[l for l in locations if l]
        )
        return data

    def get_custom_fields(self):
        return self.get_data(self.custom_fields_url, {})
        
    def create_application(self, application):
        # Check whether candidate exists
        candidates = self.get_paginated_data(self.candidates_url, {'email': application.email})
        resume = get_base64_encoded_str(application.resume.open('rb').read()) if application.resume else None
        ats_job_key = application.employer_job.ats_job_key
        application_data = {
            'job_id': ats_job_key,
            'referrer': {
                'type': 'id',
                'value': self.ats_user_id
            },
            'initial_stage_id': self.get_initial_job_application_stage_id(ats_job_key),
            'attachments': [{
                'filename': application.resume.name.split('/')[-1],
                'type': 'resume',
                'content': resume,
                'content_type': 'multipart/form-data'
            }] if resume else []
        }
        
        if candidates:
            candidate = candidates[0]
            url = f'{self.candidates_url}/{candidate["id"]}/applications'
            resp = requests.post(
                url,
                headers=self.get_request_headers(is_user_id=True),
                json=application_data
            )
            if not is_good_response(resp):
                raise AtsError(f'Could not save candidate: {get_resp_error_message(resp)}')
            candidate_data = self.get_resp_data(resp)
            ats_candidate_key = str(candidate_data['candidate_id'])
            ats_application_key = str(candidate_data['id'])
        else:
            post_data = {
                'first_name': application.first_name,
                'last_name': application.last_name,
                'email_addresses': [{
                    'value': application.email,
                    'type': 'personal'
                }],
                'phone_numbers': [{
                    'value': application.phone_number,
                    'type': 'mobile'
                }] if application.phone_number else [],
                'social_media_addresses': [{
                    'value': application.linkedin_url
                }] if application.linkedin_url else [],
                'tags': [self.JOBVYNE_TAG],
                'applications': [application_data]
            }
            resp = requests.post(
                self.candidates_url,
                headers=self.get_request_headers(is_user_id=True),
                json=post_data
            )
            if not is_good_response(resp):
                raise AtsError(f'Could not save candidate: {get_resp_error_message(resp)}')
            candidate_data = self.get_resp_data(resp)
            ats_candidate_key = str(candidate_data['id'])
            ats_application_key = str(candidate_data['application_ids'][0])
            
        # Add a note to the candidate so we know who referred them
        note_url = f'https://harvest.greenhouse.io/v1/candidates/{ats_candidate_key}/activity_feed/notes'
        resp = requests.post(
            note_url,
            headers=self.get_request_headers(is_user_id=True),
            json={
                'user_id': self.ats_user_id,
                'body': f'''Candidate was referred by {self.get_referrer_name_from_application(application)}
                    for the {self.get_job_title_from_application(application)} position
                    ''',
                'visibility': 'public'
            }
        )
        if not is_good_response(resp):
            raise AtsError(f'Could not save the note on candidate: {get_resp_error_message(resp)}')
            
        return ats_candidate_key, ats_application_key
    
    def get_initial_job_application_stage_id(self, ats_job_key):
        stages = self.get_job_stages()
        stage_name = self.ats_cfg.job_stage_name
        for stage in stages:
            if (
                str(stage['job_id']) == ats_job_key
                and ((stage_name and stage['name'] == stage_name) or (not stage_name and stage['priority'] == 0))
            ):
                return stage['id']
        return None
    
    def get_ats_user_id(self):
        resp = requests.get(
            self.users_url,
            headers=self.get_request_headers(),
            params={
                'email': self.ats_cfg.email
            }
        )
        if not is_good_response(resp):
            raise AtsError(f'Unable to fetch user: {get_resp_error_message(resp)}')
        return str(self.get_resp_data(resp)['id'])
    
    def get_request_headers(self, is_user_id=False):
        encoded_api_key = get_base64_encoded_str(f'{self.ats_cfg.api_key}:')
        return {
            'On-Behalf-Of': self.ats_user_id if is_user_id else self.ats_cfg.email,
            'Authorization': f'Basic {encoded_api_key}'
        }
    
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


def get_ats_api(ats_cfg: EmployerAts):
    return ats_map[ats_cfg.name](ats_cfg)


class AtsBaseView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        ats_id = self.data.get('ats_id') or self.query_params.get('ats_id')
        if not ats_id:
            raise ValueError('An ATS ID is required')

        self.ats_cfg = EmployerAts.objects.get(id=ats_id)
        self.check_permission()
        self.ats_api = get_ats_api(self.ats_cfg)
        
    def check_permission(self):
        self.ats_cfg.jv_check_permission(PermissionTypes.EDIT.value, self.user)


class AtsJobsView(AtsBaseView):
    
    def put(self, request):
        jobs = self.ats_api.get_jobs()
        self.ats_api.save_jobs(self.ats_cfg.employer_id, jobs)
        return Response(status=status.HTTP_200_OK)
    
    
class AtsStagesView(AtsBaseView):
    
    def get(self, request):
        stages = self.ats_api.get_job_stages()
        return Response(status=status.HTTP_200_OK, data=stages)


class AtsCustomFieldsView(AtsBaseView):
    
    def get(self, request):
        fields = self.ats_api.get_custom_fields()
        return Response(status=status.HTTP_200_OK, data=fields)
