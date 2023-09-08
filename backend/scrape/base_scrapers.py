import asyncio
import datetime
import html as html_parser
import json
import logging
import random
import re
import tempfile
from datetime import timedelta
from json import JSONDecodeError
from math import ceil
from urllib.parse import unquote

import requests
from aiohttp import ClientSession, ServerDisconnectedError
from django.conf import settings
from django.utils import timezone
from parsel import Selector
from playwright._impl._api_types import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError
from playwright.async_api import expect

from jvapp.apis.geocoding import LocationParser
from jvapp.models.employer import EmployerJob
from jvapp.utils.data import capitalize, coerce_float, coerce_int, get_base_url, get_website_domain_from_url
from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_from_unix, get_datetime_or_none
from jvapp.utils.file import get_file_storage_engine
from jvapp.utils.money import merge_compensation_data, parse_compensation_text
from scrape.job_processor import JobItem

logger = logging.getLogger(__name__)

# ---- Note: Most ATSs don't require all of these
ADVANCED_REQUEST_HEADERS = {
    'Referer': 'https://www.google.com',
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

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
]

SKIP_SCRAPE_CUTOFF = datetime.timedelta(days=7)


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def normalize_url(url):
    url_parts = re.split('[/\?]', url)
    return tuple(part for part in url_parts if part and ('http' not in part))


def get_recent_scraped_job_urls(employer_name):
    return {
        job for job in EmployerJob.objects
        .filter(
            modified_dt__gt=timezone.now() - SKIP_SCRAPE_CUTOFF,
            is_scraped=True,
            close_date__isnull=True,
            employer__employer_name=employer_name
        ).values_list('application_url', flat=True)
    }


class Scraper:
    USE_HEADERS = True
    USE_ADVANCED_HEADERS = False
    MAX_CONCURRENT_PAGES = 10
    IS_JS_REQUIRED = False
    IS_API = False
    DEFAULT_JOB_DEPARTMENT = 'General'
    DEFAULT_EMPLOYMENT_TYPE = 'Full Time'
    TEST_REDIRECT = True
    PAGE_LOAD_WAIT_EVENT = 'load'
    IS_REMOVE_QUERY_PARAMS = True
    EMPLOYER_KEY = None
    ATS_NAME = None
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
        self.base_url = get_base_url(self.get_start_url())
        self.skip_urls = [] if settings.IS_LOCAL else skip_urls
        self.job_processors = [asyncio.create_task(self.get_job_item_from_url()) for _ in
                               range(self.MAX_CONCURRENT_PAGES)]
        
    def get_client_session(self):
        headers = {
            'User-Agent': get_random_user_agent(),
            'Referer': self.base_url,
            'Origin': self.base_url,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*'
        } if self.USE_HEADERS else {}
        if self.USE_ADVANCED_HEADERS:
            headers = {**headers, **ADVANCED_REQUEST_HEADERS}
            
        return ClientSession(headers=headers)
    
    async def update_browser_context(self):
        await self.browser.set_extra_http_headers({
            'Referer': self.base_url,
            'Origin': self.base_url,
        })
    
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
        if '/track' in request.url:
            return
        logger.info(f'REQUEST FAILED: {request.url} {request.failure}')
    
    async def response_failure_logger(self, response):
        if response.status >= 400 and 'reddit' not in response.request.url:
            logger.info(f'RESPONSE ERROR: {response.status} {response.status_text} for {response.request.url}')
            request_headers = await response.request.all_headers()
            logger.info(f'RESPONSE ERROR: Request headers - {request_headers}')
    
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
                resp = await page.goto(url, wait_until=self.PAGE_LOAD_WAIT_EVENT)
                await self.response_failure_logger(resp)
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
        return await self.visit_page_with_retry(self.get_start_url())
    
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
            if self.IS_API:
                page_html = None
            elif self.IS_JS_REQUIRED:
                page = await self.visit_page_with_retry(url)
                if self.job_item_page_wait_sel:
                    page = await self.wait_for_el(page, self.job_item_page_wait_sel, max_retries=2)
                new_url = await self.do_job_page_js(page)
                if new_url:
                    url = new_url
                    page_html = await self.get_html_from_url_with_retry(url)
                else:
                    page_html = await self.get_page_html(page)
                await page.close()
            else:
                page_html = await self.get_html_from_url_with_retry(url)
            meta_data = meta_data or {}
            job_item = self.get_job_data_from_html(page_html, job_url=url, **meta_data)
            if job_item:
                self.job_items.append(job_item)
            logger.info(f'Job page scraped ({current_page}) -- {(job_item and job_item.job_title) or "no job found"}')
            self.queue.task_done()
            
    async def get_html_from_url_with_retry(self, url):
        try:
            resp = await self.get_html_from_url(url)
            return resp
        except ServerDisconnectedError:
            resp = await self.get_html_from_url(url)
            return resp
    
    async def get_html_from_url(self, url):
        """Return an HTML selector. If no JavaScript interaction is needed, this method should
        be used since it is more lightweight than get_page_html
        """
        async with self.get_client_session() as client:
            async with client.get(url) as resp:
                if not resp.ok:
                    logger.warning(f'Failed to load page: {url}\n({resp.status}) {resp.reason}')
                # resp.raise_for_status()
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
        url = re.sub('\s', '%20', url)  # Make spaces in strings safe
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
                company_data = job_data.get('hiringOrganization')
                if company_data and isinstance(company_data, dict):
                    job_item.logo_url = company_data.get('logo')
                    if website_url := company_data.get('sameAs'):
                        if isinstance(website_url, list):
                            website_url = website_url[0]
                        website_domain = get_website_domain_from_url(website_url)
                        job_item.website_domain = website_domain
        
        return job_item
    
    # Override
    def get_start_url(self):
        return self.start_url


