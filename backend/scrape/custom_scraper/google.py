import math
import re

from django.utils import timezone

from jvapp.utils.data import coerce_int
from jvapp.utils.money import parse_compensation_text
from scrape.base_scrapers import Scraper
from scrape.job_processor import JobItem


class GoogleScraper(Scraper):
    employer_name = 'Google'
    start_url = 'https://www.google.com/about/careers/applications/jobs/results/?hl=en_US'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        job_count_text = ''.join(html_dom.xpath('//div[@jsname="uEp2ad"]/text()').getall())
        job_count_match = re.match('^(?P<start_count>[0-9]+?)\W(?P<end_count>[0-9]+?)\sof\s(?P<total_count>[0-9]+?)$', job_count_text)
        start_count = coerce_int(job_count_match.group('start_count'))
        end_count = coerce_int(job_count_match.group('end_count'))
        total_count = coerce_int(job_count_match.group('total_count'))
        pages_count = math.ceil(total_count / (end_count - start_count))
        print(f'Calculated {pages_count} total pages for {total_count} jobs')
        for idx in range(pages_count):
            page_num = idx + 1
            url = f'{self.get_start_url()}&page={page_num}'
            html_dom = await self.get_html_from_url(url)
            await self.add_job_links_to_queue(
                [self.get_job_link(l) for l in html_dom.xpath('//div[@class="Ln1EL"]//a[@jsname="hSRGPd"]/@href').getall()]
            )
            
        await self.close()

    def get_job_link(self, rel_url):
        return f'https://www.google.com/about/careers/applications/{rel_url}'

    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None):
        job_info_html = html.xpath('//div[@class="DkhPwc"]')
        job_details_html = job_info_html.xpath('.//div[@class="op1BBf"]')
        locations_text = ''.join(job_details_html.xpath('.//span[contains(@class, "pwO9Dc")]/span/text()').getall())
        raw_locations = [l for l in locations_text.split(';') if l]
        locations = [l for l in raw_locations if not re.search('\+[0-9].*?more', l, re.IGNORECASE)]
        has_more = len(locations) != len(raw_locations)
        in_person_locations = []
        remote_locations = []
        if has_more:
            more_job_locations = job_info_html.xpath('.//div[@jscontroller="u3jeub"]//b/text()').getall()
            for job_locations in more_job_locations:
                if in_person_locations_match := re.match('^.*?office locations:(?P<location_text>.+?)\.$', job_locations, re.IGNORECASE):
                    in_person_locations = [l.strip() for l in in_person_locations_match.group('location_text').split(';') if l]
                if remote_locations_match := re.match('^.*?remote location.*?:(?P<location_text>.+?)\.$', job_locations, re.IGNORECASE):
                    remote_locations = [f'Remote: {l.strip()}' for l in remote_locations_match.group('location_text').split(';') if l]
            locations = in_person_locations + remote_locations
        else:
            is_remote = False
            job_detail_indicators = job_details_html.xpath('.//span[@class="RP7SMd"]/span/text()').getall()
            for job_detail in job_detail_indicators:
                if job_detail and 'remote' in job_detail:
                    is_remote = True
            if is_remote:
                locations = [f'Remote: {l}' for l in locations]
            
        qualifications = job_info_html.xpath('.//div[@class="KwJkGe"]').get()
        job_description = job_info_html.xpath('.//div[@class="aG5W3"]').get()
        responsibilities = job_info_html.xpath('.//div[@class="BDNOWe"]').get()
        description_compensation_data = parse_compensation_text(job_description)
        full_job_description = ''.join([d for d in [job_description, qualifications, responsibilities] if d])
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_info_html.xpath('.//h2[@class="p1N2lc"]/text()').get(),
            locations=locations,
            job_department=self.DEFAULT_JOB_DEPARTMENT,
            job_description=full_job_description,
            employment_type=self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=timezone.now().now(),
            **description_compensation_data
        )
