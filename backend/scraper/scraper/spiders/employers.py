import scrapy
from django.utils import timezone
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from jvapp.utils.sanitize import sanitize_html
from scraper.scraper.items import JobItem
from scraper.scraper.spiders.base_spiders import *
from scraper.scraper.utils.seleniumSetup import WEBDRIVER_WAIT_SECONDS, get_dom_el_or_none, get_selenium, \
    get_web_element_html, \
    get_web_element_wait, retry_click


class BlueOriginSpider(WorkdaySpider2):
    employer_name = 'Blue Origin'
    name = 'blueOrigin'
    start_urls = ['https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin']


class Barn2DoorSpider(BreezySpider):
    employer_name = 'Barn2Door'
    name = "barn2Door"
    start_urls = ['https://barn2door-inc.breezy.hr/?']


class ZoomoSpider(scrapy.Spider):
    name = "zoomo"
    start_urls = ['https://apply.workable.com/zoomo/']
    html = None
    driver = None
    
    def __init__(self):
        self.driver = get_selenium()
        self.driver.get('https://apply.workable.com/zoomo/')
        jobsEl = get_web_element_wait(self.driver, '#jobs')
        
        # # Filter for full time positions only
        retry_click(jobsEl, '#worktypes-filter_input')  # Open the filter
        retry_click(jobsEl, '#worktypes-filter_listbox li[value="full"]')  # Select full time option
        
        # Load all jobs
        def getRunSeconds(start):
            return (timezone.now() - start).seconds
        
        loadBtnSelector = 'button[data-ui="load-more-button"]'
        loadJobsBtn = get_dom_el_or_none(self.driver, jobsEl, loadBtnSelector)
        start = timezone.now()
        while loadJobsBtn and getRunSeconds(start) < 20:
            retry_click(jobsEl, loadBtnSelector, is_allow_not_found=True)
            loadJobsBtn = get_dom_el_or_none(self.driver, jobsEl, loadBtnSelector)
        
        # Refetch the job HTML data
        self.html = get_web_element_html(self.driver, get_web_element_wait(self.driver, '#jobs'))
        super().__init__()
    
    def parse(self, response):
        resp = Selector(text=self.html)
        jobs = resp.xpath('//ul/li[@data-ui="job"]')
        for job in jobs:
            application_url = response.urljoin(job.xpath('.//a/@href').get())
            self.driver.get(application_url)
            
            def getJobDetail():
                body = WebDriverWait(self.driver, WEBDRIVER_WAIT_SECONDS).until \
                    (lambda d: d.find_element(By.TAG_NAME, 'main'))
                jobDetail = Selector(text=get_web_element_html(self.driver, body))
                job_description = jobDetail.xpath('//div[@data-ui="job-description"]').get()
                jobRequirements = jobDetail.xpath('//div[@data-ui="job-requirements"]').get()
                jobBenefits = jobDetail.xpath('//div[@data-ui="job-benefits"]').get()
                return (job_description, jobRequirements, jobBenefits)
            
            (job_description, jobRequirements, jobBenefits) = getJobDetail()
            # Retry if failure
            if not all([job_description, jobRequirements, jobBenefits]):
                (job_description, jobRequirements, jobBenefits) = getJobDetail()
            
            yield JobItem(
                employer_name='Zoomo',
                application_url=application_url,
                job_title=job.xpath('.//h2[@data-ui="job-title"]/span/text()').get(),
                location=job.xpath('.//span[@data-ui="job-location"]/text()').get(),
                job_department=job.xpath('.//span[@data-ui="job-department"]/text()').get(),
                job_description=sanitize_html(
                    (job_description or '') + (jobRequirements or '') + (jobBenefits or '')
                ),
                employment_type=job.xpath('.//span[@data-ui="job-type"]/text()').get(),
            )


class QuipSpider(GreenhouseSpider):
    employer_name = 'quip'
    name = "quip"
    start_urls = [
        'https://boards.greenhouse.io/quip',
    ]