class BambooHrScraper(Scraper):
    """ There are two entirely different HTML structures on different BambooHR Sites
    """
    ATS_NAME = 'BambooHR'
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '.fab-Card'
    
    async def scrape_jobs(self):
        await self.update_browser_context()
        jobs = self.get_jobs()
        for job in jobs:
            await self.add_job_links_to_queue(self.get_job_url(job), meta_data={'job_id': job['id']})
        await self.close()
    
    def get_job_url(self, job):
        return f'https://{self.EMPLOYER_KEY}.bamboohr.com/careers/{job["id"]}'
    
    def get_job_data(self, job_id):
        job_resp = requests.get(f'https://{self.EMPLOYER_KEY}.bamboohr.com/careers/{job_id}/detail')
        job = json.loads(job_resp.content)
        return job['result']['jobOpening']
    
    def get_jobs(self):
        jobs_resp = requests.get(f'https://{self.EMPLOYER_KEY}.bamboohr.com/careers/list')
        jobs = json.loads(jobs_resp.content)
        return jobs['result']
    
    def get_job_data_from_html(self, html, job_url=None, job_id=None, **kwargs):
        job_data = self.get_job_data(job_id)
        standard_job_item = self.get_google_standard_job_item(html)
        job_description = job_data['description']
        description_compensation_data = parse_compensation_text(job_description)
        compensation_data = {}
        if compensation_text := job_data.get('compensation'):
            compensation_data = parse_compensation_text(compensation_text)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, compensation_data, standard_job_item.get_compensation_dict()]
        )
        location_data = job_data['location']
        location = ', '.join([
            location_data.get('city') or '',
            location_data.get('state') or '',
            location_data.get('addressCountry') or ''
        ])
        if job_data['isRemote']:
            location = 'Remote: ' + location
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['jobOpeningName'],
            locations=[location],
            job_department=job_data.get('departmentLabel', self.DEFAULT_JOB_DEPARTMENT),
            job_description=job_description,
            employment_type=job_data.get('employmentStatusLabel', self.DEFAULT_EMPLOYMENT_TYPE),
            first_posted_date=standard_job_item.first_posted_date or job_data.get('datePosted'),
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class BambooHrScraper2(Scraper):
    """ There are two entirely different HTML structures on different BambooHR Sites
    """
    ATS_NAME = 'BambooHR'
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '.ResAts__card'
    
    async def scrape_jobs(self):
        await self.update_browser_context()
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, '#resultDiv')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, '#resultDiv')
        
        html_dom = await self.get_page_html(page)
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
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class GreenhouseScraper(Scraper):
    ATS_NAME = 'Greenhouse'
    TEST_REDIRECT = False
    IS_REMOVE_QUERY_PARAMS = False
    job_item_page_wait_sel = '#header'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        
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
    
    def get_start_url(self):
        return f'https://boards.greenhouse.io/{self.EMPLOYER_KEY}/'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, api_data=None):
        location = html.xpath('//div[@id="header"]//div[@class="location"]/text()').get()
        locations = self.process_location_text(location)
        print(f'Locations: {locations}')
        standard_job_item = self.get_google_standard_job_item(html)
        if not standard_job_item:
            logger.info('Unable to parse JobItem from document. No standard job data (ld+json).')
            return None
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
            locations=locations if locations else standard_job_item.locations,
            job_department=job_department or standard_job_item.job_department,
            job_description=job_description or standard_job_item.job_description,
            employment_type=standard_job_item.employment_type,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )
    
    def process_location_text(self, location_text):
        if not location_text:
            return None
        if ';' in location_text:
            return [l for l in [location.strip() for location in location_text.split(';')] if l]
        elif 'or ' in location_text:
            return [l for l in [location.strip() for location in location_text.split('or ')] if l]
        return [location_text.strip()]


class GreenhouseIframeScraper(GreenhouseScraper):
    ATS_NAME = 'Greenhouse'
    TEST_REDIRECT = False
    job_item_page_wait_sel = None
    
    def get_start_url(self):
        return f'https://boards.greenhouse.io/embed/job_board?for={self.EMPLOYER_KEY}'
    
    def update_job_link(self, job_link):
        # https://boards.greenhouse.io/embed/job_app?for=healthgorilla&token=4840862004
        parsed_url = re.match('^https?://(www)?(?P<domain>.+?)\..*?gh_jid=(?P<job_id>[0-9]+?)$', job_link)
        if not parsed_url:
            raise ValueError(f'Could not parse URL for {job_link}')
        link_values = parsed_url.groupdict()
        domain = self.EMPLOYER_KEY or link_values["domain"]
        return f'https://boards.greenhouse.io/embed/job_app?for={domain}&token={link_values["job_id"]}'


class GreenhouseApiScraper(GreenhouseScraper):
    """Some employers don't enable an iframe embed so we have to resort to using the API instead
    """
    ATS_NAME = 'Greenhouse'
    IS_REMOVE_QUERY_PARAMS = False
    IS_API = True
    
    async def scrape_jobs(self):
        jobs_list = self.get_jobs()
        
        for job in jobs_list:
            await self.add_job_links_to_queue(job['absolute_url'], meta_data={'job_id': job['id']})
        
        await self.close()
    
    def get_jobs(self):
        jobs_resp = requests.get(
            f'https://api.greenhouse.io/v1/boards/{self.EMPLOYER_KEY}/jobs',
            params={'content': True}
        )
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['jobs']
    
    def get_job_data(self, job_id):
        job_resp = requests.get(
            f'https://boards-api.greenhouse.io/v1/boards/{self.EMPLOYER_KEY}/jobs/{job_id}',
            params={'pay_transparency': True}
        )
        return json.loads(job_resp.content)
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None):
        job_data = self.get_job_data(job_id)
        pay_ranges = [
            {
                'salary_floor': coerce_int(range['min_cents']) / 60,
                'salary_ceiling': coerce_int(range['max_cents']) / 60,
                'currency': range['currency_type']
            } for range in job_data.get('pay_input_ranges') or []
        ]
        
        compensation_data = {
            'salary_currency': None,
            'salary_floor': None,
            'salary_ceiling': None,
            'salary_interval': None
        }
        if pay_ranges:
            compensation_data = {
                'salary_currency': pay_ranges[0]['currency'],
                'salary_floor': min([pr['salary_floor'] for pr in pay_ranges]),
                'salary_ceiling': max([pr['salary_ceiling'] for pr in pay_ranges]),
                'salary_interval': 'year'
            }
        
        job_description = html_parser.unescape(job_data['content'])
        description_compensation_data = parse_compensation_text(job_description)
        
        compensation_data = merge_compensation_data(
            [compensation_data, description_compensation_data]
        )
        
        locations = []
        if job_data['location']:
            locations.append(job_data['location']['name'])
        locations += [o['location'] or o['name'] for o in job_data['offices']]
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['title'],
            locations=self.process_locations(locations),
            job_department=job_data['departments'][0]['name'] if job_data[
                'departments'] else self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['updated_at'], as_date=True)),
            **compensation_data
        )
    
    def process_locations(self, locations):
        # Subclass
        return locations


