import re

import scrapy
from django.utils import timezone
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from jvapp.utils.sanitize import sanitize_html
from scraper.scraper.items import JobItem
from scraper.scraper.utils.seleniumSetup import get_dom_el_or_none, get_selenium, get_web_element_html, get_web_element_wait,\
    retry_click, WEBDRIVER_WAIT_SECONDS


__all__ = [
    'BreezySpider', 'GreenhouseSpider', 'JazzHRSpider', 'LeverSpider', 'WorkdaySpider', 'WorkdaySpider2'
]


class BreezySpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None
    
    def parse(self, response):
        yield from response.follow_all(css='.positions-container li a', callback=self.parse_job)
    
    def parse_job(self, response):
        summaryHtml = response.xpath('//div[@class="banner"]')
        
        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=summaryHtml.xpath('.//h1/text()').get(),
            location=summaryHtml.xpath('.//li[@class="location"]/span/text()').get(),
            job_department=summaryHtml.xpath('.//li[@class="department"]/span/text()').get(),
            job_description=sanitize_html(response.xpath('//div[@class="description"]').get()),
            employment_type=summaryHtml.xpath('.//li[@class="type"]/span/text()').get(),
        )


class GreenhouseSpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None
    
    def parse(self, response):
        for departmentSection in response.xpath('//section[@class="level-0"]'):
            department = departmentSection.xpath('.//h3/text()').get() or departmentSection.xpath('.//h2/text()').get()
            jobLinks = departmentSection.xpath('./div[@class="opening"]//a')
            yield from response.follow_all(jobLinks, callback=self.parse_job, meta={'job_department': department})
            
            for subDepartmentSection in departmentSection.xpath('.//section[@class="child level-1"]'):
                department = subDepartmentSection.xpath('.//h4/text()').get()
                jobLinks = subDepartmentSection.xpath('.//div[@class="opening"]//a')
                yield from response.follow_all(jobLinks, callback=self.parse_job, meta={'job_department': department})
    
    def parse_job(self, response):
        job_department = response.request.meta['job_department']
        location = response.xpath('//div[@id="header"]//div[@class="location"]/text()').get().strip()
        
        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=response.xpath('//div[@id="header"]//h1/text()').get(),
            location=location,
            job_department=job_department,
            job_description=sanitize_html(response.xpath('//div[@id="content"]').get()),
            employment_type=None,
        )


class JazzHRSpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None
    
    def parse(self, response):
        jobs = response.css('.jobs-list a')
        yield from response.follow_all(jobs, callback=self.parse_job)
    
    def parse_job(self, response):
        jobSummary = response.xpath('//div[@class="job-header"]')
        
        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=jobSummary.xpath('.//h1/text()').get().strip(),
            location=jobSummary.xpath('(.//li[@title="Location"]//text())[2]').get().strip(),
            job_department=jobSummary.xpath('(.//li[@title="Department"]//text())[2]').get().strip(),
            job_description=sanitize_html(
                response.xpath('//div[@id="job-description"]//div[@class="description"]').get()
            ),
            employment_type=jobSummary.xpath('(.//li[@title="Type"]//text())[2]').get().strip(),
        )


class LeverSpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None
    
    def parse(self, response):
        yield from response.follow_all(response.xpath('//div[@class="posting"]//a'), callback=self.parse_job)
    
    def parse_job(self, response):
        jobSummary = response.xpath('//div[@class="posting-headline"]')
        location, job_department, positionType = jobSummary.xpath('.//div[@class="posting-categories"]/div/text()')
        
        parseItemFn = lambda item: item.get().replace('/', '').strip()
        location = parseItemFn(location)
        job_department = parseItemFn(job_department)
        positionType = parseItemFn(positionType).lower()
        
        job_description = ''
        for content in response.xpath('//div[@class="section page-centered"]//div'):
            if not content.xpath('.//text()').get():
                continue
            job_description += content.get()
        
        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=jobSummary.xpath('.//h2/text()').get().strip(),
            location=location,
            job_department=job_department,
            job_description=sanitize_html(job_description),
            employment_type=positionType,
        )


