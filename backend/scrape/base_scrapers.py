import asyncio
import json
import logging
import re
from datetime import timedelta

from aiohttp import ClientSession
from django.utils import timezone
from parsel import Selector
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from jvapp.utils.data import capitalize, coerce_float, get_base_url
from jvapp.utils.datetime import get_datetime_or_none
from jvapp.utils.sanitize import sanitize_html
from scrape.job_processor import JobItem

logger = logging.getLogger(__name__)


class Scraper:
    MAX_CONCURRENT_PAGES = 30
    IS_JS_REQUIRED = False
    start_url = None
    employer_name = None
    job_item_page_wait_sel = None
    
    def __init__(self, browser):
        self.job_items = []
        self.queue = asyncio.Queue()
        self.browser = browser
        self.session = ClientSession(headers={
            'Referer': get_base_url(self.start_url),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        })
        self.base_url = get_base_url(self.start_url)
        self.job_processors = [asyncio.create_task(self.get_job_item_from_url()) for _ in
                               range(self.MAX_CONCURRENT_PAGES)]
    
    async def get_page(self):
        return await self.browser.new_page()
    
    async def scrape_jobs(self):
        raise NotImplementedError()
    
    async def get_starting_page(self):
        logger.info(f'Scraping jobs for {self.employer_name}')
        page = await self.get_page()
        await page.goto(self.start_url)
        return page
    
    async def get_page_html(self, page):
        html = await page.locator('css=html').inner_html()
        return Selector(text=html)
    
    async def do_job_page_js(self, page):
        return
    
    async def get_job_item_from_url(self):
        """Get HTML and process it to a job item. This will wait for the page to load any necessary JS.
        url: The page URL
        wait_sel: CSS selector for a page element which indicates the page is fully loaded
        meta_data: Any additional data that should be passed to the job item
        """
        while True:
            url, meta_data = await self.queue.get()
            logger.info(f'Fetching new job page ({len(self.job_items) + 1}): {url}')
            if self.IS_JS_REQUIRED:
                page = await self.get_page()
                await page.goto(url)
                if self.job_item_page_wait_sel:
                    await self.wait_for_el(page, self.job_item_page_wait_sel)
                await self.do_job_page_js(page)
                page_html = await self.get_page_html(page)
                await page.close()
            else:
                page_html = await self.get_html_from_url(url)
            meta_data = meta_data or {}
            job_item = self.get_job_data_from_html(page_html, job_url=url, **meta_data)
            self.job_items.append(job_item)
            self.queue.task_done()
    
    async def get_html_from_url(self, url):
        """Return an HTML selector. If no JavaScript interaction is needed, this method should
        be used since it is more lightweight than get_page_html
        """
        async with self.session.get(url) as resp:
            resp.raise_for_status()
            html = await resp.text()
            return Selector(text=html)
    
    async def wait_for_el(self, page, selector):
        el = await page.wait_for_selector(selector)
        if not el:
            raise ValueError(f'DOM element matching "{selector}" not found')
    
    async def add_job_links_to_queue(self, job_links, meta_data=None):
        if not isinstance(job_links, list):
            job_links = [job_links]
        for job_link in job_links:
            job_url = self.get_absolute_url(job_link)
            if not job_url:
                continue
            await self.queue.put((job_url, meta_data))
    
    async def close(self, page=None):
        if not self.queue.empty():
            logger.info(f'Waiting for job queue to finish - Currently {self.queue.qsize()}')
            await self.queue.join()  # Wait for queue to finish
        await self.session.close()
        if page:
            await page.close()
        logger.info('Cancelling job processors')
        for job_processor in self.job_processors:
            job_processor.cancel()
    
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
    
    def get_google_standard_job_item(self, html):
        """
        https://developers.google.com/search/docs/appearance/structured-data/job-posting#structured-data-type-definitions
        """
        standard_job_data = html.xpath('//script[@type="application/ld+json"]/text()').get()
        if not standard_job_data:
            return None
        
        if not isinstance(standard_job_data, list):
            standard_job_data = [standard_job_data]
        
        job_item = JobItem()
        for job_data in standard_job_data:
            job_data = json.loads(job_data)
            if job_data.get('@type') == 'JobPosting':
                job_item.job_title = self.strip_or_none(job_data.get('title'))
                job_item.job_description = job_data.get('description')
                job_item.first_posted_date = get_datetime_or_none(job_data.get('datePosted'), as_date=True)
                job_locations = job_data.get('jobLocation')
                if not job_locations:
                    job_locations = []
                elif not isinstance(job_locations, list):
                    job_locations = [job_locations]
                job_item.locations = []
                is_remote = job_data.get('jobLocationType', None) == 'TELECOMMUTE'
                for job_location in job_locations:
                    address = job_location.get('address')
                    if not address:
                        continue
                    address_str = None
                    for prop in ('streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'addressCountry'):
                        prop_val = address.get(prop)
                        if not address_str:
                            address_str = prop_val
                        else:
                            address_str += f', {prop_val}'
                    if address_str:
                        if is_remote:
                            address_str += f' (remote)'
                        job_item.locations.append(address_str)
                if employment_type := job_data.get('employmentType'):
                    if isinstance(employment_type, list):
                        employment_type = employment_type[0]
                    job_item.employment_type = capitalize(employment_type.replace('_', ' '))
            
                if base_salary := job_data.get('baseSalary'):
                    job_item.salary_currency = base_salary.get('currency')
                    if salary_data := base_salary.get('value'):
                        salary = coerce_float(salary_data.get('value'))
                        salary_floor = coerce_float(salary_data.get('minValue'))
                        salary_ceiling = coerce_float(salary_data.get('maxValue'))
                        job_item.salary_floor = salary_floor or salary
                        job_item.salary_ceiling = salary_ceiling or salary
                        interval = salary_data.get('unitText')
                        if interval:
                            job_item.salary_interval = interval.lower()
            
            # Can be used to get company logo instead of manually adding
            # company_data = job_data.get('@graph')
            # if company_data:
            #     for datum in standard_job_data:
            #         datum_type = datum.get('@type')
            #         if datum_type == 'Organization':
            #             logo = datum.get('logo')
            #             logo_url = logo.get('url') if logo else None
        
        return job_item


class GreenhouseScraper(Scraper):
    job_item_page_wait_sel = '#header'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.start_url)
        
        for department_section in html_dom.xpath('//section[@class="level-0"]'):
            department = department_section.xpath('.//h3/text()').get() or department_section.xpath(
                './/h2/text()').get()
            job_links = department_section.xpath('./div[@class="opening"]//a/@href').getall()
            await self.add_job_links_to_queue(job_links, meta_data={'job_department': department})
            
            for sub_department_section in department_section.xpath('.//section[@class="child level-1"]'):
                department = sub_department_section.xpath('.//h4/text()').get()
                job_links = sub_department_section.xpath('.//div[@class="opening"]//a/@href').getall()
                await self.add_job_links_to_queue(job_links, meta_data={'job_department': department})
        
        await self.close()
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        
        location = html.xpath('//div[@id="header"]//div[@class="location"]/text()').get().strip()
        standard_job_item = self.get_google_standard_job_item(html)
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=html.xpath('//div[@id="header"]//h1/text()').get(),
            locations=[location],
            job_department=job_department,
            job_description=sanitize_html(html.xpath('//div[@id="content"]').get()),
            employment_type=standard_job_item.employment_type,
            first_posted_date=standard_job_item.first_posted_date,
            salary_currency=standard_job_item.salary_currency,
            salary_floor=standard_job_item.salary_floor,
            salary_ceiling=standard_job_item.salary_ceiling,
            salary_interval=standard_job_item.salary_interval
        )