class WorkdayScraper(Scraper):
    ATS_NAME = 'Workday'
    IS_JS_REQUIRED = True
    job_department_menu_data_automation_id = 'jobFamilyGroup'
    job_department_form_data_automation_id = 'jobFamilyGroupCheckboxGroup'
    job_item_page_wait_sel = '[data-automation-id="jobPostingHeader"]'
    has_job_departments = True
    
    MAX_PAGE_LOAD_WAIT_SECONDS = 5
    
    async def scrape_jobs(self):
        await self.update_browser_context()
        page = await self.get_starting_page()
        # Make sure page data has loaded
        page_container_sel = 'section[data-automation-id="jobResults"] [data-automation-id="jobFoundText"]'
        page_load_sel = '[data-automation-id="searchingForJobs"]'
        try:
            await self.wait_for_el(page, page_container_sel)
            await expect(page.locator(page_load_sel)).to_have_count(0)
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, page_container_sel)
            await expect(page.locator(page_load_sel)).to_have_count(0)
        
        if self.has_job_departments:
            job_departments = await self.get_job_departments(page)
        else:
            job_departments = [('General', 'NA')]
        
        # Iterate through each department and grab all jobs
        last_page_job_href = None
        for selector_idx, (job_department_name, job_quantity) in enumerate(job_departments):
            logger.info(f'Starting processing for: {job_department_name} | Expected quantity <{job_quantity}>')
            if self.has_job_departments:
                await self.select_job_department(page, selector_idx)
            html_dom = await self.get_page_html(page)
            
            # Make sure jobs are refreshed
            if self.has_job_departments:
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
                job_links = html_dom.xpath('//section[@data-automation-id="jobResults"]//a/@href').getall()
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
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
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
        await page.locator(f'css=button[data-automation-id="{self.job_department_menu_data_automation_id}"]').click()
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


class WorkdayApiScraper(Scraper):
    ATS_NAME = 'Workday'
    IS_API = True
    JOBS_BASE_API_URL = None
    JOBS_PER_PAGE = 20
    
    async def scrape_jobs(self):
        has_started = False
        total_jobs = None
        start_job_idx = 0
        while (not has_started) or (start_job_idx < total_jobs):
            jobs_list, total_jobs = self.get_jobs(start_job_idx)
            for job in jobs_list:
                await self.add_job_links_to_queue(self.get_job_link(job['externalPath']), meta_data={'external_path': job['externalPath']})
            start_job_idx += self.JOBS_PER_PAGE
            has_started = True
        
        await self.close()
    
    def get_jobs(self, start_job_idx):
        jobs_resp = requests.post(
            f'{self.JOBS_BASE_API_URL}/jobs',
            json={
                'appliedFacets': {},
                'limit': self.JOBS_PER_PAGE,
                'offset': start_job_idx,
                'searchText': ''
            }
        )
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['jobPostings'], jobs_data['total']
    
    def get_job_link(self, external_path):
        return f'{self.get_start_url()}{external_path}'
    
    def get_job_data(self, external_path):
        job_resp = requests.get(
            f'{self.JOBS_BASE_API_URL}{external_path}',
            params={'pay_transparency': True}
        )
        return json.loads(job_resp.content)['jobPostingInfo']
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None, external_path=None):
        job_data = self.get_job_data(external_path)
        job_description = html_parser.unescape(job_data['jobDescription'])
        description_compensation_data = parse_compensation_text(job_description)
        
        locations = list(set([job_data['location']] + job_data.get('additionalLocations', [])))
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['title'],
            locations=locations,
            job_department=self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=job_data['timeType'] or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['startDate'], as_date=True)),
            **description_compensation_data
        )


class LeverScraper(Scraper):
    ATS_NAME = 'Lever'
    TEST_REDIRECT = False
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        
        for department_section in html_dom.xpath('//div[@class="postings-wrapper"]//div[@class="postings-group"]'):
            job_links = set()
            department = department_section.xpath('.//div[contains(@class, "posting-category-title")]/text()').get()
            job_links.update(department_section.xpath('.//div[@class="posting"]//a/@href').getall())
            await self.add_job_links_to_queue(list(job_links), meta_data={'job_department': department})
        
        await self.close()
    
    def get_start_url(self):
        return f'https://jobs.lever.co/{self.EMPLOYER_KEY}/'
    
    def normalize_job_department(self, job_department):
        # Hook for child classes
        return job_department
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        standard_job_item = self.get_google_standard_job_item(html)
        headline = html.xpath('//div[@class="posting-headline"]')
        location = html.xpath('//div[contains(@class, "location")]/text()').get().replace('/', '').strip()
        employment_type_options = [
            html.xpath('//div[contains(@class, "commitment")]/text()').get(),
            standard_job_item.employment_type,
            self.DEFAULT_EMPLOYMENT_TYPE
        ]
        # The employer is probably using the commitment field incorrectly if the length is greater than 30
        employment_type = [et for et in employment_type_options if et and len(et) <= 30][0]
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
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class BreezyScraper(Scraper):
    ATS_NAME = 'Breezy HR'
    USE_ADVANCED_HEADERS = True
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        await self.add_job_links_to_queue(
            list(html_dom.xpath('//div[@class="positions-container"]//li[has-class("position")]//a/@href').getall()))
        await self.close()
    
    def get_start_url(self):
        return f'https://{self.EMPLOYER_KEY}.breezy.hr/'
    
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
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class WorkableScraper(Scraper):
    ATS_NAME = 'Workable'
    IS_API = True
    BASE_FILTER_DATA = {
        'department': [],
        'location': [],
        'query': [],
        'remote': [],
        'worktype': []
    }
    
    async def scrape_jobs(self):
        has_more = True
        next_page_key = None
        jobs = []
        while has_more:
            jobs_list, next_page_key = self.get_jobs(next_page_key=next_page_key)
            jobs += jobs_list
            has_more = bool(next_page_key)
        
        for job in jobs:
            await self.add_job_links_to_queue(self.get_job_link(job), meta_data={'job_shortcode': job['shortcode']})
        
        await self.close()
    
    def get_job_link(self, job_data):
        return f'https://apply.workable.com/{self.EMPLOYER_KEY}/j/{job_data["shortcode"]}/'
    
    def get_jobs(self, next_page_key=None):
        request_data = {**self.BASE_FILTER_DATA}
        if next_page_key:
            request_data['token'] = next_page_key
        jobs_resp = requests.post(
            f'https://apply.workable.com/api/v3/accounts/{self.EMPLOYER_KEY}/jobs',
            data=request_data
        )
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['results'], jobs_data.get('nextPage')
    
    def get_raw_job_data(self, job_shortcode):
        job_resp = requests.get(f'https://apply.workable.com/api/v2/accounts/{self.EMPLOYER_KEY}/jobs/{job_shortcode}')
        return json.loads(job_resp.content)
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_shortcode=None):
        job_data = self.get_raw_job_data(job_shortcode)
        job_description = job_data['description']
        job_requirements = job_data['requirements']
        job_benefits = job_data['benefits']
        description = ''
        for section in [job_description, job_requirements, job_benefits]:
            try:
                description += section
            except TypeError as e:
                raise e
        description_compensation_data = parse_compensation_text(description)
        location_data = job_data.get('location')
        is_remote = job_data['remote']
        if (not location_data) and is_remote:
            location_text = 'Remote'
        elif location_data:
            location_parts = [location_data.get('city'), location_data.get('region'), location_data.get('country')]
            location_text = ', '.join([p for p in location_parts if p])
            if job_data['remote']:
                location_text = f'Remote: {location_text}'
        else:
            logger.info('Unable to parse JobItem from document. No location provided.')
            return None
        
        job_department = job_data['department']
        if job_department:
            job_department = job_department[0]
        else:
            job_department = self.DEFAULT_JOB_DEPARTMENT
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['title'],
            locations=[location_text],
            job_department=job_department,
            job_description=description,
            employment_type=job_data.get('type') or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['published'], as_date=True)),
            **description_compensation_data
        )


