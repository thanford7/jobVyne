import asyncio
import logging

from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localtime
from playwright.async_api import async_playwright

from jvapp.models.employer import Employer, EmployerJob
from scrape.base_scrapers import get_random_user_agent, get_recent_scraped_job_urls
from scrape.custom_scraper.workableAts import workable_scrapers
from scrape.employer_scrapers import all_scrapers, test_scrapers
from scrape.job_processor import ScrapedJobProcessor

logger = logging.getLogger(__name__)
JS_LOAD_WAIT_MS = 30000 if settings.DEBUG else 60000


async def get_browser(playwright):
    browser = await playwright.chromium.launch(headless=True)
    browser_context = await browser.new_context()
    browser_context.set_default_timeout(JS_LOAD_WAIT_MS)
    await browser_context.set_geolocation({'latitude': 34.02016, 'longitude': -118.44472})
    await browser_context.set_extra_http_headers({
        'User-Agent': get_random_user_agent(),
        'Referer': 'https://www.google.com',
        'Origin': 'https://www.google.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*'
    })
    return browser, browser_context

        
async def launch_scraper(scraper_class, skip_urls):
    # Scrape jobs from web pages
    async with async_playwright() as p:
        browser, browser_context = await get_browser(p)
        scraper = scraper_class(p, browser_context, skip_urls)
        try:
            async_scrapers = [scraper.scrape_jobs()]
            await asyncio.gather(*async_scrapers)
        except Exception:
            await scraper.close_connections()
            raise
        await browser_context.close()
        await browser.close()
    return scraper
    
    
def run_job_scrapers(employer_names=None):
    if not employer_names:
        if settings.IS_LOCAL and test_scrapers:
            scraper_classes = list(test_scrapers.values())
        else:
            scraper_classes = list(all_scrapers.values())
    else:
        scraper_classes = (
            [all_scrapers.get(employer_name) for employer_name in employer_names] +
            [workable_scrapers.get(employer_name) for employer_name in employer_names]
        )
        scraper_classes = [s for s in scraper_classes if s]
    
    # Sort scrapers by the oldest successful scrape date
    employer_last_scrape_date = {e['employer_name']: e['last_job_scrape_success_dt'] for e in (
        Employer.objects.filter(is_use_job_url=True, organization_type=Employer.ORG_TYPE_EMPLOYER)
        .values('employer_name', 'last_job_scrape_success_dt')
    )}
    old_date = timezone.datetime(1900, 1, 1, tzinfo=timezone.get_default_timezone())
    scraper_classes.sort(key=lambda s: employer_last_scrape_date.get(s.employer_name) or old_date)
    
    for scraper_class in scraper_classes:
        # Allow scrapers to fail so it doesn't impact other scrapers
        employer = None
        scraper = None
        try:
            logger.info(f'Starting scraper for {scraper_class.employer_name}')
            try:
                employer = Employer.objects.get(employer_name=scraper_class.employer_name)
            except Employer.DoesNotExist:
                employer = Employer(
                    employer_name=scraper_class.employer_name,
                    is_use_job_url=True
                )
                employer.save()
            
            if employer and employer.last_job_scrape_success_dt:
                last_run_diff_minutes = (timezone.now() - employer.last_job_scrape_success_dt).total_seconds() / 60
                if (not settings.DEBUG) and last_run_diff_minutes < 180:
                    logger.info(f'Scraper successfully run in last 3 hours for {scraper_class.employer_name}. Skipping')
                    continue
            
            skip_urls = []
            if not employer_names:
                skip_urls = get_recent_scraped_job_urls(employer.employer_name)
            scraper = asyncio.run(launch_scraper(scraper_class, skip_urls))
        
            # Process raw job data
            job_processor = ScrapedJobProcessor(employer)
            logger.info(f'Processing jobs for {scraper_class.employer_name}')
            job_processor.process_jobs(scraper.job_items)
            logger.info(f'Finalizing all data for {scraper_class.employer_name}')
            job_processor.finalize_data(scraper.skipped_urls)
            logger.info(f'Scraping complete for {scraper_class.employer_name}')
        except Exception as e:
            logger.exception(f'Error occurred while scraping jobs for {scraper_class.employer_name}', exc_info=e)
            if employer:
                employer.has_job_scrape_failure = True
                employer.save()
        finally:
            logger.info(f'Running `finally` block for {scraper_class.employer_name}')
            if scraper:
                asyncio.run(scraper.close_connections())