class WorkdayScraper(Scraper):
    IS_JS_REQUIRED = True
    job_department_data_automation_id = 'jobFamilyGroup'
    job_department_form_data_automation_id = 'jobFamilyGroupCheckboxGroup'
    job_item_page_wait_sel = '[data-automation-id="jobPostingHeader"]'
    
    MAX_PAGE_LOAD_WAIT_SECONDS = 5
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        # Make sure page data has loaded
        await self.wait_for_el(page, 'section[data-automation-id="jobResults"]')
        
        job_departments = await self.get_job_departments(page)
        
        # Iterate through each department and grab all jobs
        last_page_job_href = None
        for selector_idx, (job_department_name, job_quantity) in enumerate(job_departments):
            logger.info(f'Starting processing for: {job_department_name} | Expected quantity <{job_quantity}>')
            await self.select_job_department(page, selector_idx)
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
                        await self.reload_page(page)
                        has_page_loaded, html_dom = await self.get_next_page(page, last_page_job_href)
                    # If reload doesn't fix the issue, something is wrong
                    if not has_page_loaded:
                        logger.warning('Page load failure. Skipping scraping for the rest of this department\'s jobs')
                        break
                job_links = html_dom.css('section[data-automation-id="jobResults"] a::attr(href)').extract()
                await self.add_job_links_to_queue(job_links, meta_data={'job_department': job_department_name})
                
                last_page_job_href = self.get_first_job_href(html_dom)
                
                is_started = True
                next_page = html_dom.css('nav[aria-label="pagination"] button[aria-label="next"]').get()
                current_page_text = html_dom.xpath('//*[@data-automation-id="jobOutOfText"]/text()').get()
                if current_page_text:
                    logger.info(f'Loaded job data for: page <{current_page_text}>')
        
        await self.close(page)
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        job_data = html.xpath('//div[@data-automation-id="jobPostingPage"]')
        # Note workday only shows the first 5 locations. JS automation would be necessary
        # to click the button to show additional locations
        locations = [l.get().strip() for l in job_data.xpath('.//div[@data-automation-id="locations"]/dl/dd/text()')]
        locations += [l.get().strip() for l in job_data.xpath('.//div[@data-automation-id="additionalLocations"]/dl/dd/text()')]
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

        standard_job_item = self.get_google_standard_job_item(html)
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=self.strip_or_none(job_data.xpath('.//*[@data-automation-id="jobPostingHeader"]/text()').get()),
            locations=locations,
            job_department=job_department,
            job_description=sanitize_html(html.xpath('//*[@data-automation-id="jobPostingDescription"]').get()),
            employment_type=standard_job_item.employment_type or self.strip_or_none(job_data.xpath('.//*[@data-automation-id="time"]/dl/dd/text()').get()),
            first_posted_date=standard_job_item.first_posted_date or posted_date,
            salary_currency=standard_job_item.salary_currency,
            salary_floor=standard_job_item.salary_floor,
            salary_ceiling=standard_job_item.salary_ceiling,
            salary_interval=standard_job_item.salary_interval
        )
    
    async def get_next_page(self, page, last_page_job_href):
        try:
            async with page.expect_response(lambda r: re.match('.*?/jobs', r.url) and r.status == 200,
                                            timeout=5000) as response_info:
                await page.locator('css=nav[aria-label="pagination"] button[aria-label="next"]').click()
            await response_info.value
            html_dom = await self.get_page_html(page)
        except PlaywrightTimeoutError:
            logger.warning('Page load timeout while waiting for jobs response')
            return False, None
        page_load_wait_seconds = 0
        while (
                last_page_job_href == self.get_first_job_href(html_dom)
                and page_load_wait_seconds < self.MAX_PAGE_LOAD_WAIT_SECONDS
        ):
            logger.info('Waiting for next page to load')
            logger.info(f'Last page URL was: {last_page_job_href}')
            await asyncio.sleep(1)
            html_dom = await self.get_page_html(page)
            page_load_wait_seconds += 1
        
        # False indicates the page failed to load
        return page_load_wait_seconds != self.MAX_PAGE_LOAD_WAIT_SECONDS, html_dom
    
    async def open_job_department_menu(self, page):
        await page.locator(f'css=button[data-automation-id="{self.job_department_data_automation_id}"]').click()
        await self.wait_for_el(page, f'div[data-automation-id="{self.job_department_form_data_automation_id}"] label')
    
    async def get_job_departments(self, page):
        await self.open_job_department_menu(page)
        html_dom = await self.get_page_html(page)
        job_departments = html_dom.xpath(
            f'//div[@data-automation-id="{self.job_department_form_data_automation_id}"]//label/text()')
        job_departments = [re.match('^(?P<department_name>.+?) \((?P<job_quantity>[0-9]+)\)$', jd.get().strip()) for jd
                           in job_departments]
        return [(jd.group('department_name'), jd.group('job_quantity')) for jd in job_departments]
    
    async def select_job_department(self, page, selector_idx):
        clear_button_sel = 'button[data-automation-id="clearButton"]'
        is_menu_open = await page.locator(f'css={clear_button_sel}').is_visible()
        if not is_menu_open:
            await self.open_job_department_menu(page)
        await self.wait_for_el(page, clear_button_sel)
        await page.locator(f'css={clear_button_sel}').click()  # Clear selected
        await page.locator(
            f'css=div[data-automation-id="{self.job_department_form_data_automation_id}"] [role="row"]:nth-child({selector_idx + 1}) [role="cell"] > div > div').click()  # Select the department menu item
        async with page.expect_response(lambda r: re.match('.*?/jobs', r.url) and r.status == 200) as response_info:
            await page.locator('css=button[data-automation-id="viewAllJobsButton"]').click()  # Apply selection
        await response_info.value
    
    async def reload_page(self, page):
        await page.reload()
        await self.wait_for_el(page, 'section[data-automation-id="jobResults"]')
        
    async def do_job_page_js(self, page):
        more_locations_sel = '[data-automation-id="locationButton-collapsed"]'
        has_more_locations = await page.locator(f'css={more_locations_sel}').is_visible()
        if has_more_locations:
            page.locator(f'css={more_locations_sel}').click()
        await self.wait_for_el(page, '[data-automation-id="additionalLocations"]')
    
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