class AshbyHQScraper(Scraper):
    ATS_NAME = 'Ashby'
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '[class*="_descriptionText"]'
    
    async def scrape_jobs(self):
        await self.update_browser_context()
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, '[class*="_titles"]')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, '[class*="_titles"]')
        
        html_dom = await self.get_page_html(page)
        
        await self.add_job_links_to_queue(
            list(html_dom.xpath('//div[contains(@class, "ashby-job-posting-brief-list")]//a/@href').getall()))
        await self.close()
    
    def get_start_url(self):
        return f'https://jobs.ashbyhq.com/{self.EMPLOYER_KEY}/'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        standard_job_item = self.get_google_standard_job_item(html)
        job_details = {}
        compensation_text_data = {}
        for job_detail in html.xpath('//div[contains(@class, "ashby-job-posting-left-pane")]/div'):
            job_detail_name = job_detail.xpath('.//h2[contains(@class, "_heading")]/text()').get().strip().lower()
            if job_detail_name == 'location':
                job_details['location'] = job_detail.xpath('.//p/text()').get()
            elif job_detail_name == 'type':
                job_details['employment_type'] = job_detail.xpath('.//p/text()').get()
            elif job_detail_name == 'department':
                job_details['department'] = ' - '.join(job_detail.xpath('.//p/span/text()').getall())
            elif job_detail_name == 'compensation':
                compensation_text = job_detail.xpath(
                    './/span[contains(@class, "_compensationTierSummary")]/text()').get()
                compensation_text_data = parse_compensation_text(compensation_text)
        
        description = html.xpath('//div[contains(@class, "_descriptionText")]').get()
        description_compensation_data = parse_compensation_text(description)
        
        compensation_data = merge_compensation_data(
            [compensation_text_data, description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=html.xpath('//h1[contains(@class, "ashby-job-posting-heading")]/text()').get(),
            locations=[job_details['location']],
            job_department=job_details['department'],
            job_description=description,
            employment_type=job_details['employment_type'],
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class AshbyHQApiScraper(Scraper):
    ATS_NAME = 'Ashby'
    IS_API = True
    
    async def scrape_jobs(self):
        jobs = self.get_jobs()
        company_data = self.get_company_data()
        
        for job in jobs:
            await self.add_job_links_to_queue(
                self.get_job_link(job), meta_data={'job_id': job['id'], 'website_url': company_data['publicWebsite']}
            )
        
        await self.close()
    
    def get_job_link(self, job_data):
        return f'https://jobs.ashbyhq.com/{self.EMPLOYER_KEY}/{job_data["id"]}'
    
    def get_jobs(self):
        post_data = {
            'operationName': 'ApiJobBoardWithTeams',
            'query': 'query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    teams {\n      id\n      name\n      parentTeamId\n      __typename\n    }\n    jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\n  locationId\n  locationName\n  __typename\n}',
            'variables': {'organizationHostedJobsPageName': self.EMPLOYER_KEY}
        }
        
        resp = requests.post(
            f'https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams',
            json=post_data
        )
        data = json.loads(resp.content)
        return data['data']['jobBoard']['jobPostings']
    
    def get_company_data(self):
        post_data = {
            'operationName': 'ApiOrganizationFromHostedJobsPageName',
            'query': 'query ApiOrganizationFromHostedJobsPageName($organizationHostedJobsPageName: String!) {\n  organization: organizationFromHostedJobsPageName(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    ...OrganizationParts\n    __typename\n  }\n}\n\nfragment OrganizationParts on Organization {\n  name\n  publicWebsite\n  customJobsPageUrl\n  allowJobPostIndexing\n  theme {\n    colors\n    showJobFilters\n    showTeams\n    showAutofillApplicationsBox\n    logoWordmarkImageUrl\n    logoSquareImageUrl\n    applicationSubmittedSuccessMessage\n    jobBoardTopDescriptionHtml\n    jobBoardBottomDescriptionHtml\n    __typename\n  }\n  appConfirmationTrackingPixelHtml\n  recruitingPrivacyPolicyUrl\n  activeFeatureFlags\n  timezone\n  __typename\n}',
            'variables': {'organizationHostedJobsPageName': self.EMPLOYER_KEY}
        }
        
        resp = requests.post(
            f'https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiOrganizationFromHostedJobsPageName',
            json=post_data
        )
        data = json.loads(resp.content)
        return data['data']['organization']
    
    def get_raw_job_data(self, job_id):
        post_data = {
            'operationName': 'ApiJobPosting',
            'query': 'query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {\n  jobPosting(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n    jobPostingId: $jobPostingId\n  ) {\n    id\n    title\n    departmentName\n    locationName\n    employmentType\n    descriptionHtml\n    isListed\n    isConfidential\n    teamNames\n    applicationForm {\n      ...FormRenderParts\n      __typename\n    }\n    surveyForms {\n      ...FormRenderParts\n      __typename\n    }\n    secondaryLocationNames\n    compensationTierSummary\n    compensationTiers {\n      id\n      title\n      tierSummary\n      __typename\n    }\n    compensationTierGuideUrl\n    scrapeableCompensationSalarySummary\n    compensationPhilosophyHtml\n    applicationLimitCalloutHtml\n    __typename\n  }\n}\n\nfragment JSONBoxParts on JSONBox {\n  value\n  __typename\n}\n\nfragment FileParts on File {\n  id\n  filename\n  __typename\n}\n\nfragment FormFieldEntryParts on FormFieldEntry {\n  id\n  field\n  fieldValue {\n    ... on JSONBox {\n      ...JSONBoxParts\n      __typename\n    }\n    ... on File {\n      ...FileParts\n      __typename\n    }\n    ... on FileList {\n      files {\n        ...FileParts\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  isRequired\n  descriptionHtml\n  isHidden\n  __typename\n}\n\nfragment FormRenderParts on FormRender {\n  id\n  formControls {\n    identifier\n    title\n    __typename\n  }\n  errorMessages\n  sections {\n    title\n    descriptionHtml\n    fieldEntries {\n      ...FormFieldEntryParts\n      __typename\n    }\n    isHidden\n    __typename\n  }\n  sourceFormDefinitionId\n  __typename\n}',
            'variables': {'organizationHostedJobsPageName': self.EMPLOYER_KEY, 'jobPostingId': str(job_id)}
        }
        
        jobs_resp = requests.post(
            f'https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting',
            json=post_data
        )
        data = json.loads(jobs_resp.content)
        return data['data']['jobPosting']
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None, website_url=None):
        job_data = self.get_raw_job_data(job_id)
        job_description = job_data['descriptionHtml']
        description_compensation_data = parse_compensation_text(job_description)
        location = job_data['locationName']
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['title'],
            locations=[location],
            job_department=job_data['departmentName'] or self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=self.DEFAULT_EMPLOYMENT_TYPE,
            website_domain=get_website_domain_from_url(website_url),
            **description_compensation_data
        )
    
    