class QuartetHealthSpider(GreenhouseSpider):
    employer_name = 'Quartet Health'
    name = "quartetHealth"
    start_urls = [
        'https://boards.greenhouse.io/quartethealth',
    ]


class ProdegeSpider(scrapy.Spider):
    name = "prodege"
    start_urls = [
        'http://jobs.jobvite.com/careers/prodege/jobs',
    ]

    def parse(self, response):
        allJobs = response.xpath('//div[@class="jv-wrapper"]')
        for department, jobTable in zip(allJobs.xpath('.//h3/text()'), allJobs.xpath('.//table[@class="jv-job-list"]')):
            yield from response.follow_all(jobTable.xpath('.//a'), callback=self.parse_job, meta={'job_department': department.get().strip()})

    def parse_job(self, response):
        job_department = response.request.meta['job_department']
        job_title = response.xpath('//h2[@class="jv-header"]/text()').get().strip()
        locations = response.xpath('//p[@class="jv-job-detail-meta"]/text()')[1:]  # The first text item is the job department
        job_description = sanitize_html(response.xpath('//div[@class="jv-job-detail-description"]').get())
        for location in locations:
            location = ', '.join([l.strip() for l in location.get().strip().split(',')])
            yield JobItem(
                employer_name='Prodege',
                application_url=response.url,
                job_title=job_title,
                location=location,
                job_department=job_department,
                job_description=job_description,
                employment_type=None,
            )


class PilotSpider(GreenhouseSpider):
    employer_name = 'Pilot'
    name = 'pilot'
    start_urls = [
        'https://boards.greenhouse.io/pilothq/',
    ]


class OnnaSpider(GreenhouseSpider):
    employer_name = 'Onna'
    name = 'onna'
    start_urls = ['https://boards.greenhouse.io/onna']


class NomadHealthSpider(GreenhouseSpider):
    employer_name = 'Nomad Health'
    name = 'nomadHealth'
    start_urls = ['https://boards.greenhouse.io/nomadhealth']


class MolocoSpider(GreenhouseSpider):
    employer_name = 'Moloco'
    name = 'moloco'
    start_urls = ['https://boards.greenhouse.io/moloco']


class LiberisSpider(GreenhouseSpider):
    employer_name = 'Liberis'
    name = 'liberis'
    start_urls = ['https://boards.greenhouse.io/liberis']


class KindbodySpider(GreenhouseSpider):
    employer_name = 'Kindbody'
    name = 'kindbody'
    start_urls = ['https://boards.greenhouse.io/kindbody/']


class HavenlySpider(GreenhouseSpider):
    employer_name = 'Havenly'
    name = 'havenly'
    start_urls = ['https://boards.greenhouse.io/havenly']


class GradleSpider(GreenhouseSpider):
    employer_name = 'Gradle'
    name = 'gradle'
    start_urls = ['https://boards.greenhouse.io/gradle']


class ComplyAdvantageSpider(GreenhouseSpider):
    employer_name = 'Comply Advantage'
    name = 'complyAdvantage'
    start_urls = ['https://boards.greenhouse.io/complyadvantage']


class BlockRenovationSpider(GreenhouseSpider):
    employer_name = 'Block Renovation'
    name = 'blockRenovation'
    start_urls = ['https://boards.greenhouse.io/blockrenovation']


class LinkSquaresSpider(BreezySpider):
    employer_name = 'LinkSquares'
    name = 'linkSquares'
    start_urls = ['https://linksquares.breezy.hr/']


class OutschoolSpider(LeverSpider):
    employer_name = 'Outschool'
    name = 'outschool'
    start_urls = ['https://jobs.lever.co/outschool/']


class MediaflySpider(LeverSpider):
    employer_name = 'Mediafly'
    name = 'mediafly'
    start_urls = ['https://jobs.lever.co/Mediafly/']


