import datetime
from dataclasses import dataclass
from typing import Union

from django.utils import timezone

from jvapp.apis.geocoding import LocationParser
from jvapp.models import Employer, EmployerJob, JobDepartment

@dataclass
class JobItem:
    employer_name: str
    application_url: Union[str, None]
    job_title: str
    locations: list
    job_department: str
    job_description: str
    employment_type: Union[str, None]
    first_posted_date: Union[datetime.date, None]


class JobProcessor:
    
    def __init__(self):
        self.employers = {employer.employer_name: {
            'employer': employer,
            'jobs': {self.generate_job_key(j): j for j in employer.employer_job.all() if j.is_scraped},
            'found_jobs': set()
        } for employer in Employer.objects.prefetch_related('employer_job', 'employer_job__locations').all()}
        self.scraped_employers = set()
        self.location_parser = LocationParser()
        self.job_departments = {j.name.lower(): j for j in JobDepartment.objects.all()}
        
    def finalize_data(self):
        # Set the close date of a job if it no longer exists on the employers job page
        for employer_data in self.employers.values():
            employer = employer_data['employer']
            if employer.employer_name not in self.scraped_employers:
                continue
            for job_key, job in employer_data['jobs'].items():
                if job_key not in employer_data['found_jobs'] and not job.close_date:
                    job.close_date = timezone.now().date()
                    job.save()
            employer.last_job_scrape_success_dt = timezone.now()
            employer.save()
    
    def process_jobs(self, job_items):
        for job_item in job_items:
            self.process_job(job_item)
    
    def process_job(self, job_item: JobItem):
        employer_name = job_item.employer_name
        employer_data = self.employers.get(employer_name)
        if not employer_data:
            employer = Employer(employer_name=employer_name)
            employer.save()
            employer_data = {
                'employer': employer,
                'jobs': {},
                'found_jobs': set()
            }
            self.employers[employer_name] = employer_data
        else:
            employer = employer_data['employer']
        self.scraped_employers.add(employer_name)
        
        if not job_item.employment_type:
            return
        
        locations = [self.location_parser.get_location(loc) for loc in job_item.locations]
        
        new_job = EmployerJob(
            job_title=job_item.job_title,
            is_scraped=True
        )
        if not (job := employer_data['jobs'].get(self.generate_job_key(new_job, locations=locations))):
            new_job.employer = employer
            self.update_job(new_job, job_item)
            employer_data['jobs'][self.generate_job_key(new_job, locations=locations)] = new_job
            job = new_job
        else:
            self.update_job(job, job_item)
        
        job_location_model = job.locations.through
        job_location_model.objects.bulk_create(locations, ignore_conflicts=True)
        
        employer_data['found_jobs'].add(self.generate_job_key(job, locations=locations))
        
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
            not job.open_date,
            job.close_date
        ]):
            return False
        
        return True
    
    def update_job(self, job, job_item: JobItem):
        if self.is_same_job(job, job_item):
            return job
        
        job.application_url = job_item.application_url
        job.job_description = job_item.job_description
        job.employment_type = job_item.employment_type
        job.job_department = self.get_or_create_job_department(job_item)
        
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
    def generate_job_key(job, locations=None):
        return (
            job.job_title,
            tuple(l.id for l in job.locations.all()) if not locations else tuple(l.id for l in locations)
        )