class AshbyHQApiV2Scraper(Scraper):
    ATS_NAME = 'Ashby'
    IS_API = True
    
    async def scrape_jobs(self):
        jobs = self.get_jobs()
        company_data = self.get_company_data()
        
        for job in jobs:
            await self.add_job_links_to_queue(
                job['jobUrl'], meta_data={'job_data': job, 'website_url': company_data['publicWebsite'] if company_data else None}
            )
        
        await self.close()
    
    def get_jobs(self):
        resp = requests.get(
            f'https://api.ashbyhq.com/posting-api/job-board/{self.EMPLOYER_KEY}',
            params={'includeCompensation': True}
        )
        data = json.loads(resp.content)
        return data['jobs']
    
    def get_company_data(self):
        post_data = {
            'operationName': 'ApiOrganizationFromHostedJobsPageName',
            'query': 'query ApiOrganizationFromHostedJobsPageName($organizationHostedJobsPageName: String!) {\n  organization: organizationFromHostedJobsPageName(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    ...OrganizationParts\n    __typename\n  }\n}\n\nfragment OrganizationParts on Organization {\n  name\n  publicWebsite\n  customJobsPageUrl\n  allowJobPostIndexing\n  theme {\n    colors\n    showJobFilters\n    showTeams\n    showAutofillApplicationsBox\n    logoWordmarkImageUrl\n    logoSquareImageUrl\n    applicationSubmittedSuccessMessage\n    jobBoardTopDescriptionHtml\n    jobBoardBottomDescriptionHtml\n    __typename\n  }\n  appConfirmationTrackingPixelHtml\n  recruitingPrivacyPolicyUrl\n  activeFeatureFlags\n  timezone\n  __typename\n}',
            'variables': {'organizationHostedJobsPageName': self.EMPLOYER_KEY}
        }
        
        resp = requests.post(
            f'https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiOrganizationFromHostedJobsPageName',
            json=post_data
        )
        data = json.loads(resp.content)
        return data['data']['organization']
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None, job_data=None, website_url=None):
        job_description = job_data['descriptionHtml']
        description_compensation_data = parse_compensation_text(job_description) or {}
        if compensation_data := (job_data.get('compensation') or {}):
            if compensation_summary := compensation_data.get('summaryComponents'):
                comp = next((c for c in compensation_summary if c['compensationType'].lower() == 'salary'), None)
                if comp:
                    compensation_data = {
                        'salary_currency': comp['currencyCode'],
                        'salary_floor': comp['minValue'],
                        'salary_ceiling': comp['maxValue'],
                        'salary_interval': 'year'
                    }
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, compensation_data]
        )
        
        location = job_data['location']
        if job_data['isRemote'] and (not LocationParser.get_is_remote(location)):
            location = f'Remote: {location}'
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['title'],
            locations=[location],
            job_department=job_data['department'] or self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=job_data['employmentType'] or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['publishedAt'], as_date=True)),
            website_domain=get_website_domain_from_url(website_url),
            **compensation_data
        )


class UltiProScraper(Scraper):
    ATS_NAME = 'UltiPro'
    IS_REMOVE_QUERY_PARAMS = False
    TEST_REDIRECT = False
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '[data-automation="job-description"]'
    
    async def scrape_jobs(self):
        await self.update_browser_context()
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        # Issue: REQUEST FAILED: https://www.linkedin.com/li/track net::ERR_ABORTED
        try:
            await self.wait_for_el(page, '#OpportunitiesContainer')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, '#OpportunitiesContainer')
        
        # Load all jobs
        is_more = await page.locator('css=#LoadMoreJobs').is_visible()
        while is_more:
            await page.locator('css=#LoadMoreJobs').click()
            is_more = await page.locator('css=#LoadMoreJobs').is_visible()
        
        html_dom = await self.get_page_html(page)
        
        await self.add_job_links_to_queue(
            list(html_dom.xpath('//a[@data-automation="job-title"]/@href').getall()))
        await self.close()
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        # Ultipro doesn't have the ld+json standard
        description = html.xpath('//*[@data-automation="job-description"]/parent::div').get()
        description_compensation_data = parse_compensation_text(description)
        posted_date = html.xpath('//*[@data-automation="job-posted-date"]/text()').get()
        if posted_date:
            posted_date = get_datetime_format_or_none(get_datetime_or_none(posted_date, as_date=True))
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=html.xpath('//*[@data-automation="opportunity-title"]/text()').get(),
            locations=[html.xpath('//*[@data-automation="city-state-zip-country-label"]/text()').get()],
            job_department=html.xpath('//*[@data-automation="job-category"]/text()').get(),
            job_description=description,
            employment_type=html.xpath('//*[@data-automation="JobFullTime"]/text()').get(),
            first_posted_date=posted_date,
            **description_compensation_data
        )


