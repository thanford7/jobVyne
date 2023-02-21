import base64
import hashlib
import hmac
import json
import logging
import re
import urllib.parse
from dataclasses import dataclass
from datetime import date, timedelta

import requests
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.apis.employer import EmployerAtsView
from jvapp.apis.geocoding import LocationParser
from jvapp.models import Employer, EmployerAts, EmployerJob, JobApplication, JobDepartment, PermissionName
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.data import coerce_int
from jvapp.utils.datetime import get_datetime_from_unix, get_datetime_or_none, get_unix_datetime
from jvapp.utils.file import get_file_name, get_mime_from_file_path, get_safe_file_path
from jvapp.utils.response import is_good_response
from jvapp.utils.sanitize import sanitize_html


logger = logging.getLogger(__name__)


REQUEST_FN_GET = requests.get
REQUEST_FN_POST = requests.post
REQUEST_FN_PUT = requests.put
REQUEST_FN_DELETE = requests.delete


class AtsError(Exception):
    pass


def get_resp_error_message(resp):
    return f'({resp.status_code}) {resp.text}'


def get_base64_encoded(text, as_string=True):
    # Must be in bytes to encode
    if not isinstance(text, bytes):
        text = text.encode()
    encoded_text = base64.b64encode(text)
    if as_string:
        return str(encoded_text, encoding='utf-8')
    return encoded_text


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
    salary_interval: str = None
    locations: list = None


def is_response_object(obj):
    return isinstance(obj, requests.Response)


