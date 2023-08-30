import json

import requests

from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none
from jvapp.utils.money import parse_compensation_text
from scrape.base_scrapers import Scraper
from scrape.job_processor import JobItem


class MicrosoftScraper(Scraper):
    ATS_NAME = 'Custom'
    employer_name = 'Microsoft'
    IS_REMOVE_QUERY_PARAMS = False
    JOBS_PER_PAGE = 20
    
    async def scrape_jobs(self):
        total_jobs = None
        page_idx = 1
        jobs_count = 0
        while (not total_jobs) or (jobs_count < total_jobs):
            jobs_list, total_jobs = self.get_jobs(page_idx)
            page_idx += 1
            jobs_count += self.JOBS_PER_PAGE
            
            for job in jobs_list:
                await self.add_job_links_to_queue(self.get_job_link(job['jobId']), meta_data={'job_data': job})
        
        await self.close()
    
    def get_job_link(self, job_id):
        return f'https://jobs.careers.microsoft.com/global/en/job/{job_id}'
    
    def get_jobs(self, page_idx):
        query_params = {
            'l': 'en_us',
            'pg': page_idx,
            'pgSz': self.JOBS_PER_PAGE,
            'o': 'Relevance'
        }
        jobs_resp = requests.get(
            'https://gcsservices.careers.microsoft.com/search/api/v1/search',
            params=query_params
        )
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['operationResult']['result']['jobs'], jobs_data['operationResult']['result']['totalJobs']
    
    def get_raw_job_data(self, job_id):
        job_resp = requests.get(f'https://gcsservices.careers.microsoft.com/search/api/v1/job/{job_id}')
        data = json.loads(job_resp.content)
        return data['operationResult']['result']
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None, job_data=None):
        extra_job_data = self.get_raw_job_data(job_data['jobId'])
        description = job_data['properties']['description']
        description_compensation_data = parse_compensation_text(description)
        description = ''.join([x for x in [description, extra_job_data['responsibilities'], extra_job_data['qualifications']] if x])
        locations = job_data['properties']['locations']
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['title'],
            locations=locations,
            job_department=job_data['properties']['profession'],
            job_description=description,
            employment_type=job_data['properties']['employmentType'],
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['postingDate'], as_date=True)),
            **description_compensation_data
        )