class SmartRecruitersScraper(Scraper):
    ATS_NAME = 'SmartRecruiters'
    
    async def scrape_jobs(self):
        page_idx = 0
        while True:
            jobs_html = self.get_page_data(page_idx)
            if not jobs_html:
                break
            await self.add_job_links_to_queue(jobs_html.xpath('//a/@href').getall())
            page_idx += 1
        
        await self.close()
    
    def get_start_url(self):
        return f'https://careers.smartrecruiters.com/{self.EMPLOYER_KEY}/'
    
    def get_page_data(self, page_idx):
        request_url = f'https://careers.smartrecruiters.com/{self.EMPLOYER_KEY}/api/more?page={page_idx}'
        resp = requests.get(request_url)
        html_text = resp.content
        if not html_text:
            return None
        return Selector(text=html_text.decode('latin-1'))
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        job_data_html = html.xpath('//main[contains(@class, "jobad-main")]')
        job_title = job_data_html.xpath('.//h1[@class="job-title"]/text()').get()
        job_description = job_data_html.xpath('.//div[@itemprop="description"]').get()
        if not job_description:
            logger.info(f'No description found for {job_title} at {job_url}')
            return None
        description_compensation_data = parse_compensation_text(job_description)
        location_html = job_data_html.xpath('.//spl-job-location')
        location_text = location_html.xpath('./@formattedaddress').get()
        remote_type = location_html.xpath('./@workplacetype').get()
        if remote_type == 'remote' and ('remote' not in location_text.lower()):
            location_text = f'Remote: {location_text}'
        
        posted_date = html.xpath('//meta[@itemprop="datePosted"]/@content').get()
        if posted_date:
            posted_date = get_datetime_format_or_none(get_datetime_or_none(posted_date, as_date=True))
        
        job_details = job_data_html.xpath('.//li[@class="job-detail"]/text()').getall()
        job_department = None
        for job_detail in job_details:
            if 'department' in job_detail.lower():
                job_department = job_detail.replace('Department:', '').strip()
                break
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_title,
            locations=[location_text],
            job_department=job_department,
            job_description=job_description,
            employment_type=job_data_html.xpath('.//li[@itemprop="employmentType"]/text()').get(),
            first_posted_date=posted_date,
            **description_compensation_data
        )


class SmartRecruitersApiScraper(Scraper):
    ATS_NAME = 'SmartRecruiters'
    IS_API = True
    JOBS_PER_PAGE = 100  # This is the max
    
    async def scrape_jobs(self):
        has_started = False
        total_jobs = None
        start_job_idx = 0
        jobs = []
        while (not has_started) or (start_job_idx < total_jobs):
            jobs_list, total_jobs = self.get_jobs(start_job_idx)
            jobs += jobs_list
            start_job_idx += self.JOBS_PER_PAGE
            has_started = True
        
        for job in jobs:
            await self.add_job_links_to_queue(self.get_job_link(job['id']), meta_data={'job_id': job['id']})
        
        await self.close()
    
    def get_job_link(self, job_id):
        return f'https://jobs.smartrecruiters.com/{self.EMPLOYER_KEY}/{job_id}'
    
    def get_jobs(self, job_idx):
        request_data = {
            'limit': self.JOBS_PER_PAGE,
            'offset': job_idx
        }
        jobs_resp = requests.get(
            f'https://api.smartrecruiters.com/v1/companies/{self.EMPLOYER_KEY}/postings',
            params=request_data
        )
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['content'], jobs_data['totalFound']
    
    def get_raw_job_data(self, job_id):
        job_resp = requests.get(f'https://api.smartrecruiters.com/v1/companies/{self.EMPLOYER_KEY}/postings/{job_id}')
        return json.loads(job_resp.content)
    
    def get_job_description_section(self, jd_section):
        return f'<h6>{jd_section["title"]}</h6>{jd_section["text"]}'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None):
        job_data = self.get_raw_job_data(job_id)
        job_description_data = job_data['jobAd']['sections']
        job_description = ''.join([
            self.get_job_description_section(s) for s in [
                job_description_data['companyDescription'],
                job_description_data['jobDescription'],
                job_description_data['qualifications'],
                job_description_data['additionalInformation'],
            ]
        ])
        description_compensation_data = parse_compensation_text(job_description)
        location_parts = ['address', 'city', 'region', 'country', 'postalCode']
        location_data = job_data['location']
        location_text = ', '.join([location_data.get(p) for p in location_parts if location_data.get(p)])
        if location_data['remote']:
            location_text = f'Remote: {location_text}'
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['name'],
            locations=[location_text],
            job_department=job_data['function']['label'] or self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=job_data['typeOfEmployment']['label'] or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_or_none(job_data['releasedDate'], as_date=True)),
            **description_compensation_data
        )


