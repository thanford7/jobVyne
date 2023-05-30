import datetime
from dataclasses import dataclass
from typing import Union

from django.utils import timezone

from jvapp.apis.geocoding import LocationParser
from jvapp.models import EmployerJob, JobDepartment
from jvapp.utils.sanitize import sanitize_html


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
    
    def get_compensation_dict(self):
        return {
            'salary_currency': self.salary_currency,
            'salary_floor': self.salary_floor,
            'salary_ceiling': self.salary_ceiling,
            'salary_interval': self.salary_interval
        }


class JobProcessor:
    default_employment_type = 'Full Time'
    
    def __init__(self, employer):
        self.employer = employer
        self.jobs = {
            j.get_key(): j for j in
            EmployerJob.objects.prefetch_related('locations').filter(
                employer=employer,
                is_scraped=True
            )
        }
        self.found_jobs = set()
        self.location_parser = LocationParser()
        # TODO: Handle bogus locations (multiple, bad format, etc.)
        self.job_departments = {j.name.lower(): j for j in JobDepartment.objects.all()}
        
    def finalize_data(self, skipped_job_urls):
        # Set the close date of a job if it no longer exists on the employers job page
        skipped_jobs = []
        close_jobs = []
        for job_key, job in self.jobs.items():
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
        EmployerJob.objects\
            .filter(id__in=[j.id for j in skipped_jobs])\
            .update(modified_dt=timezone.now())

    def process_jobs(self, job_items):
        for job_item in job_items:
            self.process_job(job_item)
    
    def process_job(self, job_item: JobItem):
        job_item.job_description = sanitize_html(job_item.job_description)
        job_item.employment_type = job_item.employment_type or self.default_employment_type
        
        locations = [
            self.location_parser.get_location(self.add_remote_to_location(loc, job_item.job_title))
            for loc in set(job_item.locations)
        ]
        location_ids = [l.id for l in locations]
        location_ids.sort()
        location_ids = tuple(location_ids)
        
        new_job = EmployerJob(
            job_title=job_item.job_title,
            is_scraped=True
        )
        if not (job := self.jobs.get(EmployerJob.generate_job_key(new_job.job_title, location_ids))):
            new_job.employer = self.employer
            self.update_job(new_job, job_item)
            self.jobs[EmployerJob.generate_job_key(new_job.job_title, location_ids)] = new_job
            job = new_job
        else:
            self.update_job(job, job_item)
        
        job_location_model = job.locations.through
        job_location_model.objects.bulk_create(
            [job_location_model(location=l, employerjob=job) for l in locations],
            ignore_conflicts=True
        )
        
        self.found_jobs.add(EmployerJob.generate_job_key(job.job_title, location_ids))
        
        return job
    
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
        
        job.application_url = job_item.application_url
        job.job_description = job_item.job_description
        job.employment_type = job_item.employment_type
        job.job_department = self.get_or_create_job_department(job_item)
        job.salary_currency_name = job_item.salary_currency
        job.salary_floor = job_item.salary_floor
        job.salary_ceiling = job_item.salary_ceiling
        job.salary_interval = job_item.salary_interval
        
        job.open_date = job.open_date or job_item.first_posted_date or timezone.now().date()
        job.close_date = None
        job.save()
        return job
    
    def get_or_create_job_department(self, job_item: JobItem):
        if not job_item.job_department:
            return None
        
        if not (job_department := self.job_departments.get(job_item.job_department.lower())):
            job_department = JobDepartment(name=job_item.job_department)
            job_department.save()
            self.job_departments[job_item.job_department.lower()] = job_department
        
        return job_department
    
    @staticmethod
    def add_remote_to_location(location, job_title):
        if 'remote' in job_title.lower() and not 'remote' in location.lower():
            return f'{location} (remote)'
        return location