class BaseAts:
    NAME = None  # Override with ATS name for subclasses
    BATCH_SIZE = 500
    JOBVYNE_TAG = 'JOBVYNE'
    DEFAULT_APP_LOOKBACK_DAYS = 120  # Number of days to pull applications for status updates
    
    def __init__(self, ats_cfg):
        self.ats_cfg = ats_cfg
        self.location_parser = LocationParser()
        self.ats_user_id = self.get_ats_user_id()
    
    def get_request_headers(self):
        return {}
    
    @staticmethod
    def get_resp_data(resp):
        return json.loads(resp.text)
    
    def get_current_applications(self, start_dt=None):
        start_dt = start_dt or (timezone.now() - timedelta(days=self.DEFAULT_APP_LOOKBACK_DAYS))
        return {
            app.ats_application_key or f'JOBVYNE-{app.id}': app
            for app in
            JobApplication.objects.filter(employer_job__employer_id=self.ats_cfg.employer_id, created_dt__gte=start_dt)
        }
    
    def get_current_jobs(self):
        return {
            job.ats_job_key or f'JOBVYNE-{job.id}': job
            for job in
            EmployerJob.objects
                .prefetch_related('locations')
                .filter(employer_id=self.ats_cfg.employer_id, close_date__isnull=True)
        }
    
    def get_job_departments(self):
        return {dept.name.lower(): dept for dept in JobDepartment.objects.all()}
    
    def get_locations(self):
        pass
    
    def get_referrer_name_from_application(self, application):
        referrer = application.social_link_filter.owner
        return f'{referrer.first_name} {referrer.last_name}'
    
    def get_job_title_from_application(self, application):
        return application.employer_job.job_title
    
    def get_encoded_resume(self, application, as_string=True):
        return get_base64_encoded(application.resume.open('rb').read(), as_string=as_string) if application.resume else None
    
    def get_referral_note(self, application):
        return f'''Candidate was referred by {self.get_referrer_name_from_application(application)}
        for the {self.get_job_title_from_application(application)} position
        '''
    
    def get_ats_user_id(self):
        return None
    
    def delete_webhooks(self):
        pass  # Noop - Override as needed
    
    def get_custom_fields(self):
        raise NotImplementedError()
    
    def get_normalized_job_data(self, job):
        raise NotImplementedError()
    
    def get_job_stages(self):
        raise NotImplementedError()
    
    def create_application(self, application):
        raise NotImplementedError()
    
    def add_application_note(self, application, **kwargs):
        raise NotImplementedError()
    
    def get_application(self, application_key):
        raise NotImplementedError()
    
    def get_candidate_key(self, application_key):
        raise NotImplementedError()
    
    def save_jobs(self, jobs):
        current_jobs = self.get_current_jobs()
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
                job_data = self.get_normalized_job_data(job)
                current_job = current_jobs.get(job_data.ats_job_key) or EmployerJob(
                    employer_id=self.ats_cfg.employer_id,
                    created_dt=now
                )
                current_job.modified_dt = now
                is_new = not bool(current_job.id)
                current_job.ats_job_key = job_data.ats_job_key
                current_job.job_title = job_data.job_title
                if job_data.job_description:
                    current_job.job_description = sanitize_html(job_data.job_description)
                else:
                    current_job.job_description = None
                current_job.open_date = job_data.open_date
                current_job.close_date = job_data.close_date
                job_department = None
                if job_data.department_name and not (job_department := job_departments.get(job_data.department_name.lower())):
                    job_department = JobDepartment(name=job_data.department_name)
                    job_department.save()
                    job_departments[job_data.department_name.lower()] = job_department
                current_job.job_department = job_department
                current_job.employment_type = job_data.employment_type
                current_job.salary_floor = job_data.salary_floor
                current_job.salary_ceiling = job_data.salary_ceiling
                current_job.salary_currency_id = job_data.salary_currency_type
                jobs_list = update_jobs
                if is_new:
                    # We can't bulk save new jobs because Django doesn't provide the PK after saving
                    # This would normally be fine, but we also have to bulk save job locations which
                    # requires the PK of the job
                    current_job.save()
                    jobs_list = create_jobs
                jobs_list.append(current_job)
                
                if (not is_new) and {l.id for l in job_data.locations} != {l.id for l in current_job.locations.all()}:
                    clear_location_job_ids.append(current_job.id)
                    for location in job_data.locations:
                        # jobs must be saved before the JobLocationsModel can be saved
                        # since jobs aren't saved yet, we store a reference to where we can get the job once it is saved
                        create_job_locations.append((location, is_new, len(jobs_list) - 1))
                if is_new:
                    for location in job_data.locations:
                        create_job_locations.append((location, is_new, len(jobs_list) - 1))
                
                process_count += 1
            
            # Update jobs
            EmployerJob.objects.bulk_update(update_jobs, EmployerJob.UPDATE_FIELDS)
            
            # Remove and add new locations
            processed_create_job_locations = []
            for (location, is_new, job_idx) in create_job_locations:
                job_list = update_jobs if not is_new else create_jobs
                job = job_list[job_idx]
                processed_create_job_locations.append(JobLocationsModel(location=location, employerjob=job))
            JobLocationsModel.objects.filter(employerjob_id__in=clear_location_job_ids).delete()
            JobLocationsModel.objects.bulk_create(processed_create_job_locations)
            
            create_jobs = []
            update_jobs = []
            create_job_locations = []
            clear_location_job_ids = []
        
        # Close any jobs that weren't created/updated
        close_jobs = EmployerJob.objects.filter(modified_dt__lt=now, ats_job_key__isnull=False)
        for job in close_jobs:
            job.close_date = now.date()
        EmployerJob.objects.bulk_update(close_jobs, ['close_date'])
        
    def save_application_statuses(self, application_statuses):
        current_applications = self.get_current_applications()
        applications_to_update = []
        for application_key, status_data in application_statuses.items():
            if not (application := current_applications.get(application_key)):
                continue
            if status_data.get('is_archived'):
                new_status = JobApplication.ApplicationStatus.DECLINED
            else:
                new_status = status_data['status']
            
            if application.application_status != new_status:
                application.application_status = new_status
                application.application_status_dt = timezone.now()
            
            if len(applications_to_update) == self.BATCH_SIZE:
                JobApplication.objects.bulk_update(applications_to_update, ['application_status', 'application_status_dt'])
                applications_to_update = []
                
        if len(applications_to_update):
            JobApplication.objects.bulk_update(applications_to_update, ['application_status', 'application_status_dt'])


