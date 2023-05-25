import asyncio
import json
import logging
import re
import tempfile
from datetime import timedelta
from json import JSONDecodeError
from urllib.parse import unquote

from aiohttp import ClientSession
from django.utils import timezone
from parsel import Selector
from playwright._impl._api_types import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError

from jvapp.utils.data import capitalize, coerce_float, get_base_url
from jvapp.utils.datetime import get_datetime_or_none
from jvapp.utils.file import get_file_storage_engine
from jvapp.utils.money import merge_compensation_data, parse_compensation_text
from scrape.job_processor import JobItem

logger = logging.getLogger(__name__)


REQUEST_HEADERS = {
    'Referer': 'https://www.google.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua-Mobile': '?0'
}


def normalize_url(url):
    url_parts = re.split('[/\?]', url)
    return tuple(part for part in url_parts if part and ('http' not in part))


class Scraper:
    MAX_CONCURRENT_PAGES = 10
    IS_JS_REQUIRED = False
    DEFAULT_JOB_DEPARTMENT = 'General'
    DEFAULT_EMPLOYMENT_TYPE = 'Full Time'
    TEST_REDIRECT = True
    PAGE_LOAD_WAIT_EVENT = 'load'
    IS_REMOVE_QUERY_PARAMS = True
    start_url = None
    employer_name = None
    job_item_page_wait_sel = None
    
    def __init__(self, playwright, browser, skip_urls):
        self.job_page_count = 0
        self.skipped_urls = []
        self.job_items = []
        self.queue = asyncio.Queue()
        self.playwright = playwright
        self.browser = browser
        self.session = ClientSession(headers=REQUEST_HEADERS)
        self.skip_urls = skip_urls
        logger.info(f'scraper {self.session} created')
        self.base_url = get_base_url(self.start_url)
        self.job_processors = [asyncio.create_task(self.get_job_item_from_url()) for _ in
                               range(self.MAX_CONCURRENT_PAGES)]
    
    async def get_new_page(self):
        page = await self.browser.new_page()
        page.on('dialog', lambda dialog: dialog.accept())
        return page
    
    async def save_page_info(self, page):
        # If page didn't load we won't have a URL
        if (not page.url) or (not re.match('^http.*?', page.url)):
            return
        
        storage = get_file_storage_engine()
        employer_name = '_'.join(self.employer_name.split(' '))
        
        screenshot_file_path = f'scraper_error/{employer_name}_screenshot_{timezone.now()}.png'
        screenshot = await page.screenshot(full_page=True)
        screenshot_file = tempfile.TemporaryFile()
        screenshot_file.write(screenshot)
        storage.save(screenshot_file_path, screenshot_file)
        
        html_file_path = f'scraper_error/{employer_name}_page_{timezone.now()}.html'
        # This won't load if the error is caused by a page load issue
        page_content = await page.content()
        html_file = tempfile.TemporaryFile()
        html_file.write(bytes(page_content, 'utf-8'))
        storage.save(html_file_path, html_file)
    
    async def request_failure_logger(self, request):
        logger.info(f'REQUEST FAILED: {request.url} {request.failure}')
    
    def response_failure_logger(self, response):
        if response.status >= 400 and 'reddit' not in response.request.url:
            logger.info(f'RESPONSE ERROR: {response.status} {response.status_text} for {response.request.url}')
    
    async def visit_page_with_retry(self, url, max_retries=4):
        # Some browser IPs may not work. If they don't we'll remove the browser and try another
        retries = 0
        error = None
        
        logger.info(f'Attempting to visit: "{url}"')
        logger.info(f'Number of open pages: {len(self.browser.pages)}')
        page = None
        e = None
        error_pages = []
        while retries < (max_retries + 1):
            page = await self.get_new_page()
            resp = None
            try:
                page.on('requestfailed', self.request_failure_logger)
                page.on('response', self.response_failure_logger)
                resp = await page.goto(url, referer=self.start_url, wait_until=self.PAGE_LOAD_WAIT_EVENT)
                if self.TEST_REDIRECT and (normalize_url(page.url) != normalize_url(url)):
                    logger.info('Page was redirected. Trying to reload page')
                    error_pages.append(page)
                    retries += 1
                    await asyncio.sleep(1)
                else:
                    for p in error_pages:
                        await p.close()
                    return page
            except (PlaywrightTimeoutError, PlaywrightError) as e:
                error_pages.append(page)
                error = e
                retries += 1
                logger.info(
                    f'Exception reaching page "{url}". Trying to reload page (retry {retries} of {max_retries})')
                if resp:
                    logger.info(f'Response: {resp.status} -- {resp.status_text}')
                await asyncio.sleep(1)
        
        await self.save_page_info(page)
        
        for p in error_pages:
            await p.close()
        
        raise error or ValueError(f'{str(e)} -- Exceeded max tries while trying to visit: "{url}"')
    
    async def scrape_jobs(self):
        raise NotImplementedError()
    
    async def get_starting_page(self):
        logger.info(f'Scraping jobs for {self.employer_name}')
        return await self.visit_page_with_retry(self.start_url)
    
    async def get_page_html(self, page):
        html = await page.locator('css=html').inner_html()
        return Selector(text=html)
    
    async def do_job_page_js(self, page):
        return None
    
    async def get_job_item_from_url(self):
        """Get HTML and process it to a job item. This will wait for the page to load any necessary JS.
        url: The page URL
        wait_sel: CSS selector for a page element which indicates the page is fully loaded
        meta_data: Any additional data that should be passed to the job item
        """
        while True:
            url, meta_data = await self.queue.get()
            current_page = self.job_page_count = self.job_page_count + 1
            logger.info(f'Fetching new job page ({current_page}): {url}')
            if self.IS_JS_REQUIRED:
                page = await self.visit_page_with_retry(url)
                if self.job_item_page_wait_sel:
                    page = await self.wait_for_el(page, self.job_item_page_wait_sel, max_retries=2)
                new_url = await self.do_job_page_js(page)
                if new_url:
                    url = new_url
                    page_html = await self.get_html_from_url(url)
                else:
                    page_html = await self.get_page_html(page)
                await page.close()
            else:
                page_html = await self.get_html_from_url(url)
            meta_data = meta_data or {}
            job_item = self.get_job_data_from_html(page_html, job_url=url, **meta_data)
            if job_item:
                self.job_items.append(job_item)
            logger.info(f'Job page scraped ({current_page}) -- {(job_item and job_item.job_title) or "no job found"}')
            self.queue.task_done()
    
    async def get_html_from_url(self, url):
        """Return an HTML selector. If no JavaScript interaction is needed, this method should
        be used since it is more lightweight than get_page_html
        """
        async with self.session.get(url) as resp:
            resp.raise_for_status()
            html = await resp.text()
            return Selector(text=html)
    
    async def wait_for_el(self, page, selector, max_retries=0, state='visible', timeout=30000):
        retries = 0
        while True:
            try:
                await page.wait_for_selector(selector, state=state)
                return page
            except PlaywrightTimeoutError as e:
                retries += 1
                logger.info(f'Could not find selector {selector} in: "{page.url}"')
                if retries > max_retries:
                    logger.info(f'Retries ({retries}) exceeded max retries ({max_retries})')
                    await self.save_page_info(page)
                    raise e
                logger.info('Retrying visiting page')
                page = await self.visit_page_with_retry(page.url)
    
    async def add_job_links_to_queue(self, job_links, meta_data=None):
        if not isinstance(job_links, list):
            job_links = [job_links]
        for job_link in job_links:
            job_url = self.get_absolute_url(job_link)
            if not all((job_url, self.is_english(job_url))):
                continue
            if job_url in self.skip_urls:
                logger.info(f'URL {job_url} has been recently scraped; skipping')
                self.skipped_urls.append(job_url)
                continue
            await self.queue.put((job_url, meta_data))
    
    async def close_connections(self, page=None):
        logger.info(f'close connections, page is {page}, session is {self.session}')
        await self.session.close()
        if page:
            await page.close()
        logger.info('Cancelling job processors')
        for job_processor in self.job_processors:
            job_processor.cancel()
    
    async def close(self, page=None):
        if not self.queue.empty():
            logger.info(f'Waiting for job queue to finish - Currently {self.queue.qsize()}')
            # wait for either `queue.join()` to complete or a consumer to raise
            done, _ = await asyncio.wait([self.queue.join(), *self.job_processors],
                                         return_when=asyncio.FIRST_COMPLETED)
            # The set of tasks that are 'done' but have not been removed from
            # `self.job_processors` are exceptions. There is only one (since we
            # used FIRST_COMPLETED), so we `await` it to propagate the exception.
            consumers_raised = set(done) & set(self.job_processors)
            if consumers_raised:
                logger.info(f'Found {len(consumers_raised)} consumers that raised exceptions')
                await consumers_raised.pop()  # propagate the exception
        await self.close_connections(page=page)
    
    def get_absolute_url(self, url):
        if not url:
            return None
        
        is_relative_url = url[0] == '/'
        if is_relative_url:
            url = self.base_url + url
        url = re.sub('[,"\']', '', unquote(url))
        url = re.sub('\s', '%A0', url)  # Make spaces in strings safe
        if self.IS_REMOVE_QUERY_PARAMS:
            url = url.split('?')[0]
        return url
    
    def is_english(self, text):
        try:
            text.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True
    
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
            try:
                job_data = json.loads(job_data)
            except JSONDecodeError:
                continue
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