class KandjiSpider(LeverSpider):
    employer_name = 'Kandji'
    name = 'kandji'
    start_urls = ['https://jobs.lever.co/kandji']


class JerrySpider(LeverSpider):
    employer_name = 'Jerry'
    name = 'jerry'
    start_urls = ['https://jobs.lever.co/getjerry/']


class IroncladSpider(LeverSpider):
    employer_name = 'Ironclad'
    name = 'ironclad'
    start_urls = ['https://jobs.lever.co/ironcladapp']


class HiveSpider(LeverSpider):
    employer_name = 'Hive'
    name = 'hive'
    start_urls = ['https://jobs.lever.co/hive/']


class FountainSpider(LeverSpider):
    employer_name = 'Fountain'
    name = 'fountain'
    start_urls = ['https://jobs.lever.co/fountain']


class FLYRLabsSpider(LeverSpider):
    employer_name = 'FLYR Labs'
    name = 'flyr'
    start_urls = ['https://jobs.lever.co/flyrlabs']


class DISQOSpider(LeverSpider):
    employer_name = 'DISQO'
    name = 'disqo'
    start_urls = ['https://jobs.lever.co/disqo']


class AttentiveSpider(LeverSpider):
    employer_name = 'Attentive'
    name = 'attentive'
    start_urls = ['https://www.attentivemobile.com/careers']

    html = None
    driver = None

    def __init__(self):
        self.driver = get_selenium()
        self.driver.get('https://www.attentivemobile.com/careers')
        self.html = get_web_element_html(self.driver, get_web_element_wait(self.driver, '#lever-jobs-container'))
        super().__init__()

    def parse(self, response):
        resp = Selector(text=self.html)
        jobs = resp.xpath('//li[@class="lever-job"]//a')
        yield from response.follow_all(jobs, callback=self.parse_job)


class CurologySpider(LeverSpider):
    employer_name = 'Curology'
    name = 'curology'
    start_urls = ['https://jobs.lever.co/curology']


class CoverGeniusSpider(LeverSpider):
    employer_name = 'Cover Genius'
    name = 'covergenius'
    start_urls = ['https://jobs.lever.co/covergenius']


class BounteousSpider(LeverSpider):
    employer_name = 'Bounteous'
    name = 'bounteous'
    start_urls = ['https://jobs.lever.co/bounteous']


class LeapSpider(JazzHRSpider):
    employer_name = 'Leap'
    name = 'leap'
    start_urls = ['https://leap.applytojob.com/apply']


class FlorenceHealthcareSpider(JazzHRSpider):
    employer_name = 'Florence Healthcare'
    name = 'florence'
    start_urls = ['https://florencehealthcare.applytojob.com/apply']


class AzaleaHealthSpider(JazzHRSpider):
    employer_name = 'Azalea Health'
    name = 'azaleaHeath'
    start_urls = ['https://azaleahealth.theresumator.com/apply']


class ExabeamSpider(LeverSpider):
    employer_name = 'Exabeam'
    name = 'exabeam'
    start_urls = ['https://jobs.lever.co/exabeam']
    
    
class HospitalIQSpider(scrapy.Spider):
    name = 'hospiq'
    employer_name = 'Hospital IQ'
    start_urls = ['https://www.hospiq.com/careers/']
    
    def parse(self, response):
        yield from response.follow_all(response.xpath('//div[@id="grayback"]//a'), callback=self.parse_job)
    
    def parse_job(self, response):
        jobData = response.xpath('//div[@id="leftcol"]')
        job_description = '<p>' + jobData.xpath('./text()').get() + '</p>'
        for content in jobData.xpath('./*[not(self::p) and not(self::a) and not(self::br)]'):
            job_description += content.get()
        
        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=jobData.xpath('.//p[1]/text()').get().strip(),
            location='Remote',
            job_department='General',
            job_description=sanitize_html(job_description),
            employment_type='Full time',
        )
