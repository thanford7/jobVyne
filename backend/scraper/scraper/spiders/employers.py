import scrapy
from django.utils import timezone
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from jvapp.utils.sanitize import REDUCE_H_TAG_MAP, sanitize_html
from scraper.items import JobItem
from scraper.utils.seleniumSetup import getDomElOrNone, getSelenium, getWebElementHtml, getWebElementWait,\
    retryClick, WEBDRIVER_WAIT_SECONDS


def scraper_sanitize_html(html):
    return sanitize_html(html, replace_tag_map={
        'div': 'p', 'span': 'p', 'form': 'p', 'i': 'em', 'b': 'strong', **REDUCE_H_TAG_MAP
    })


# def fontSizeToHeaderSanitizer(element):
#     style = element.get('style')
#     if not style or ('font-size' not in style):
#         return element
#
#     fontSizeStyle = next((s for s in style.split(';') if 'font-size' in s), None)
#     fontSizePx = fontSizeStyle.split(':')[1].strip()
#     if 'px' not in fontSizePx:
#         return element
#
#     fontSize = float(fontSizePx.replace('px', '').strip())
#     if fontSize >= 16:
#         element.tag = 'h5'
#     else:
#         element.tag = 'h6'
#
#     element.style = None
#
#     return element


class BreezySpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None

    def parse(self, response):
        yield from response.follow_all(css='.positions-container li a', callback=self.parseJob)

    def parseJob(self, response):
        summaryHtml = response.xpath('//div[@class="banner"]')

        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=summaryHtml.xpath('.//h1/text()').get(),
            location=summaryHtml.xpath('.//li[@class="location"]/span/text()').get(),
            job_department=summaryHtml.xpath('.//li[@class="department"]/span/text()').get(),
            job_description=scraper_sanitize_html(response.xpath('//div[@class="description"]').get()),
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
            yield from response.follow_all(jobLinks, callback=self.parseJob, meta={'job_department': department})

            for subDepartmentSection in departmentSection.xpath('.//section[@class="child level-1"]'):
                department = subDepartmentSection.xpath('.//h4/text()').get()
                jobLinks = subDepartmentSection.xpath('.//div[@class="opening"]//a')
                yield from response.follow_all(jobLinks, callback=self.parseJob, meta={'job_department': department})

    def parseJob(self, response):
        job_department = response.request.meta['job_department']
        location = response.xpath('//div[@id="header"]//div[@class="location"]/text()').get().strip()

        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=response.xpath('//div[@id="header"]//h1/text()').get(),
            location=location,
            job_department=job_department,
            job_description=scraper_sanitize_html(response.xpath('//div[@id="content"]').get()),
            employment_type=None,
        )


class JazzHRSpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None

    def parse(self, response):
        jobs = response.css('.jobs-list a')
        yield from response.follow_all(jobs, callback=self.parseJob)

    def parseJob(self, response):
        jobSummary = response.xpath('//div[@class="job-header"]')

        yield JobItem(
            employer_name=self.employer_name,
            application_url=response.url,
            job_title=jobSummary.xpath('.//h1/text()').get().strip(),
            location=jobSummary.xpath('(.//li[@title="Location"]//text())[2]').get().strip(),
            job_department=jobSummary.xpath('(.//li[@title="Department"]//text())[2]').get().strip(),
            job_description=scraper_sanitize_html(
                response.xpath('//div[@id="job-description"]//div[@class="description"]').get()
            ),
            employment_type=jobSummary.xpath('(.//li[@title="Type"]//text())[2]').get().strip(),
        )


class LeverSpider(scrapy.Spider):
    name = None
    employer_name = None
    start_urls = None

    def parse(self, response):
        yield from response.follow_all(response.xpath('//div[@class="posting"]//a'), callback=self.parseJob)

    def parseJob(self, response):
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
            job_description=scraper_sanitize_html(job_description),
            employment_type=positionType,
        )


class Barn2DoorSpider(BreezySpider):
    employer_name = 'Barn2Door'
    name = "barn2Door"
    start_urls = [
        'https://barn2door-inc.breezy.hr/?',
    ]


class ZoomoSpider(scrapy.Spider):
    name = "zoomo"
    start_urls = [
        'https://apply.workable.com/zoomo/',
    ]
    html = None
    driver = None

    def __init__(self):
        self.driver = getSelenium()
        self.driver.get('https://apply.workable.com/zoomo/')
        jobsEl = getWebElementWait(self.driver, '#jobs')

        # # Filter for full time positions only
        retryClick(jobsEl, '#worktypes-filter_input')  # Open the filter
        retryClick(jobsEl, '#worktypes-filter_listbox li[value="full"]')  # Select full time option

        # Load all jobs
        def getRunSeconds(start):
            return (timezone.now() - start).seconds

        loadBtnSelector = 'button[data-ui="load-more-button"]'
        loadJobsBtn = getDomElOrNone(self.driver, jobsEl, loadBtnSelector)
        start = timezone.now()
        while loadJobsBtn and getRunSeconds(start) < 20:
            retryClick(jobsEl, loadBtnSelector, isAllowNotFound=True)
            loadJobsBtn = getDomElOrNone(self.driver, jobsEl, loadBtnSelector)

        # Refetch the job HTML data
        self.html = getWebElementHtml(self.driver, getWebElementWait(self.driver, '#jobs'))
        super().__init__()

    def parse(self, response):
        resp = Selector(text=self.html)
        jobs = resp.xpath('//ul/li[@data-ui="job"]')
        for job in jobs:
            application_url = response.urljoin(job.xpath('.//a/@href').get())
            self.driver.get(application_url)
            def getJobDetail():
                body = WebDriverWait(self.driver, WEBDRIVER_WAIT_SECONDS).until(lambda d: d.find_element(By.TAG_NAME, 'main'))
                jobDetail = Selector(text=getWebElementHtml(self.driver, body))
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
                job_description=scraper_sanitize_html(
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
            yield from response.follow_all(jobTable.xpath('.//a'), callback=self.parseJob, meta={'job_department': department.get().strip()})

    def parseJob(self, response):
        job_department = response.request.meta['job_department']
        job_title = response.xpath('//h2[@class="jv-header"]/text()').get().strip()
        locations = response.xpath('//p[@class="jv-job-detail-meta"]/text()')[1:]  # The first text item is the job department
        job_description = scraper_sanitize_html(response.xpath('//div[@class="jv-job-detail-description"]').get())
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
        self.driver = getSelenium()
        self.driver.get('https://www.attentivemobile.com/careers')
        self.html = getWebElementHtml(self.driver, getWebElementWait(self.driver, '#lever-jobs-container'))
        super().__init__()

    def parse(self, response):
        resp = Selector(text=self.html)
        jobs = resp.xpath('//li[@class="lever-job"]//a')
        yield from response.follow_all(jobs, callback=self.parseJob)


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
