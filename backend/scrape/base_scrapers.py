import asyncio
import logging
import re
from datetime import timedelta

from django.utils import timezone
from parsel import Selector
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from jvapp.utils.data import get_base_url
from jvapp.utils.sanitize import sanitize_html
from scrape.job_processor import JobItem

logger = logging.getLogger(__name__)


class Scraper:
    MAX_CONCURRENT_PAGES = 30
    start_url = None
    
    def __init__(self, browser, session):
        self.job_items = []
        self.queue = asyncio.Queue()
        self.browser = browser
        self.session = session
        self.base_url = get_base_url(self.start_url)
    
    async def get_page(self):
        return await self.browser.new_page()
    
    async def scrape_jobs(self):
        raise NotImplementedError()
    
    async def get_page_html(self, page):
        html = await page.locator('css=body').inner_html()
        return Selector(text=html)
    
    async def get_page_from_url_js(self):
        """Get HTML and process it to a job item. This will wait for the page to load any necessary JS.
        url: The page URL
        wait_sel: CSS selector for a page element which indicates the page is fully loaded
        meta_data: Any additional data that should be passed to the job item
        """
        while True:
            url, wait_sel, meta_data = await self.queue.get()
            logger.info(f'Fetching new job page ({len(self.job_items) + 1}): {url}')
            page = await self.get_page()
            await page.goto(url)
            await self.wait_for_el(page, wait_sel)
            page_html = await self.get_page_html(page)
            await page.close()
            meta_data = meta_data or {}
            job_item = self.get_job_data_from_html(page_html, job_url=url, **meta_data)
            self.job_items.append(job_item)
    
    async def get_html_from_url(self, url):
        """Return an HTML selector. If no JavaScript interaction is needed, this method should
        be used since it is more lightweight than get_page_html
        """
        resp = await self.session.request(method='GET', url=url)
        resp.raise_for_status()
        html = await resp.text()
        return Selector(text=html)
    
    async def wait_for_el(self, page, selector):
        el = await page.wait_for_selector(selector)
        if not el:
            raise ValueError(f'DOM element matching "{selector}" not found')
    
    def get_absolute_url(self, url):
        if not url:
            return None
        
        is_relative_url = url[0] == '/'
        if is_relative_url:
            url = self.base_url + url
        return url
    
    def strip_or_none(self, val):
        if not val:
            return None
        return val.strip()
    
    def get_job_data_from_html(self, html, job_url=None, **kwargs):
        raise NotImplementedError()


