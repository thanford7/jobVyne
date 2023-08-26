import json

import requests

from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none
from jvapp.utils.money import parse_compensation_text
from scrape.base_scrapers import Scraper
from scrape.job_processor import JobItem


class DocuSignScraper(Scraper):
    ATS_NAME = 'Custom'
    employer_name = 'DocuSign'
    IS_API = True
    JOBS_PER_PAGE = 10  # This is the max
    
    async def scrape_jobs(self):
        total_jobs = None
        page_idx = 1
        jobs_count = 0
        while (not total_jobs) or (jobs_count < total_jobs):
            jobs_list, total_jobs = self.get_jobs(page_idx)
            page_idx += 1
            jobs_count += self.JOBS_PER_PAGE
        
            for job in jobs_list:
                await self.add_job_links_to_queue(self.get_job_link(job['slug']), meta_data={'job_data': job})
        
        await self.close()
    
    def get_job_link(self, job_id):
        return f'https://careers.docusign.com/jobs/{job_id}'
    
    def get_jobs(self, page_idx):
        request_data = {
            'page': page_idx,
            'sortBy': 'relevance',
            'descending': False,
            'internal': False
        }
        jobs_resp = requests.get(
            f'https://careers.docusign.com/api/jobs',
            params=request_data
        )
        jobs_data = json.loads(jobs_resp.content)
        return [j['data'] for j in jobs_data['jobs']], jobs_data['totalCount']
    
    def get_location_text(self, location_dict):
        return ', '.join([x for x in [location_dict.get('city'), location_dict.get('state'), location_dict.get('country')] if x])
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None, job_data=None):
        description = f'<p>{job_data["description"]}</p><p>{job_data["qualifications"]}</p><p>{job_data["responsibilities"]}</p>'
        description_compensation_data = parse_compensation_text(description)
        locations = [x.strip() for x in job_data['full_location'].split(';')]
        
        employment_type = job_data.get('employment_type')
        if employment_type:
            employment_type = ' '.join([x.capitalize() for x in employment_type.split('_')])
        else:
            employment_type = self.DEFAULT_EMPLOYMENT_TYPE
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['title'],
            locations=locations,
            job_department=job_data['category'][0].strip() if job_data['category'] else self.DEFAULT_JOB_DEPARTMENT,
            job_description=description,
            employment_type=employment_type,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['create_date'], as_date=True)),
            **description_compensation_data
        )