class GreenhouseAts(BaseAts):
    NAME = 'greenhouse'
    
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
    
    def get_normalized_job_data(self, job):
        custom_fields = job['custom_fields']
        employment_type_key = self.ats_cfg.employment_type_field_key or 'employment_type'
        salary_range_key = self.ats_cfg.salary_range_field_key or 'salary_range'
        salary_range = custom_fields.get(salary_range_key)
        locations = [self.location_parser.get_location(office['location']['name']) for office in job['offices']]
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
        resume = self.get_encoded_resume(application, as_string=True)
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
        self.add_application_note(self.get_referral_note(application), candidate_key=ats_candidate_key)
            
        return ats_candidate_key, ats_application_key
    
    def add_application_note(self, note, candidate_key=None, **kwargs):
        if not candidate_key:
            raise AtsError(f'Could not save the note on candidate: A candidate key is required')
        note_url = f'https://harvest.greenhouse.io/v1/candidates/{candidate_key}/activity_feed/notes'
        resp = requests.post(
            note_url,
            headers=self.get_request_headers(is_user_id=True),
            json={
                'user_id': self.ats_user_id,
                'body': note,
                'visibility': 'public'
            }
        )
        if not is_good_response(resp):
            raise AtsError(f'Could not save the note on candidate: {get_resp_error_message(resp)}')

    def get_application_statuses(self):
        applications = self.get_applications()
        return {
            app['id']: {
                'status': self.get_application_status(app)
            } for app in applications
        }
    
    @staticmethod
    def get_application_status(application):
        application_status = application['status']
        if application_status == 'hired':
            return JobApplication.ApplicationStatus.HIRED.value
        elif application_status == 'rejected':
            return JobApplication.ApplicationStatus.DECLINED.value
        else:
            return application['current_stage']['name']

    def get_applications(self, app_start_date=None):
        app_start_date = app_start_date or (timezone.now() - timedelta(days=self.DEFAULT_APP_LOOKBACK_DAYS))
        app_start_timestamp = get_unix_datetime(app_start_date)
        return self.get_paginated_data(
            'https://harvest.greenhouse.io/v1/applications/',
            {'last_activity_after': app_start_timestamp}
        )
        
    def get_application(self, application_key):
        application_url = f'https://harvest.greenhouse.io/v1/applications/{application_key}'
        return self.get_data(application_url, {})
    
    def get_candidate_key(self, application_key):
        application_data = self.get_application(application_key)
        return application_data['candidate_id']
    
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
        encoded_api_key = get_base64_encoded(f'{self.ats_cfg.api_key}:')
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


