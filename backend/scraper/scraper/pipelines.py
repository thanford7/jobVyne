# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from asgiref.sync import sync_to_async
from django.utils import timezone

from jvapp.apis.geocoding import LocationParser
from jvapp.models import Employer, EmployerJob, JobDepartment


class ScraperPipeline:
    employers = None
    scraped_employers = None
    location_parser = None
    job_departments = None
    job_update_attributes = ['application_url', 'job_department', 'job_description']

    def open_spider(self, spider):
        self.employers = {employer.employer_name: {
            'employer': employer,
            'jobs': {self.generate_job_key(j): j for j in employer.employer_job.all() if j.is_scraped},
            'found_jobs': set()
        } for employer in Employer.objects.prefetch_related('employer_job', 'employer_job__locations').all()}
        self.scraped_employers = set()
        self.location_parser = LocationParser()
        self.job_departments = {j.name.lower(): j for j in JobDepartment.objects.all()}

    def close_spider(self, spider):
        # Set the close date of a job if it no longer exists on the employers job page
        for employer_data in self.employers.values():
            if employer_data['employer'].employer_name not in self.scraped_employers:
                continue
            for job_key, job in employer_data['jobs'].items():
                if job_key not in employer_data['found_jobs'] and not job.close_date:
                    job.close_date = timezone.now().date()
                    job.save()

        if driver := getattr(spider, 'driver', None):
            driver.close()

    @sync_to_async
    def process_item(self, item, spider):
        employer_name = item['employer_name']
        employer_data = self.employers.get(employer_name)
        if not employer_data:
            employer = Employer(employer_name=employer_name)
            employer.save()
            self.employers[employer_name] = {
                'employer': employer,
                'jobs': {},
                'found_jobs': set()
            }
        else:
            employer = employer_data['employer']
        self.scraped_employers.add(employer_name)

        if not item['employment_type']:
            return item
        
        location = self.location_parser.get_location(item['location'])

        new_job = EmployerJob(
            job_title=item['job_title'],
            is_scraped=True
        )
        if not (job := employer_data['jobs'].get(self.generate_job_key(new_job, location=location))):
            new_job.employer = employer
            self.update_job(new_job, item)
            employer_data['jobs'][self.generate_job_key(new_job, location=location)] = new_job
            job = new_job
        else:
            self.update_job(job, item)
            
        job.locations.add(location)

        employer_data['found_jobs'].add(self.generate_job_key(job, location=location))

        return item

    def is_same_job(self, job, job_data):
        job_department = self.get_or_create_job_department(job_data)
        if any([
            job.application_url != job_data['application_url'],
            job.job_description != job_data['job_description'],
            job.job_department != job_department,
            not job.open_date,
            job.close_date
        ]):
            return False

        return True

    def update_job(self, job, job_data):
        if self.is_same_job(job, job_data):
            return job
        
        job.application_url = job_data['application_url']
        job.job_description = job_data['job_description']
        job.job_department = self.get_or_create_job_department(job_data)

        job.open_date = job.open_date or timezone.now().date()
        job.close_date = None
        job.save()
        return job
    
    def get_or_create_job_department(self, job_data):
        if not (job_department_name := job_data.get('job_department')):
            return None
        
        if not (job_department := self.job_departments.get(job_department_name.lower())):
            job_department = JobDepartment(name=job_department_name)
            job_department.save()
            self.job_departments[job_department_name.lower()] = job_department
        
        return job_department

    @staticmethod
    def generate_job_key(job, location=None):
        return (
            job.job_title,
            tuple(l.id for l in job.locations.all()) if not location else (location.id,)
        )