class PaylocityScraper(Scraper):
    ATS_NAME = 'Paylocity'
    IS_JS_REQUIRED = True
    job_item_page_wait_sel = '.job-preview-header'
    
    async def scrape_jobs(self):
        await self.update_browser_context()
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, '.jobs-list')
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, '.jobs-list')
        
        html_dom = await self.get_page_html(page)
        
        await self.add_job_links_to_queue(
            list(html_dom.xpath('//div[contains(@class, "job-listing-job-item")]//a/@href').getall()))
        await self.close()
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        location_text = html.xpath('//div["job-preview-header"]//div[@class="preview-location"]/text()').get()
        is_remote = 'remote' in location_text.lower()
        standard_job_item = self.get_google_standard_job_item(html)
        if not standard_job_item:
            logger.info(f'Skipped url because there is no standard job item {job_url}')
            return None
        job_description = standard_job_item.job_description
        description_compensation_data = parse_compensation_text(job_description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        locations = [f'{"Remote " if is_remote else ""}{l}' for l in standard_job_item.locations]
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=standard_job_item.job_title,
            locations=locations,
            job_department=standard_job_item.job_department or self.DEFAULT_JOB_DEPARTMENT,
            job_description=standard_job_item.job_description,
            employment_type=standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class ApplicantProScraper(Scraper):
    ATS_NAME = 'ApplicantPro'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        await self.add_job_links_to_queue(
            list(html_dom.xpath('//div[@id="job_listings"]//a/@href').getall()))
        await self.close()
    
    def get_start_url(self):
        return f'https://{self.EMPLOYER_KEY}.applicantpro.com/jobs/'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        standard_job_item = self.get_google_standard_job_item(html)
        if not standard_job_item:
            return None
        job_description = standard_job_item.job_description
        description_compensation_data = parse_compensation_text(job_description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=standard_job_item.job_title,
            locations=standard_job_item.locations,
            job_department=standard_job_item.job_department or self.DEFAULT_JOB_DEPARTMENT,
            job_description=standard_job_item.job_description,
            employment_type=standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class EightfoldScraper(Scraper):
    ATS_NAME = 'Eightfold'
    IS_API = True
    JOBS_PER_PAGE = 10  # This looks like the max that's supported
    
    async def scrape_jobs(self):
        total_jobs = None
        start_job_idx = 0
        jobs = []
        while (not total_jobs) or (start_job_idx < total_jobs):
            jobs_list, total_jobs = self.get_jobs(start_job_idx)
            jobs += jobs_list
            start_job_idx += self.JOBS_PER_PAGE
        
        for job in jobs:
            await self.add_job_links_to_queue(self.get_job_link(job), meta_data={'job_id': job['id']})
        
        await self.close()
    
    def get_job_link(self, job_data):
        return f'https://careers.{self.EMPLOYER_KEY}.com/careers?pid={job_data["id"]}'
    
    def get_jobs(self, next_page_start):
        request_data = {
            'sort_by': 'relevance',
            'num': self.JOBS_PER_PAGE,
            'start': next_page_start
        }
        request_url = f'https://careers.{self.EMPLOYER_KEY}.com/api/apply/v2/jobs'
        jobs_resp = requests.get(request_url, params=request_data)
        jobs_data = json.loads(jobs_resp.content)
        return jobs_data['positions'], jobs_data['count']
    
    def get_raw_job_data(self, job_id):
        job_resp = requests.get(f'https://careers.{self.EMPLOYER_KEY}.com/api/apply/v2/jobs/{job_id}')
        return json.loads(job_resp.content)
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_id=None):
        job_data = self.get_raw_job_data(job_id)
        job_description = job_data['job_description']
        description_compensation_data = parse_compensation_text(job_description)
        locations = job_data['locations']
        # is_remote = job_data['location_flexibility']
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_data['name'],
            locations=locations,
            job_department=job_data['department'] or self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=get_datetime_format_or_none(get_datetime_from_unix(job_data['t_create']).date()),
            **description_compensation_data
        )


class JobviteScraper(Scraper):
    ATS_NAME = 'Jobvite'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        await self.add_job_links_to_queue(
            html_dom.xpath('//*[@class="jv-job-list"]//a/@href').getall()
        )
        await self.close()
    
    def get_start_url(self):
        return f'https://jobs.jobvite.com/careers/{self.EMPLOYER_KEY}/'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        meta_data = html.xpath('//p[@class="jv-job-detail-meta"]/text()').getall()
        
        locations = [
            l.strip() for l in meta_data[1:]
        ] if meta_data and len(meta_data) > 1 else None
        print(f'Locations: {locations}')
        
        standard_job_item = self.get_google_standard_job_item(html)
        if not standard_job_item:
            logger.info('Unable to parse JobItem from document. No standard job data (ld+json).')
            return None
        if not any((locations, standard_job_item.locations)):
            logger.info('Unable to parse JobItem from document. No location found.')
            return None
        
        job_title = (html.xpath('//h2[@class="jv-header"]//text()').get() or standard_job_item.job_title).strip()
        
        job_department = meta_data[0]
        if job_department:
            job_department = job_department.strip()
        
        job_description = html.xpath('//div[@class="jv-job-detail-description"]').get()
        description_compensation_data = parse_compensation_text(job_description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_title,
            locations=locations if locations else standard_job_item.locations,
            job_department=job_department or standard_job_item.job_department,
            job_description=job_description or standard_job_item.job_description,
            employment_type=standard_job_item.employment_type,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class RipplingScraper(Scraper):
    ATS_NAME = 'Rippling'
    
    async def scrape_jobs(self):
        jobs = self.get_jobs()
        for job in jobs:
            await self.add_job_links_to_queue(job['url'], meta_data={
                'job_department': job['department']['label'],
                'job_title': job['name'],
                'location': job['workLocation']['label']
            })
        
        await self.close()
    
    def get_jobs(self):
        jobs_resp = requests.get(
            f'https://app.rippling.com/api/ats2_provisioning/api/v1/board/{self.EMPLOYER_KEY}/jobs',
            headers={'User-Agent': get_random_user_agent()},
        )
        return json.loads(jobs_resp.content.decode('utf-8'))
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, job_title=None, location=None):
        description = html.xpath('//div[@class="ATS_htmlPreview"]').get()
        description_compensation_data = parse_compensation_text(description)
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_title,
            locations=[location],
            job_department=job_department,
            job_description=description,
            employment_type=self.DEFAULT_EMPLOYMENT_TYPE,
            **description_compensation_data
        )