class LeverAts(BaseAts):
    NAME = 'lever'
    
    EVENT_STAGE_CHANGE = 'candidateStageChange'
    EVENT_HIRED = 'candidateHired'
    EVENT_ARCHIVE_CHANGE = 'candidateArchiveChange'
    EVENT_DELETED = 'candidateDeleted'

    def get_paginated_data(self, relative_url, item_id=None, body_cfg=None):
        has_next = True
        next = None
        data = []
        relative_url = f'{relative_url}/{item_id}' if item_id else relative_url
        while has_next:
            response = self.get_data(REQUEST_FN_GET, relative_url, next_key=next, body_cfg=body_cfg)
            has_next = response.get('hasNext')
            next = response.get('next')
            data += response.get('data', [])
    
        return data

    def get_data(self, request_method_fn, relative_url, next_key=None, body_cfg=None, files=None, is_JSON=False):
        body = {}
        if body_cfg:
            body = {**body_cfg, **body}
        if next_key:
            body['offset'] = next_key
        url = f'{settings.LEVER_BASE_URL}{relative_url}'
        
        if LeverOauthTokenView.has_access_token_expired(self.ats_cfg):
            LeverOauthTokenView.refresh_access_token(self.ats_cfg)
        
        request_kwargs = {}
        request_kwargs['headers'] = {'Authorization': f'Bearer {self.ats_cfg.access_token}'}
        if is_JSON:
            request_kwargs['headers']['Content-Type'] = 'application/json'
            request_kwargs['json'] = body
        elif request_method_fn == REQUEST_FN_GET:
            request_kwargs['params'] = body
        else:
            request_kwargs['data'] = body
        
        if files:
            request_kwargs['files'] = files
    
        response = request_method_fn(url, **request_kwargs)
        if not is_good_response(response):
            raise AtsError(f'Could not complete request for {relative_url} endpoint: {get_resp_error_message(response)}')
        
        # Delete requests don't return any content
        return response.json() if response.content else None

    def get_jobs(self):
        jobs = self.get_paginated_data('postings', body_cfg={'state': 'published'})
        requisitions = self.get_requisitions()
        if requisitions:
            for job in jobs:
                requisition_codes = job['requisitionCodes']
                salary_range = job.get('salaryRange')
                if not any([requisition_codes, salary_range]):
                    continue
                
                # If no salary range is present on the job, fall back to requisition
                if not salary_range:
                    requisition_code = requisition_codes[0]
                    requisition = requisitions.get(requisition_code)
                    if not requisition:
                        continue
                    salary_range = requisition['compensationBand']
                    if not salary_range:
                        continue
                
                min_salary, max_salary, interval = self.get_normalized_salary(salary_range)
                job['salary_floor'] = min_salary
                job['salary_ceiling'] = max_salary
                job['salary_interval'] = interval
                job['salary_currency'] = salary_range['currency']
            
        return jobs
    
    def get_posting_owner_key(self, job_key):
        job = self.get_data(REQUEST_FN_GET, f'postings/{job_key}')
        return job['data']['owner']
    
    def get_requisitions(self):
        requisitions = self.get_paginated_data('requisitions', body_cfg={'status': 'open'}) or []
        return {r['requisitionCode']: r for r in requisitions}

    def get_normalized_job_data(self, job):
        raw_location = job['categories']['location']
        if job['workplaceType'] == 'remote':
            raw_location = f'Remote: {raw_location}'
        locations = [self.location_parser.get_location(raw_location) if raw_location else None]
        data = JobData(
            ats_job_key=str(job['id']),
            job_title=job['text'],
            job_description=self.get_formatted_job_description(job['content']),
            open_date=self.get_datetime_from_lever_unix(job['createdAt']),
            department_name=f'{job["categories"]["team"]} - {job["categories"]["department"]}',
            employment_type=job['categories']['commitment'],
            salary_floor=job.get('salary_floor'),
            salary_ceiling=job.get('salary_ceiling'),
            salary_currency_type=job.get('salary_currency'),
            salary_interval=job.get('salary_interval'),
            locations=[l for l in locations if l]
        )
        return data

    def create_application(self, application):
        # Make sure this person hasn't applied already
        current_opportunities = self.get_opportunities_for_candidate(application.email)
        for opp in current_opportunities:
            ats_job_key = opp['application']['posting']
            if ats_job_key == application.employer_job.ats_job_key:
                return opp['contact'], opp['id']
        
        body_cfg = {
            'name': f'{application.first_name} {application.last_name}',
            'postings[]': application.employer_job.ats_job_key,
            'stage': self.ats_cfg.job_stage_name,
            'emails[]': application.email,
            'tags[]': self.JOBVYNE_TAG,
            'sources[]': self.JOBVYNE_TAG,
            'origin': 'referred',
            'createdAt': self.get_lever_unix_from_datetime(timezone.now())
        }
        if application.phone_number:
            body_cfg['phones[]'] = json.dumps({'value': application.phone_number})
        if application.linkedin_url:
            body_cfg['links[]'] = application.linkedin_url
        
        posting_owner_key = self.get_posting_owner_key(application.employer_job.ats_job_key)
        resume_file_path = get_safe_file_path(application.resume)
        data = self.get_data(
            REQUEST_FN_POST,
            f'opportunities?perform_as={posting_owner_key}&parse=true&perform_as_posting_owner=true',
            body_cfg=body_cfg,
            files={'resumeFile': (get_file_name(resume_file_path), application.resume.open('rb').read(), get_mime_from_file_path(resume_file_path))}
        )

        return data['data']['contact'], data['data']['id']
    
    def get_candidate_key(self, application_key):
        return application_key
    
    def add_application_note(self, note, candidate_key=None, **kwargs):
        if not candidate_key:
            raise AtsError('Could not save the note on candidate: An opportunity key is required')
        self.get_data(
            REQUEST_FN_POST,
            f'opportunities/{candidate_key}/notes',
            is_JSON=True,
            body_cfg={
                'value': note
            }
        )
        
    def add_webhook(self, event):
        webhook_url = f'{settings.API_URL}lever/webhooks/{self.ats_cfg.employer_id}/'
        body_cfg = {
            'url': webhook_url,
            'event': event,
        }
        if event != LeverAts.EVENT_DELETED:
            body_cfg['configuration'] = {
                'conditions': {
                    'origins': ['referred']
                }
            }
        data = self.get_data(
            REQUEST_FN_POST, 'webhooks', is_JSON=True, body_cfg=body_cfg
        )
        return data['data']
    
    def get_application_statuses(self):
        applications = self.get_applications()
        return {
            app['id']: {
                'status': app['stage']['text'],
                'is_archived': bool(app['archivedAt'])
            } for app in applications
        }
    
    def get_opportunities_for_candidate(self, candidate_email):
        return self.get_paginated_data(f'opportunities?expand=applications&tag={self.JOBVYNE_TAG}&email={urllib.parse.quote(candidate_email)}')
    
    def get_applications(self, app_start_date=None):
        app_start_date = app_start_date or (timezone.now() - timedelta(days=self.DEFAULT_APP_LOOKBACK_DAYS))
        app_start_timestamp = self.get_lever_unix_from_datetime(app_start_date)
        return self.get_paginated_data(f'opportunities?expand=applications&expand=stage&tag={self.JOBVYNE_TAG}&created_at_start={app_start_timestamp}')
        
    def get_application(self, opportunity_key):
        data = self.get_data(REQUEST_FN_GET, f'opportunities/{opportunity_key}?expand=applications&expand=stage')
        return data['data']

    def get_job_stages(self):
        return self.get_paginated_data('stages')
    
    def get_job_stage(self, stage_key):
        data = self.get_data(REQUEST_FN_GET, f'stages/{stage_key}')
        return data['data']
    
    def get_jobvyne_lever_user(self, email):
        data = self.get_data(REQUEST_FN_GET, f'users?email={urllib.parse.quote(email)}')
        users = data['data']
        return users[0] if users else None
    
    def get_or_create_jobvyne_lever_user(self, email):
        user = self.get_jobvyne_lever_user(email)
        if not user:
            resp = self.get_data(REQUEST_FN_POST, 'users', is_JSON=True, body_cfg={
                'name': 'JobVyne',
                'email': email,
                'accessRole': 'team member'
            })
            user = resp['data']
        
        return user
    
    def delete_webhooks(self):
        for webhook_key in ('webhook_stage_change_key', 'webhook_archive_key', 'webhook_hire_key', 'webhook_delete_key'):
            if key := getattr(self.ats_cfg, webhook_key):
                self.get_data(REQUEST_FN_DELETE, f'webhooks/{key}')
    
    @staticmethod
    def get_formatted_job_description(description_content):
        html_text = description_content.get('descriptionHtml', '')
        
        description_lists = description_content['lists']
        for description_list in description_lists:
            html_text += f'<h6>{description_list["text"]}</h6>'
            html_text += description_list['content']
        
        html_text += description_content.get('closingHtml', '')
        return html_text
    
    @staticmethod
    def get_normalized_salary(compensation):
        min_salary = coerce_int(compensation['min'])
        max_salary = coerce_int(compensation['max'])
        interval = compensation['interval']
        if not all([min_salary, max_salary, interval]):
            return None, None, None
        if interval == 'per-year-salary':
            return min_salary, max_salary, EmployerJob.SalaryInterval.YEAR.value
        if interval == 'per-month-salary':
            return min_salary, max_salary, EmployerJob.SalaryInterval.MONTH.value
        if interval == 'semi-month-salary':
            return min_salary * 2, max_salary * 2, EmployerJob.SalaryInterval.MONTH.value
        if interval == 'bi-month-salary':
            return min_salary / 2, max_salary / 2, EmployerJob.SalaryInterval.MONTH.value
        if interval == 'bi-week-salary':
            return min_salary / 2, max_salary / 2, EmployerJob.SalaryInterval.WEEK.value
        if interval == 'per-week-salary':
            return min_salary, max_salary, EmployerJob.SalaryInterval.WEEK.value
        if interval == 'per-day-wage':
            return min_salary, max_salary, EmployerJob.SalaryInterval.DAY.value
        if interval == 'per-hour-wage':
            return min_salary, max_salary, EmployerJob.SalaryInterval.HOUR.value
        if interval == 'one-time':
            return min_salary, max_salary, EmployerJob.SalaryInterval.ONCE.value
        return None, None, None
    
    @staticmethod
    def get_datetime_from_lever_unix(val):
        if not val:
            return None
        # Lever uses milliseconds for unix, but we need it in seconds
        unix_ts = int(val) / 1000
        return get_datetime_from_unix(unix_ts)
    
    @staticmethod
    def get_lever_unix_from_datetime(val):
        ts = get_unix_datetime(val)
        return ts * 1000


