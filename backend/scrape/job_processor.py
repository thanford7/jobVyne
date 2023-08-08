import datetime
from dataclasses import dataclass
from typing import Union

from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone

from jvapp.apis.geocoding import LocationParser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.employer import EmployerJob, JobDepartment
from jvapp.utils.file import get_file_extension
from jvapp.utils.image import convert_url_to_image
from jvapp.utils.sanitize import sanitize_html
from jvapp.utils.taxonomy import run_job_title_standardization


@dataclass
class JobItem:
    employer_name: str = None
    application_url: Union[str, None] = None
    job_title: str = None
    locations: list = None
    job_department: str = None
    job_description: str = None
    employment_type: Union[str, None] = None
    first_posted_date: Union[datetime.date, None] = None
    salary_currency: Union[str, None] = None
    salary_floor: Union[float, None] = None
    salary_ceiling: Union[float, None] = None
    salary_interval: Union[str, None] = None
    logo_url: Union[str, None] = None
    website_domain: Union[str, None] = None
    created_user_id: Union[int, None] = None
    
    def get_compensation_dict(self):
        return {
            'salary_currency': self.salary_currency,
            'salary_floor': self.salary_floor,
            'salary_ceiling': self.salary_ceiling,
            'salary_interval': self.salary_interval
        }


class JobProcessor:
    IS_JOB_SCRAPED = False
    default_employment_type = 'Full Time'
    
    def __init__(self, employer, ignore_fields=None, is_use_location_caching=True):
        self.employer = employer
        jobs = self.get_existing_jobs(employer)
        self.jobs_by_key = {j.get_key(): j for j in jobs}
        self.jobs_by_url = {j.application_url: j for j in jobs}
        self.found_jobs = set()
        self.location_parser = LocationParser(is_use_location_caching=is_use_location_caching)
        self.job_departments = {j.name.lower(): j for j in JobDepartment.objects.all()}
        self.ignore_fields = ignore_fields or []  # Fields that should not be updated
    
    def get_existing_jobs(self, employer):
        return EmployerJob.objects.prefetch_related('locations').filter(employer=employer)
    
    def get_job_by_key(self, job_title, location_ids):
        return self.jobs_by_key.get(EmployerJob.generate_job_key(job_title, location_ids))
    
    def process_jobs(self, job_items):
        for job_item in job_items:
            self.process_job(job_item)
    
    def save_employer(self, job_item: JobItem):
        is_save_employer = False
        if job_item.logo_url and not self.employer.logo:
            self.employer.logo = convert_url_to_image(
                job_item.logo_url,
                f'{self.employer.employer_name}_logo.{get_file_extension(job_item.logo_url)}',
                is_use_request=True
            )
            is_save_employer = True
        if job_item.website_domain and (
                not self.employer.email_domains or job_item.website_domain not in self.employer.email_domains):
            if not self.employer.email_domains:
                self.employer.email_domains = job_item.website_domain
            else:
                self.employer.email_domains += f',{job_item.website_domain}'
            is_save_employer = True
        
        if is_save_employer:
            self.employer.save()
    
    def get_job_locations(self, job_item: JobItem):
        if job_item.locations and (not isinstance(job_item.locations, list)):
            job_item.locations = [job_item.locations]
        locations = list(set([
            self.location_parser.get_location(self.add_remote_to_location(loc, job_item.job_title))
            for loc in set(job_item.locations) if loc
        ]))
        location_ids = [l.id for l in locations]
        location_ids.sort()
        location_ids = tuple(location_ids)
        return locations, location_ids
    
    def process_job(self, job_item: JobItem, user=None):
        raise NotImplemented()
    
    def is_same_job(self, job: EmployerJob, job_item: JobItem):
        """Check whether all job attributes are the same and therefore there's no need to update/save
        """
        job_department = self.get_or_create_job_department(job_item)
        if any([
            job.application_url != job_item.application_url,
            job.job_description != job_item.job_description,
            job.employment_type != job_item.employment_type,
            job.job_department != job_department,
            job.salary_floor != job_item.salary_floor,
            job.salary_ceiling != job_item.salary_ceiling,
            job.salary_interval != job_item.salary_interval,
            not job.open_date,
            job.close_date
        ]):
            return False
        
        return True
    
    def update_job(self, job: EmployerJob, job_item: JobItem):
        if self.is_same_job(job, job_item):
            job.save()  # Updates the modified_dt
            return job
        
        for field in (
            'application_url', 'job_description', 'employment_type', 'salary_floor', 'salary_ceiling', 'salary_interval'
        ):
            if field in self.ignore_fields:
                continue
            setattr(job, field, getattr(job_item, field))
        
        if 'job_department' not in self.ignore_fields:
            job.job_department = self.get_or_create_job_department(job_item)
        if 'salary_currency' not in self.ignore_fields:
            job.salary_currency_name = job_item.salary_currency
        
        if self.IS_JOB_SCRAPED:
            job.is_job_approved = True
            job.created_user = None
        else:
            job.is_job_approved = False
        
        job.open_date = job.open_date or job_item.first_posted_date or timezone.now().date()
        job.close_date = None
        job.save()
        return job
    
    def get_or_create_job_department(self, job_item: JobItem):
        if not job_item.job_department:
            return None
        
        if not (job_department := self.job_departments.get(job_item.job_department.lower())):
            # We still might miss an existing job department if another employer job processor has recently saved it
            try:
                job_department = JobDepartment(name=job_item.job_department)
                job_department.save()
            except IntegrityError:
                job_department = JobDepartment.objects.get(name=job_item.job_department)
            
            self.job_departments[job_item.job_department.lower()] = job_department
        
        return job_department
    
    @staticmethod
    def add_remote_to_location(location, job_title):
        if 'remote' in job_title.lower() and not 'remote' in location.lower():
            return f'{location} (remote)'
        return location