# NOTE: This is different from RipplingScraper!
class RipplingAtsScraper(Scraper):
    ATS_NAME = 'Rippling'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        await self.add_job_links_to_queue(
            html_dom.xpath('//div[@class="jobs-list-container"]//a[@class="mobile-apply-link"]/@href').getall(),
        )
        await self.close()
    
    def get_start_url(self):
        return f'https://{self.EMPLOYER_KEY}.rippling-ats.com/'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        locations = [
            l.strip() for l in
            html.xpath('//span[@class="job-content-location"]/text()').getall()
        ]
        print(f'Locations: {locations}')
        standard_job_item = self.get_google_standard_job_item(html)
        locations = locations or standard_job_item.locations
        if not locations:
            logger.info('Unable to parse JobItem from document. No location found.')
            return None
        
        job_description = html.xpath('//div[contains(@class, "job-content-body")]').get()
        compensation_text = html.xpath('//div[contains(@class, "job-content-salary")]//text()').get()
        description_compensation_data = parse_compensation_text(compensation_text or job_description)
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=html.xpath('//div[@class="job-title-container"]//h2/text()').get() or standard_job_item.job_title,
            locations=locations,
            job_department=standard_job_item.job_department or self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description or standard_job_item.job_description,
            employment_type=standard_job_item.employment_type,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class RecruiteeScraper(Scraper):
    ATS_NAME = 'Recruitee'
    TEST_REDIRECT = False
    IS_REMOVE_QUERY_PARAMS = False
    job_item_page_wait_sel = '#header'
    
    async def scrape_jobs(self):
        html_dom = await self.get_html_from_url(self.get_start_url())
        job_links = list(set(html_dom.xpath('//a/@href').getall()))
        await self.add_job_links_to_queue([l for l in job_links if re.match('^.*?/o/.+?$', l)])
        await self.close()
    
    def get_start_url(self):
        return f'https://{self.EMPLOYER_KEY}.recruitee.com/'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, api_data=None):
        standard_job_item = self.get_google_standard_job_item(html)
        if not standard_job_item:
            logger.info('Unable to parse JobItem from document. No standard job data (ld+json).')
            return None
        description_compensation_data = parse_compensation_text(standard_job_item.job_description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=standard_job_item.job_title,
            locations=standard_job_item.locations,
            job_department=standard_job_item.job_department or self.DEFAULT_JOB_DEPARTMENT,
            job_description=standard_job_item.job_description,
            employment_type=standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )
    
    
class PhenomPeopleScraper(Scraper):
    ATS_NAME = 'Phenom'
    IS_JS_REQUIRED = True
    JOBS_PER_PAGE = 10
    job_item_page_wait_sel = '.job-info'
    
    async def scrape_jobs(self):
        await self.update_browser_context()
        page = await self.get_starting_page()
        await self.wait_for_el(page, '[data-ph-at-id="jobs-list"]')
        html_dom = await self.get_page_html(page)
        jobs_count = int(html_dom.xpath('//div[contains(@class, "phs-jobs-list-count")]/@data-ph-at-count').get())
        total_page_count = ceil(jobs_count / self.JOBS_PER_PAGE)
        page_count = 0
        while page_count < total_page_count:
            next_button_sel = 'a[data-ph-at-id="pagination-next-link"]'
            has_next_page = await page.locator(f'css={next_button_sel}').is_visible()
            if page_count != 0 and has_next_page:
                await page.locator(f'css={next_button_sel}').click()
                # await page.goto(self.get_next_page_url(page_count))
                await self.wait_for_el(page, '[data-ph-at-id="jobs-list"]')
                html_dom = await self.get_page_html(page)
            job_links = html_dom.xpath('//ul[@data-ph-at-id="jobs-list"]//span[@role="heading"]//a/@href').getall()
            await self.add_job_links_to_queue(job_links)
            page_count += 1
        await self.close()
        
    def get_next_page_url(self, page_idx):
        start_url = self.get_start_url()
        if page_idx == 0:
            return start_url
        return f'{start_url}?s=1&from={page_idx * self.JOBS_PER_PAGE}'
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None, api_data=None):
        standard_job_item = self.get_google_standard_job_item(html)
        if not standard_job_item:
            logger.info('Unable to parse JobItem from document. No standard job data (ld+json).')
            return None
        
        job_details = html.xpath('//div[@class="job-header-block"]')
        job_description = html.xpath('//section[@class="job-description"]').get()
        description_compensation_data = parse_compensation_text(job_description)
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        locations = [l.strip() for l in job_details.xpath('.//span[contains(@class, "job-location")]/text()').getall() if l and l.strip()]
        department = [d.strip() for d in job_details.xpath('.//span[contains(@class, "job-category")]/text()').getall() if d and d.strip()]
        if department:
            department = department[0]
        
        employment_type = [t.strip() for t in job_details.xpath('.//span[contains(@class, "type")]/text()').getall() if t and t.strip()]
        if employment_type:
            employment_type = employment_type[0]
            
        job_title = job_details.xpath('.//h1[@class="job-title"]/text()').get()
        if job_title:
            job_title = job_title.strip()
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=job_title or standard_job_item.job_title,
            locations=locations or standard_job_item.locations,
            job_department=department or standard_job_item.job_department or self.DEFAULT_JOB_DEPARTMENT,
            job_description=job_description,
            employment_type=employment_type or standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )
    

class StandardScraper(Scraper):
    jobs_xpath_sel = None
    
    async def scrape_jobs(self):
        html_dom = await self.get_html()
        await self.add_job_links_to_queue(
            list(html_dom.xpath(self.jobs_xpath_sel).getall()))
        await self.close()
    
    async def get_html(self):
        return await self.get_html_from_url(self.get_start_url())
    
    def get_job_data_from_html(self, html, job_url=None, job_department=None):
        standard_job_item = self.get_google_standard_job_item(html)
        if not standard_job_item:
            return None
        job_description = standard_job_item.job_description
        description_compensation_data = parse_compensation_text(job_description)
        
        compensation_data = merge_compensation_data(
            [description_compensation_data, standard_job_item.get_compensation_dict()]
        )
        
        return JobItem(
            employer_name=self.employer_name,
            application_url=job_url,
            job_title=standard_job_item.job_title,
            locations=standard_job_item.locations,
            job_department=standard_job_item.job_department or self.DEFAULT_JOB_DEPARTMENT,
            job_description=standard_job_item.job_description,
            employment_type=standard_job_item.employment_type or self.DEFAULT_EMPLOYMENT_TYPE,
            first_posted_date=standard_job_item.first_posted_date,
            logo_url=standard_job_item.logo_url,
            website_domain=standard_job_item.website_domain,
            **compensation_data
        )


class StandardJsScraper(StandardScraper):
    IS_JS_REQUIRED = True
    main_page_wait_sel = None  # Per employer scraper
    job_item_page_wait_sel = None  # Per employer scraper
    
    async def get_html(self):
        await self.update_browser_context()
        page = await self.get_starting_page()
        
        # Make sure page data has loaded
        try:
            await self.wait_for_el(page, self.main_page_wait_sel)
        except PlaywrightTimeoutError:
            page = await self.get_starting_page()
            await self.wait_for_el(page, self.main_page_wait_sel)
        
        return await self.get_page_html(page)

# TODO: JazzHR Scraper
# https://blavity.applytojob.com/