class BambooHrScraper(Scraper):
    """ There are two entirely different HTML structures on different BambooHR Sites
    """
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '.jss-e8'
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, '.jss-e8')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, '.jss-e8')
        
        html_dom = await self.get_page_html(page)
        # html_dom = await self.get_html_from_url(self.start_url)
        await self.add_job_links_to_queue(html_dom.xpath('//div[@class="jss-e8"]//ul//a/@href').getall())
        await self.close(page=page)
    
    def get_job_data_from_html(self, html, job_url=None, **kwargs):
        job_data = html.xpath('//div[contains(@class, "jss-e8")]')
        job_details = html.xpath('//div[contains(@class, "jss-e73")]//p/text()').getall()
        job_detail_data = {}
        content_key = None
        for content_item in job_details:
            if not content_item:
                continue
            if not content_key:
                content_key = content_item.lower()
            else:
                job_detail_data[content_key] = content_item
                content_key = None
        
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = job_data.xpath('//div[contains(@class, "jss-e21")]').get()
        description_compensation_data = parse_compensation_text(job_description)
        compensation_data = {}
        if compensation_text := job_detail_data.get('compensation'):
            compensation_data = parse_compensation_text(compensation_text)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data.xpath('//h2[contains(@class, "jss-e18")]/text()').get(),
            locations=[job_data.xpath('//span[contains(@class, "jss-e19")]/text()').get()],
            job_department=job_detail_data.get('department', self.DEFAULT_JOB_DEPARTMENT),
            job_description=job_description,
            employment_type=job_detail_data.get('employment type', self.DEFAULT_EMPLOYMENT_TYPE),
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )


class BambooHrScraper2(Scraper):
    """ There are two entirely different HTML structures on different BambooHR Sites
    """
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '.ResAts__card'
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, '#resultDiv')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, '#resultDiv')
        
        html_dom = await self.get_page_html(page)
        # html_dom = await self.get_html_from_url(self.start_url)
        await self.add_job_links_to_queue(html_dom.xpath('//div[@id="resultDiv"]//ul//meta/@content').getall())
        await self.close(page=page)
    
    def get_job_data_from_html(self, html, job_url=None, **kwargs):
        job_data = html.xpath('//div[contains(@class, "js-jobs-left")]')
        job_details = html.xpath('//ul[contains(@class, "posInfoList")]//div/text()').getall()
        job_detail_data = {}
        content_key = None
        for content_item in job_details:
            if not content_item:
                continue
            if not content_key:
                content_key = content_item.lower()
            else:
                job_detail_data[content_key] = content_item
                content_key = None
        
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = job_data.xpath('.//div[contains(@class, "js-jobs-description")]').get()
        description_compensation_data = parse_compensation_text(job_description)
        compensation_data = {}
        if compensation_text := job_detail_data.get('compensation'):
            compensation_data = parse_compensation_text(compensation_text)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data.xpath('//h2/text()').get(),
            locations=[job_detail_data.get('location')],
            job_department=job_detail_data.get('department', self.DEFAULT_JOB_DEPARTMENT),
            job_description=job_description,
            employment_type=job_detail_data.get('employment type', self.DEFAULT_EMPLOYMENT_TYPE),
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )


class GreenhouseScraper(Scraper):
    TEST_REDIRECT = False
    IS_REMOVE_QUERY_PARAMS = False
    job_item_page_wait_sel = '#header'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.start_url)
        
        for department_section in html_dom.xpath('//section[@class="level-0"]'):
            department = department_section.xpath('.//h3/text()').get() or department_section.xpath(
                './/h2/text()').get()
            job_links = department_section.xpath('./div[@class="opening"]//a/@href').getall()
            await self.add_job_links_to_queue(
                [self.update_job_link(jl) for jl in job_links],
                meta_data={'job_department': department}
            )
            
            for sub_department_section in department_section.xpath('.//section[@class="child level-1"]'):
                department = sub_department_section.xpath('.//h4/text()').get()
                job_links = sub_department_section.xpath('.//div[@class="opening"]//a/@href').getall()
                await self.add_job_links_to_queue(
                    [self.update_job_link(jl) for jl in job_links],
                    meta_data={'job_department': department}
                )
        
        await self.close()
    
    def update_job_link(self, job_link):
        return job_link
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        location = html.xpath('//div[@id="header"]//div[@class="location"]/text()').get()
        if location:
            location = location.strip()
        standard_job_item = self.get_google_standard_job_item(html)
        if not any((location, standard_job_item.locations)):
            logger.info('Unable to parse JobItem from document. No location found.')
            return None
        job_description = html.xpath('//div[@id="content"]').get()
        description_compensation_data = parse_compensation_text(job_description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=html.xpath('//div[@id="header"]//h1/text()').get() or standard_job_item.job_title,
            locations=[location] if location else standard_job_item.locations,
            job_department=job_department or standard_job_item.job_department,
            job_description=job_description or standard_job_item.job_description,
            employment_type=standard_job_item.employment_type,
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )


class GreenhouseIframeScraper(GreenhouseScraper):
    TEST_REDIRECT = False
    GREENHOUSE_JOB_BOARD_DOMAIN = None
    job_item_page_wait_sel = None
    
    def update_job_link(self, job_link):
        # https://boards.greenhouse.io/embed/job_app?for=healthgorilla&token=4840862004
        parsed_url = re.match('^https?://(www)?(?P<domain>.+?)\..*?gh_jid=(?P<job_id>[0-9]+?)$', job_link)
        if not parsed_url:
            raise ValueError(f'Could not parse URL for {job_link}')
        link_values = parsed_url.groupdict()
        domain = self.GREENHOUSE_JOB_BOARD_DOMAIN or link_values["domain"]
        return f'https://boards.greenhouse.io/embed/job_app?for={domain}&token={link_values["job_id"]}'