class UserCreatedJobProcessor(JobProcessor):
    
    def process_job(self, job_item: JobItem, user=None):
        assert user
        job_item.employment_type = job_item.employment_type or self.default_employment_type
        locations, location_ids = self.get_job_locations(job_item)
        new_job = EmployerJob(
            job_title=job_item.job_title.strip(),
            is_job_approved=False,
            created_user_id=job_item.created_user_id
        )
        
        existing_job_by_key = self.get_job_by_key(new_job.job_title, location_ids)
        existing_job_by_url = self.jobs_by_url.get(job_item.application_url)
        existing_job = existing_job_by_key or existing_job_by_url
        if existing_job:
            if existing_job.jv_check_permission(PermissionTypes.EDIT.value, user):
                self.update_job(existing_job, job_item)
            if existing_job_by_url:
                existing_job.locations.set(locations)
            run_job_title_standardization(job_filter=Q(id=existing_job.id))
            return existing_job, False
        
        new_job.employer = self.employer
        self.update_job(new_job, job_item)
        new_job.locations.set(locations)
        run_job_title_standardization(job_filter=Q(id=new_job.id))
        
        return new_job, True


class ScrapedJobProcessor(JobProcessor):
    IS_JOB_SCRAPED = True
    
    def get_existing_jobs(self, employer):
        return EmployerJob.objects.prefetch_related('locations').filter(
            employer=employer,
            is_scraped=True
        )
    
    def process_job(self, job_item: JobItem, user=None):
        """Create or update an EmployerJob
        """
        self.save_employer(job_item)
        job_item.job_description = sanitize_html(job_item.job_description)
        job_item.employment_type = job_item.employment_type or self.default_employment_type
        locations, location_ids = self.get_job_locations(job_item)
        
        new_job = EmployerJob(
            job_title=job_item.job_title.strip(),
            is_scraped=self.IS_JOB_SCRAPED
        )
        is_new_job = False
        is_update_locations = True
        existing_job_by_key = self.get_job_by_key(new_job.job_title, location_ids)
        existing_job_by_url = self.jobs_by_url.get(job_item.application_url)
        if existing_job_by_key:
            self.update_job(existing_job_by_key, job_item)
            job = existing_job_by_key
            is_update_locations = False
        elif existing_job_by_url:
            self.update_job(existing_job_by_url, job_item)
            job = existing_job_by_url
        else:
            new_job.employer = self.employer
            self.update_job(new_job, job_item)
            self.jobs_by_key[EmployerJob.generate_job_key(new_job.job_title, location_ids)] = new_job
            self.jobs_by_url[new_job.application_url] = new_job
            job = new_job
            is_new_job = True
        
        if is_update_locations:
            job.locations.set(locations)
        self.found_jobs.add(EmployerJob.generate_job_key(job.job_title, location_ids))
        
        return job, is_new_job
    
    def finalize_data(self, skipped_job_urls):
        # Set the close date of a job if it no longer exists on the employers job page
        skipped_jobs = []
        close_jobs = []
        for job_key, job in self.jobs_by_key.items():
            if job.application_url in skipped_job_urls:
                skipped_jobs.append(job)
            elif job_key not in self.found_jobs and not job.close_date:
                job.close_date = timezone.now().date()
                job.modified_dt = timezone.now()
                close_jobs.append(job)
        
        EmployerJob.objects.bulk_update(close_jobs, ['close_date', 'modified_dt'])
        self.employer.has_job_scraper = True
        self.employer.last_job_scrape_success_dt = timezone.now()
        self.employer.has_job_scrape_failure = False
        self.employer.save()
        
        # Bulk update the modified timestamp of jobs that were skipped
        EmployerJob.objects \
            .filter(id__in=[j.id for j in skipped_jobs]) \
            .update(modified_dt=timezone.now())
        
        run_job_title_standardization(job_filter=Q(employer_id=self.employer.id), is_non_standardized_only=True)