class WorkdayScraper(Scraper):
    employer_name = None
    
    MAX_PAGE_LOAD_WAIT_SECONDS = 5
    
    async def scrape_jobs(self):
        logger.info(f'Scraping jobs for {self.employer_name}')
        job_processors = [asyncio.create_task(self.get_page_from_url_js()) for _ in range(self.MAX_CONCURRENT_PAGES)]
        page = await self.get_page()
        await page.goto(self.start_url)
        # Make sure page data has loaded
        await self.wait_for_el(page, 'section[data-automation-id="jobResults"]')
        
        # Get all job departments
        await page.locator('css=button[data-automation-id="jobFamilyGroup"]').click()
        await self.wait_for_el(page, 'div[data-automation-id="jobFamilyGroupCheckboxGroup"] label')
        html_dom = await self.get_page_html(page)
        job_departments = html_dom.xpath('//div[@data-automation-id="jobFamilyGroupCheckboxGroup"]//label/text()')
        job_departments = [re.match('^(?P<department_name>.+?) \((?P<job_quantity>[0-9]+)\)$', jd.get().strip()) for jd in job_departments]
        job_departments = [(jd.group('department_name'), jd.group('job_quantity')) for jd in job_departments]
        
        # Iterate through each department and grab all jobs
        last_page_job_href = None
        for selector_idx, (job_department_name, job_quantity) in enumerate(job_departments):
            logger.info(f'Starting processing for: {job_department_name} | Expected quantity <{job_quantity}>')
            clear_button_sel = 'button[data-automation-id="clearButton"]'
            is_menu_open = await page.locator(f'css={clear_button_sel}').is_visible()
            if not is_menu_open:
                await page.locator('css=button[data-automation-id="jobFamilyGroup"]').click()  # Open department menu
            await self.wait_for_el(page, clear_button_sel)
            await page.locator(f'css={clear_button_sel}').click()  # Clear selected
            await page.locator(
                f'css=div[data-automation-id="jobFamilyGroupCheckboxGroup"] [role="row"]:nth-child({selector_idx + 1}) [role="cell"] > div > div').click()  # Select the department menu item
            async with page.expect_response(lambda r: re.match('.*?/jobs', r.url) and r.status == 200) as response_info:
                await page.locator('css=button[data-automation-id="viewAllJobsButton"]').click()  # Apply selection
            response = await response_info.value
            html_dom = await self.get_page_html(page)
            
            # Make sure jobs are refreshed
            page_load_wait_seconds = 0
            while (
                (not self.is_job_quantity_match(html_dom, job_quantity))
                or (last_page_job_href and last_page_job_href == self.get_first_job_href(html_dom))
            ) and page_load_wait_seconds < self.MAX_PAGE_LOAD_WAIT_SECONDS:
                logger.info(f'Waiting for page to load: {page.url}')
                await asyncio.sleep(1)
                html_dom = await self.get_page_html(page)
                page_load_wait_seconds += 1

            # If the page is taking this long to load, something is wrong
            if page_load_wait_seconds == self.MAX_PAGE_LOAD_WAIT_SECONDS:
                logger.info(f'Waited {page_load_wait_seconds} seconds for page to load. Terminating')
                break

            # Parse jobs for each page
            is_started = False
            next_page = None
            while (not is_started) or next_page:
                if next_page:
                    has_page_loaded, html_dom = await self.get_next_page(page, last_page_job_href)
                    # Workday has a bug where pagination can stop working
                    # Try reloading the page once
                    if not has_page_loaded:
                        logger.info('Failed to go to next page. Trying page reload')
                        await page.reload()
                        has_page_loaded, html_dom = await self.get_next_page(page, last_page_job_href)
                    # If reload doesn't fix the issue, something is wrong
                    if not has_page_loaded:
                        logger.warning('Page load failure. Skipping scraping for the rest of this department\'s jobs')
                        break
                for job_link in html_dom.css('section[data-automation-id="jobResults"] a::attr(href)').extract():
                    job_url = self.get_absolute_url(job_link)
                    if not job_url:
                        continue
                    await self.queue.put(
                        (job_url, '[data-automation-id="jobPostingHeader"]', {'job_department': job_department_name})
                    )

                last_page_job_href = self.get_first_job_href(html_dom)
                
                is_started = True
                next_page = html_dom.css('nav[aria-label="pagination"] button[aria-label="next"]').get()
                current_page_text = html_dom.xpath('//*[@data-automation-id="jobOutOfText"]/text()').get()
                if current_page_text:
                    logger.info(f'Loaded job data for: page <{current_page_text}>')
        
        logger.info('Closing main page')
        await page.close()
        logger.info('Waiting for job queue to finish')
        await self.queue.join()  # Wait for queue to finish
        logger.info('Cancelling job processors')
        for job_processor in job_processors:
            job_processor.cancel()
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        job_data = html.xpath('//div[@data-automation-id="jobPostingPage"]')
        # Note workday only shows the first 5 locations. JS automation would be necessary
        # to click the button to show additional locations
        locations = [l.get().strip() for l in job_data.xpath('.//div[@data-automation-id="locations"]/dl/dd/text()')]
        posted_date = job_data.xpath('.//*[@data-automation-id="postedOn/dl/dd/text()"]').get()
        today = timezone.now().date()
        if posted_date:
            posted_date = posted_date.strip().lower()
            days_ago_match = re.match('^.*?(?P<days>[0-9]+)\+? days.*$', posted_date)
            if days_ago_match:
                days_ago = int(days_ago_match.group('days'))
                posted_date = today - timedelta(days=days_ago)
            elif 'today' in posted_date:
                posted_date = today
            elif 'yesterday' in posted_date:
                posted_date = today - timedelta(days=1)
            else:
                posted_date = None
                
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=self.strip_or_none(job_data.xpath('.//*[@data-automation-id="jobPostingHeader"]/text()').get()),
            locations=locations,
            job_department=job_department,
            job_description=sanitize_html(html.xpath('//*[@data-automation-id="jobPostingDescription"]').get()),
            employment_type=self.strip_or_none(job_data.xpath('.//*[@data-automation-id="time"]/dl/dd/text()').get()),
            first_posted_date=posted_date
        )
    
    async def get_next_page(self, page, last_page_job_href):
        try:
            async with page.expect_response(lambda r: re.match('.*?/jobs', r.url) and r.status == 200, timeout=5000) as response_info:
                await page.locator('css=nav[aria-label="pagination"] button[aria-label="next"]').click()
            response = await response_info.value
            html_dom = await self.get_page_html(page)
        except PlaywrightTimeoutError:
            return False, None
        page_load_wait_seconds = 0
        while (
                last_page_job_href == self.get_first_job_href(html_dom)
                and page_load_wait_seconds < self.MAX_PAGE_LOAD_WAIT_SECONDS
        ):
            logger.info('Waiting for next page to load')
            await asyncio.sleep(1)
            html_dom = await self.get_page_html(page)
            page_load_wait_seconds += 1
    
        # False indicates the page failed to load
        return page_load_wait_seconds != self.MAX_PAGE_LOAD_WAIT_SECONDS, html_dom
    
    def is_job_quantity_match(self, html_dom, expected_job_quantity):
        job_quantity_string = html_dom.xpath('//*[@data-automation-id="jobOutOfText"]/text()').get()
        if not job_quantity_string and expected_job_quantity is not None:
            return False
        job_quantity_match = re.match('^.+? of (?P<job_quantity>[0-9]+) .*$', job_quantity_string)
        if not job_quantity_match and expected_job_quantity is not None:
            return False
        return job_quantity_match.group('job_quantity') == expected_job_quantity
    
    def get_first_job_href(self, html_dom):
        job_hrefs = html_dom.css('section[data-automation-id="jobResults"] a::attr(href)').extract()
        if not job_hrefs:
            return None
        return job_hrefs[0]