ats_map = {
    GreenhouseAts.NAME: GreenhouseAts,
    LeverAts.NAME: LeverAts
}


def get_ats_api(ats_cfg: EmployerAts):
    return ats_map[ats_cfg.name](ats_cfg)


class AtsBaseView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        ats_id = self.data.get('ats_id') or self.query_params.get('ats_id')
        self.employer_id = self.data.get('employer_id')
        if not any([ats_id, self.employer_id]):
            return get_error_response('An ATS ID or employer ID is required')
        
        if ats_id:
            ats_filter = Q(id=ats_id)
        else:
            ats_filter = Q(employer_id=self.employer_id)

        try:
            self.ats_cfg = EmployerAts.objects.select_related('employer').get(ats_filter)
        except EmployerAts.DoesNotExist:
            return get_error_response('An ATS connection does not exist')

        self.ats_api = get_ats_api(self.ats_cfg)


class AtsJobsView(AtsBaseView):
    
    def put(self, request):
        if not any([
            self.user.is_admin,
            self.user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_JOBS.value, self.employer_id)
        ]):
            return get_error_response('You do not have the appropriate permissions to update jobs')

        jobs = self.ats_api.get_jobs()
        self.ats_api.save_jobs(jobs)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully updated jobs'
        })
    
    
class AtsStagesView(AtsBaseView):
    
    def get(self, request):
        stages = self.ats_api.get_job_stages()
        return Response(status=status.HTTP_200_OK, data=stages)


