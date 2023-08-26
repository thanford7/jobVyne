import json

import requests

from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none
from jvapp.utils.money import parse_compensation_text
from scrape.base_scrapers import Scraper
from scrape.job_processor import JobItem


class AmazonScraper(Scraper):
    ATS_NAME = 'Custom'
    IS_API = True
    JOBS_PER_PAGE = 100
    employer_name = 'Amazon'
    
    async def scrape_jobs(self):
        total_jobs = None
        start_job_idx = 0
        jobs = []
        while (not total_jobs) or (start_job_idx < total_jobs):
            jobs_list, total_jobs = self.get_jobs(start_job_idx)
            jobs += jobs_list
            start_job_idx += self.JOBS_PER_PAGE
        
        for job in jobs:
            await self.add_job_links_to_queue(self.get_job_link(job), meta_data={'job_data': job})
        
        await self.close()
    
    def get_job_link(self, job_data):
        return f'https://www.amazon.jobs{job_data["job_path"]}'
    
    def get_jobs(self, next_page_start):
        request_data = {
            'sort_by': 'relevance',
            'result_limit': self.JOBS_PER_PAGE,
            'offset': next_page_start,
            'normalized_country_code[]': ['USA', 'CAN']
        }
        jobs_resp = requests.get(
            f'https://www.amazon.jobs/en/search.json',
            params=request_data
        )
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['jobs'], jobs_data['hits']
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None, job_data=None):
        job_description = job_data['description']
        description_compensation_data = parse_compensation_text(job_description)
        
        job_qualifications = job_data['basic_qualifications']
        preferred_qualifications = job_data['preferred_qualifications']
        job_description = f'<p>{job_description}</p><h4>Qualifications</h4><p>{job_qualifications}</p><h4>Preferred Qualifications</h4><p>{preferred_qualifications}</p>'
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data["title"],
            locations=[job_data['normalized_location']],
            job_department=job_data['job_category'] or self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=job_data['job_schedule_type'] or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['posted_date'], as_date=True)),
            **description_compensation_data
        )