class WorkdayScraper(Scraper):
    IS_JS_REQUIRED = True
    job_department_data_automation_id = 'jobFamilyGroup'
    job_department_form_data_automation_id = 'jobFamilyGroupCheckboxGroup'
    job_item_page_wait_sel = '[data-automation-id="jobPostingHeader"]'
    
    MAX_PAGE_LOAD_WAIT_SECONDS = 5
    
    async def scrape_jobs(self):
        page = await self.get_starting_page()
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, 'section[data-automation-id="jobResults"]')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
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
                        # TODO: Add retry for this
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
        
        await self.close(page=page)
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        job_data = html.xpath('//div[@data-automation-id="job-posting-details"]')
        # Note workday only shows the first 5 locations. JS automation would be necessary
        # to click the button to show additional locations
        locations = [l.get().strip() for l in job_data.xpath('.//div[@data-automation-id="locations"]/dl/dd/text()')]
        locations += [l.get().strip() for l in
                      job_data.xpath('.//div[@data-automation-id="additionalLocations"]/dl/dd/text()')]
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
        
        job_title = self.strip_or_none(html.xpath('.//*[@data-automation-id="jobPostingHeader"]/text()').get())
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = html.xpath('//*[@data-automation-id="jobPostingDescription"]').get()
        description_compensation_data = parse_compensation_text(job_description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_title,
            locations=locations,
            job_department=job_department,
            job_description=job_description,
            employment_type=standard_job_item.employment_type or self.strip_or_none(
                job_data.xpath('.//*[@data-automation-id="time"]/dl/dd/text()').get()),
            first_posted_date=standard_job_item.first_posted_date or posted_date,
            **compensation_data
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
        await self.wait_for_el(
            page,
            f'div[data-automation-id="{self.job_department_form_data_automation_id}"] label'
        )
    
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
            await page.locator(f'css={more_locations_sel}').click()
            try:
                await self.wait_for_el(page, '[data-automation-id="additionalLocations"]')
            except PlaywrightTimeoutError:
                pass
        
        return None
    
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


class LeverScraper(Scraper):
    TEST_REDIRECT = False
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.start_url)
        
        for department_section in html_dom.xpath('//div[@class="postings-wrapper"]//div[@class="postings-group"]'):
            job_links = set()
            department = department_section.xpath('.//div[contains(@class, "posting-category-title")]/text()').get()
            job_links.update(department_section.xpath('.//div[@class="posting"]//a/@href').getall())
            await self.add_job_links_to_queue(list(job_links), meta_data={'job_department': department})
        
        await self.close()
    
    def normalize_job_department(self, job_department):
        # Hook for child classes
        return job_department
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        standard_job_item = self.get_google_standard_job_item(html)
        headline = html.xpath('//div[@class="posting-headline"]')
        location = html.xpath('//div[contains(@class, "location")]/text()').get().replace('/', '').strip()
        employment_type = html.xpath('//div[contains(@class, "commitment")]/text()').get()
        employment_type = employment_type.replace('/', '').strip() if employment_type else None
        description_wrapper = html.xpath('//div[@class="content"]//div[contains(@class, "section-wrapper")][2]')
        description_sections = description_wrapper.xpath(
            './/div[contains(@class, "section") and not(contains(@class, "last-section-apply"))]').getall()
        description = ''
        for section in description_sections:
            description += section
        
        description_compensation_data = parse_compensation_text(description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=headline.xpath('//h2/text()').get(),
            locations=[location],
            job_department=self.normalize_job_department(job_department),
            job_description=description,
            employment_type=employment_type,
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )


class BreezyScraper(Scraper):
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.start_url)
        await self.add_job_links_to_queue(
            list(html_dom.xpath('//div[@class="positions-container"]//li[has-class("position")]//a/@href').getall()))
        await self.close()
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        standard_job_item = self.get_google_standard_job_item(html)
        headline = html.xpath('//div[@class="banner"]')
        location = headline.xpath('.//li[@class="location"]//text()').get().strip()
        employment_type = headline.xpath('.//li[@class="type"]//text()').get()
        if employment_type:
            employment_type = employment_type.strip()
            if employment_type == '%LABEL_POSITION_TYPE_PART_TIME%':
                employment_type = 'Part-Time'
            else:
                employment_type = 'Full-Time'
        compensation_data = {}
        compensation_text = headline.xpath('.//li[@class="salary-range"]//text()').getall()
        if compensation_text:
            compensation_text = ''.join([ct.strip() for ct in compensation_text])
            salary_interval = 'hour' if 'hr' in compensation_text else 'year'
            compensation_data = parse_compensation_text(compensation_text, salary_interval=salary_interval)
        description = html.xpath('//div[@class="description"]').get()
        description_compensation_data = parse_compensation_text(description)
        
        compensation_data = merge_compensation_data(
            [compensation_data, description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=headline.xpath('//h1/text()').get(),
            locations=[location],
            job_department=job_department,
            job_description=description,
            employment_type=employment_type,
            first_posted_date=standard_job_item.first_posted_date,
            **compensation_data
        )
