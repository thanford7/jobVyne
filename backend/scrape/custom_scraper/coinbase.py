from jvapp.utils.money import merge_compensation_data, parse_compensation_text
from scrape.base_scrapers import Scraper
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from scrape.job_processor import JobItem

#  Note uses CloudFlare to block proxy scrapers. Not using Coinbase until we can figure out how to bypass
class CoinbaseScraper(Scraper):
    IS_JS_REQUIRED = True
    employer_name = 'Coinbase'
    start_url = 'https://www.coinbase.com/careers/positions'
    job_item_page_wait_sel = '[class*="Listing__JobDescription"]'
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        page_load_sel = '[class*="Positions__PositionsColumn"]'
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, page_load_sel)
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, page_load_sel)
        
        # Open all departments
        for department_link in await page.locator('css=[class*="Department__DepartmentHeader"]').all():
            await department_link.click()
            
        await self.wait_for_el(page, '[class*="Department__JobsWrapper"]')
        html_dom = await self.get_page_html(page)
        all_positions = html_dom.xpath('//div[contains(@class, "Positions__PositionsColumn")]')
        for department in all_positions.xpath('.//div[contains(@class, "Department__Wrapper")]'):
            department_name = department.xpath('.//div[contains(@class, "Department__DepartmentHeader")]/descendant::p[1]/text()').get()
            for job in department.xpath('.//div[contains(@class, "Department__Job")]'):
                location = job.xpath('./p/text()').get()
                await self.add_job_links_to_queue(
                    job.xpath('.//a/@href').get(),
                    meta_data={'job_department': department_name, 'location_text': location}
                )
        
        await self.close(page=page)
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, location_text=None, **kwargs):
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = html.xpath('.//div[contains(@class, "Listing__JobDescription")]').get()
        description_compensation_data = parse_compensation_text(job_description)
        compensation_data = {}
        compensation_data = merge_compensation_data(
            [description_compensation_data, compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=standard_job_item.job_title or html.xpath('.//h1[contains(@class, "Listing__Title")]/text()').get(),
            locations=standard_job_item.locations or [location_text.strip()],
            job_department=standard_job_item.job_department or job_department.strip(),
            job_description=standard_job_item.job_description or job_description,
            employment_type=standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )
    
    async def request_failure_logger(self, request):
        return  # noop
    
    def response_failure_logger(self, response):
        return  # noop