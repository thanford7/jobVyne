import logging

from scrape.base_scrapers import Scraper
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from scrape.job_processor import JobItem

logger = logging.getLogger(__name__)


class PinterestScraper(Scraper):
    employer_name = 'Pinterest'
    start_url = 'https://www.pinterestcareers.com/job-search-results/'
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '.jd-description'
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        page_load_sel = '.widget-jobsearch-results'
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, page_load_sel)
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, page_load_sel)
        
        page_count = 0
        while page_count == 0 or await page.locator(f'css=#pagination{page_count + 1}').is_visible():
            if page_count != 0:
                next_page_url = self.start_url + f'?pg={page_count + 1}'
                logger.info(f'Going to next page: {next_page_url}')
                await self.close(page)
                page = await self.visit_page_with_retry(next_page_url)
                await self.wait_for_el(page, page_load_sel)
            html_dom = await self.get_page_html(page)
            await self.add_job_links_to_queue(html_dom.xpath('//div[has-class("job")]//div[has-class("jobTitle")]//a/@href').getall())
            page_count += 1
        
        await self.close(page=page)
    
    def get_job_data_from_html(self, html, job_url=None, **kwargs):
        job_data = html.xpath('//*[@class="job-fields"]')
        employment_type = job_data.xpath('.//div[@id="gtm-jobdetail-employment-type"]/span/text()').get()
        if employment_type and employment_type.lower() == 'regular':
            employment_type = self.DEFAULT_EMPLOYMENT_TYPE
        
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = html.xpath('//div[has-class("jd-description")]').get()
        description_compensation_data = self.parse_compensation_text(job_description)
        compensation_data = {}
        compensation_data = self.merge_compensation_data(
            [description_compensation_data, compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=html.xpath('//div[has-class("title")]/h1//text()').get(),
            locations=job_data.xpath('.//div[@id="gtm-jobdetail-location"]//span/text()').getall(),
            job_department=job_data.xpath('.//div[@id="gtm-jobdetail-category"]/span/text()').get(),
            job_description=job_description,
            employment_type=employment_type or standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )
    
    async def request_failure_logger(self, request):
        return  # noop
    
    def response_failure_logger(self, response):
        return  # noop