class AtsCustomFieldsView(AtsBaseView):
    
    def get(self, request):
        fields = self.ats_api.get_custom_fields()
        return Response(status=status.HTTP_200_OK, data=fields)
    
    
class LeverOauthUrlView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def get(self, request):
        lever_redirect_url = self.get_redirect_url(request)
        lever_oauth_url = f'{settings.LEVER_REDIRECT_BASE}?client_id={settings.LEVER_CLIENT_ID}&redirect_uri={lever_redirect_url}&state={settings.LEVER_STATE}&response_type=code&scope={settings.LEVER_SCOPE}&prompt=consent&audience={settings.LEVER_BASE_URL}'
        return Response(status=status.HTTP_200_OK, data=lever_oauth_url)
    
    @staticmethod
    def get_redirect_url(request):
        base_url = get_current_site(request).domain
        return f'https://{base_url}{settings.LEVER_CALLBACK_URL}'
    

class LeverOauthTokenView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    ACCESS_TOKEN_EXPIRATION_SECONDS = 60 * 60  # 1 hour
    REFRESH_TOKEN_EXPIRATION_SECONDS = 60 * 60 * 24 * 30  # 30 days
    EXPIRATION_BUFFER_SECONDS = 60 * 2
    
    def post(self, request):
        if self.data.get('state') != settings.LEVER_STATE:
            return Response('Request state is incorrect', status=status.HTTP_400_BAD_REQUEST)
        
        if not (employer_id := self.data.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        ats_cfg = EmployerAtsView.get_new_ats_cfg(self.user, employer_id, LeverAts.NAME)
        if not self.has_refresh_token_expired(ats_cfg):
            self.refresh_access_token(ats_cfg)
        else:
            response = requests.post(settings.LEVER_AUTH_TOKEN_URL, {
                'client_id': settings.LEVER_CLIENT_ID,
                'client_secret': settings.LEVER_CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'code': self.data.get('code'),
                'redirect_uri': LeverOauthUrlView.get_redirect_url(request)
            })
    
            if response.status_code != 200:
                self.raise_response_error(response)
    
            data = response.json()
            EmployerAtsView.update_ats(self.user, ats_cfg, {**data, **self.data})
            self.update_token_expiration(ats_cfg)
            ats_cfg.save()
        
        # Add webhook configuration
        ats_api = get_ats_api(ats_cfg)
        for event, key_attr, token_attr in (
            (LeverAts.EVENT_STAGE_CHANGE, 'webhook_stage_change_key', 'webhook_stage_change_token'),
            (LeverAts.EVENT_ARCHIVE_CHANGE, 'webhook_archive_key', 'webhook_archive_token'),
            (LeverAts.EVENT_HIRED, 'webhook_hire_key', 'webhook_hire_token'),
            (LeverAts.EVENT_DELETED, 'webhook_delete_key', 'webhook_delete_token')
        ):
            # Don't add a new webhook if one already exists
            if getattr(ats_cfg, key_attr, None):
                continue
                
            webhook_data = ats_api.add_webhook(event)
            setattr(ats_cfg, key_attr, webhook_data['id'])
            setattr(ats_cfg, token_attr, webhook_data['configuration']['signatureToken'])
        
        ats_cfg.save()
            
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Lever successfully connected'
        })
    
    def put(self, request):
        if not (employer_id := self.data.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        ats_cfg = EmployerAtsView.get_new_ats_cfg(self.user, employer_id, LeverAts.NAME)
        self.refresh_access_token(ats_cfg)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Lever successfully connected'
        })

    @staticmethod
    def has_access_token_expired(ats_cfg):
        if not (ats_cfg.access_token and ats_cfg.access_token_expire_dt):
            return True
        return (ats_cfg.access_token_expire_dt - timedelta(seconds=LeverOauthTokenView.EXPIRATION_BUFFER_SECONDS)) < timezone.now()
    
    @staticmethod
    def has_refresh_token_expired(ats_cfg):
        if not (ats_cfg.refresh_token and ats_cfg.refresh_token_expire_dt):
            return True
        return (ats_cfg.refresh_token_expire_dt - timedelta(seconds=LeverOauthTokenView.EXPIRATION_BUFFER_SECONDS)) < timezone.now()
    
    @staticmethod
    def refresh_access_token(ats_cfg):
        if not ats_cfg.refresh_token:
            raise ConnectionError('No refresh token exists for this employer')
        if LeverOauthTokenView.has_refresh_token_expired(ats_cfg):
            raise ConnectionError('The refresh token has already expired')
        response = requests.post(settings.LEVER_AUTH_TOKEN_URL, {
            'client_id': settings.LEVER_CLIENT_ID,
            'client_secret': settings.LEVER_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': ats_cfg.refresh_token
        })

        if response.status_code != 200:
            LeverOauthTokenView.raise_response_error(response)

        data = response.json()
        ats_cfg.access_token = data['access_token']
        ats_cfg.refresh_token = data['refresh_token']
        LeverOauthTokenView.update_token_expiration(ats_cfg)
        ats_cfg.save()
        
    @staticmethod
    def update_token_expiration(ats_cfg):
        ats_cfg.access_token_expire_dt = timezone.now() + timedelta(seconds=LeverOauthTokenView.ACCESS_TOKEN_EXPIRATION_SECONDS)
        ats_cfg.refresh_token_expire_dt = timezone.now() + timedelta(seconds=LeverOauthTokenView.REFRESH_TOKEN_EXPIRATION_SECONDS)
        
    @staticmethod
    def raise_response_error(response):
        raise ConnectionError(f'({response.status_code}) Unable to connect to Lever: {response.reason}')


