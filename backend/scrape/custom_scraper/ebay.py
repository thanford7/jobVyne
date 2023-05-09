from scrape.base_scrapers import Scraper
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from scrape.job_processor import JobItem


class EbayScraper(Scraper):
    employer_name = 'Ebay'
    start_url = 'https://jobs.ebayinc.com/us/en/search-results'
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '[data-ph-at-id="job-info"]'
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, '.phs-jobs-list-header')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, '.phs-jobs-list-header')
        
        page_count = 0
        next_button_selector = '.next-btn'
        while page_count == 0 or await page.locator(f'css={next_button_selector}').is_visible():
            if page_count != 0:
                await page.locator(f'css={next_button_selector}').click()
                await self.wait_for_el(page, self.job_item_page_wait_sel)
            html_dom = await self.get_page_html(page)
            await self.add_job_links_to_queue(html_dom.xpath('//li[@class="jobs-list-item"]//a/@href').getall())
            page_count += 1
        
        await self.close(page=page)
    
    def get_job_data_from_html(self, html, job_url=None, **kwargs):
        header_data = html.xpath('//*[@data-ph-at-id="job-header"]')
        
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = html.xpath('//*[contains(@class, "jd-info")]').get()
        description_compensation_data = self.parse_compensation_text(job_description)
        compensation_data = {}
        compensation_data = self.merge_compensation_data(
            [description_compensation_data, compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=header_data.xpath('//*[contains(@class, "job-title")]/text()').get(),
            locations=header_data.xpath('//li[contains(@class, "location")]/text()').getall(),
            job_department=header_data.xpath('//*[contains(@class, "job-category")]/text()').get(),
            job_description=job_description,
            employment_type=standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )

    async def request_failure_logger(self, request):
        return  # noop

    def response_failure_logger(self, response):
        return  # noop
