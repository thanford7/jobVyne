import json

import requests

from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none
from jvapp.utils.money import parse_compensation_text
from scrape.base_scrapers import Scraper
from scrape.job_processor import JobItem


class PacksizeScraper(Scraper):
    ATS_NAME = 'Custom'
    employer_name = 'Packsize'
    IS_REMOVE_QUERY_PARAMS = False
    
    async def scrape_jobs(self):
        jobs = self.get_jobs()
        for job in jobs:
            await self.add_job_links_to_queue(self.get_job_link(job), meta_data={'job_id': job['id']})
        
        await self.close()
    
    def get_job_link(self, job_data):
        return f'https://www.packsize.com/browse-jobs/?jobId={job_data["id"]}/'
    
    def get_jobs(self):
        jobs_resp = requests.get(
            'https://careers-api.clearcompany.com/v1/5f0810da-bb55-02f2-0b2e-336973c249e1'
        )
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['results']
    
    def get_raw_job_data(self, job_id):
        job_resp = requests.get(f'https://careers-api.clearcompany.com/v1/5f0810da-bb55-02f2-0b2e-336973c249e1/{job_id}')
        return json.loads(job_resp.content)
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None):
        job_data = self.get_raw_job_data(job_id)
        description = job_data['description']
        description_compensation_data = parse_compensation_text(description)
        location_text = ', '.join([
            job_data.get('locationCity') or '',
            job_data.get('locationSubdivisionFullName') or '',
            job_data.get('locationCountry') or ''
        ])
        if job_data['isRemote']:
            location_text = f'Remote: {location_text}'
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['positionTitle'],
            locations=[location_text],
            job_department=job_data['departmentName'],
            job_description=description,
            employment_type=self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['postedDate'], as_date=True)),
            **description_compensation_data
        )