class LeverWebhooksView(APIView):
    permission_classes = [AllowAny]
    hook_events = {
        LeverAts.EVENT_STAGE_CHANGE: {
            'name': 'stage change',
            'token_attr': 'webhook_stage_change_token'
        },
        LeverAts.EVENT_HIRED: {
            'name': 'candidate hire',
            'token_attr': 'webhook_hire_token',
            'status': JobApplication.ApplicationStatus.HIRED.value
        },
        LeverAts.EVENT_ARCHIVE_CHANGE: {
            'name': 'candidate archive',
            'token_attr': 'webhook_archive_token',
        },
        LeverAts.EVENT_DELETED: {
            'name': 'candidate delete',
            'token_attr': 'webhook_delete_token',
            'status': JobApplication.ApplicationStatus.DECLINED.value
        }
    }
    
    def post(self, request, employer_id):
        data = request.data
        employer = Employer.objects.prefetch_related('ats_cfg').get(id=employer_id)
        logging_message_start = f'{employer.employer_name} (ID={employer.id}) |'
        ats_cfg = next((cfg for cfg in employer.ats_cfg.all()), None)
        if not ats_cfg:
            logger.error(f'{logging_message_start} No active connection with Lever')
            return Response(status=status.HTTP_200_OK)
        
        event = data['event']
        event_cfg = self.hook_events[event]
        hook_token = getattr(ats_cfg, event_cfg['token_attr'])
        if not hook_token:
            logger.error(f'{logging_message_start} The signature token for the {event_cfg["name"]} webhook has not been configured')
            return Response(status=status.HTTP_200_OK)
    
        is_authorized_request = self.validate_lever_request(data, hook_token)
        if not is_authorized_request:
            logger.warning(f'{logging_message_start} Unauthorized Lever webhook request')
            return Response(status=status.HTTP_200_OK)
    
        # If data is empty, it was just a test connection
        if not data['data']:
            return Response(status=status.HTTP_200_OK)
    
        event_data = data['data']
        try:
            job_application = JobApplication.objects.get(ats_application_key=event_data['opportunityId'])
        except JobApplication.DoesNotExist:
            logger.warning(
                f'{logging_message_start} Webhook received request for unknown application. Opportunity key: {event_data["opportunityId"]}'
            )
            return Response(status=status.HTTP_200_OK)
        
        # Update application status and datetime
        ats_api = get_ats_api(ats_cfg)
        application_status = event_cfg.get('status')
        if application_status:
            pass
        elif event == 'candidateStageChange':
            stage_key = event_data['toStageId']
            job_stage = ats_api.get_job_stage(stage_key)
            application_status = job_stage['text']
        elif event == 'candidateArchiveChange':
            if event_data['toArchived']:
                application_status = JobApplication.ApplicationStatus.DECLINED.value
            else:
                application = ats_api.get_application(event_data['opportunityId'])
                application_status = application['stage']['text']
        
        job_application.application_status = application_status
        job_application.application_status_dt = timezone.now()
        job_application.save()
    
    @staticmethod
    def validate_lever_request(request_data, signature_token):
        plain_text = request_data.get('token') + str(request_data['triggeredAt'])
        hash = hmac.new(bytes(signature_token, 'UTF-8'), plain_text.encode(), hashlib.sha256).hexdigest()
        return hash == request_data['signature']