class WorkdaySpider2(scrapy.Spider):
    name = None
    employer_name = None
    start_url = None
    
    def start_requests(self):
        yield scrapy.Request(self.start_url, meta={
            'playwright': True,
            'playwright_include_page': True,
            'playwright_page_methods': [PageMethod('wait_for_selector', 'section[data-automation-id="jobResults"]')],
            'errback': self.errback
        })
    
    def get_html_dom(self, page):
        html = page.locate('section[data-automation-id="jobResults"]').inner_html()
        return Selector(text=html)
    
    async def parse(self, response):
        page = response.meta["playwright_page"]
        html_dom = self.get_html_dom(page)
        
        # Iterate through each job department
        await page.locate('css=button[data-automation-id="jobFamilyGroup"]').click()
        job_departments = html_dom.xpath('//div[@data-automation-id="jobFamilyGroupCheckboxGroup"]')
        job_department_names = [
            re.sub('\([0-9]+\)', '', jd).strip()
            for jd in job_departments.xpath('.//label/text()').get()
        ]
        for selector_idx, job_department_name in enumerate(job_department_names):
            # Note: Setting page filters does not result in a new page redirect
            await page.locate('css=button[data-automation-id="jobFamilyGroup"]').click()  # Open department menu
            await page.locate('css=button[data-automation-id="clearButton"]').click()  # Clear selected
            await page.locate \
                (f'css=div[data-automation-id="jobFamilyGroupCheckboxGroup"] [role="cell"]:nth-of-type({selector_idx + 1})').click()  # Select the department menu item
            await page.locate('css=button[data-automation-id="viewAllJobsButton"]').click()  # Apply selection
            
            # Parse jobs for each page
            is_started = False
            next_page = None
            while (not is_started) or next_page:
                if next_page:
                    retry_click('nav[aria-label="pagination"]', 'button[aria-label="next"]')
                    html_dom = self.get_html_dom(page)
                for job_link in html_dom.css('section[data-automation-id="jobResults"] a'):
                    yield response.follow(job_link, callback=self.parse_job, meta={'job_department': job_department_name})
                
                is_started = True
                next_page = html_dom.css('nav[aria-label="pagination"] button[aria-label="next"]').get()
        
        await page.close()
    
    def parse_job(self, response):
        job_department = response.request.meta['job_department']
        job_data = response.xpath('//div[@data-automation-id="jobPostingPage"]')
        # Note workday only shows the first 5 locations. JS automation would be necessary
        # to click the button to show additional locations
        locations = [l.get().strip() for l in job_data.xpath('.//div[@data-automation-id="locations"]/dl/dd/text()')]
        
        job_description = ''
        for content in response.xpath('//div[@class="section page-centered"]//div'):
            if not content.xpath('.//text()').get():
                continue
            job_description += content.get()
        
        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=job_data.xpath('.//[@data-automation-id="jobPostingHeader"]/text()').get().strip(),
            location=locations[0],
            job_department=job_department,
            job_description=sanitize_html(job_description),
            employment_type=job_data.xpath('.//[@data-automation-id="time"]/dl/dd/text()').get().strip(),
        )
    
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()


class WorkdaySpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None
    driver = None
    
    def __init__(self):
        print(f'Starting {self.name} spider')
        self.driver = get_selenium(is_debug=True)
        self.driver.get(self.start_urls[0])
        super().__init__()
    
    def get_html_dom(self):
        html = get_web_element_html(
            self.driver, get_web_element_wait(self.driver, 'section[data-automation-id="jobResults"]')
        )
        return Selector(text=html)
    
    def parse(self, response):
        print(f'Parsing for {self.name} spider')
        html_dom = self.get_html_dom()
        # Iterate through each job department
        job_page_sel = 'div[data-automation-id="jobSearchPage"]'
        retry_click(job_page_sel, 'button[data-automation-id="jobFamilyGroup"]')
        job_departments = html_dom.xpath('//div[@data-automation-id="jobFamilyGroupCheckboxGroup"]')
        job_department_names = [re.sub('\([0-9]+\)', '', jd).strip() for jd in job_departments.xpath('.//label/text()').get()]
        job_department_dom_els = job_departments.xpath('.//div[role="row"]')
        for job_department_name, job_department_el in zip(job_department_names, job_department_dom_els):
            retry_click('div[data-automation-id="jobSearch"]', 'button[data-automation-id="jobFamilyGroup"]')  # Open department menu
            retry_click('div[data-automation-id="toolbar"]', 'button[data-automation-id="clearButton"]')  # Clear selected
            retry_click(job_department_el.get(), '[role="cell"]')  # Select the department menu item
            retry_click('div[data-automation-id="toolbar"]', 'button[data-automation-id="viewAllJobsButton"]')  # Apply selection
            
            # Parse jobs for each page
            is_started = False
            next_page = None
            while (not is_started) or next_page:
                if next_page:
                    retry_click('nav[aria-label="pagination"]', 'button[aria-label="next"]')
                    html_dom = self.get_html_dom()
                yield from response.follow_all(
                    html_dom.xpath('//section[@data-automation-id="jobResults"]//a'),
                    callback=self.parse_job,
                    meta={'job_department': job_department_name}
                )
                is_started = True
                next_page = response.css('nav[aria-label="pagination"] button[aria-label="next"]').get()
    
    def parse_job(self, response):
        job_department = response.request.meta['job_department']
        job_data = response.xpath('//div[@data-automation-id="jobPostingPage"]')
        # Note workday only shows the first 5 locations. JS automation would be necessary
        # to click the button to show additional locations
        locations = [l.get().strip() for l in job_data.xpath('.//div[@data-automation-id="locations"]/dl/dd/text()')]
        
        job_description = ''
        for content in response.xpath('//div[@class="section page-centered"]//div'):
            if not content.xpath('.//text()').get():
                continue
            job_description += content.get()
        
        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=job_data.xpath('.//[@data-automation-id="jobPostingHeader"]/text()').get().strip(),
            location=locations[0],
            job_department=job_department,
            job_description=sanitize_html(job_description),
            employment_type=job_data.xpath('.//[@data-automation-id="time"]/dl/dd/text()').get().strip(),
        )
