from jvapp.utils.money import merge_compensation_data, parse_compensation_text
from scrape.base_scrapers import Scraper
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from scrape.job_processor import JobItem


class AncestryScraper(Scraper):
    ATS_NAME = 'Custom'
    USE_HEADERS = False
    employer_name = 'Ancestry'
    start_url = 'https://careers.ancestry.com/jobs/search'
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        page_load_sel = '[data-controller="jobs--table-results"]'
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, page_load_sel)
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, page_load_sel)

        html_dom = await self.get_page_html(page)
        await self.add_job_links_to_queue(html_dom.xpath('//td[@class="job-search-results-title"]//a/@href').getall())
        
        await self.close(page=page)
    
    def get_job_data_from_html(self, html, job_url=None, **kwargs):
        job_data = html.xpath('//div[@class="block-job-description"]')
        
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = job_data.xpath('.//*[contains(@class, "job-description")]').get()
        description_compensation_data = parse_compensation_text(job_description)
        compensation_data = {}
        compensation_data = merge_compensation_data(
            [description_compensation_data, compensation_data, standard_job_item.get_compensation_dict()]
        )
        job_department = job_data.xpath('.//li[contains(@class, "job-component-department")]//span/text()').get() or 'General'
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data.xpath('.//*[contains(@class, "job-title")]/text()').get(),
            locations=[
                location_text.strip() for location_text in
                job_data.xpath('.//div[contains(@class, "job-component-list-location")]//li//span/text()').getall()
            ],
            job_department=job_department.strip(),
            job_description=job_description,
            employment_type=standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )
