import asyncio
import datetime
import logging
from itertools import groupby

from django.conf import settings
from django.utils import timezone
from playwright.async_api import async_playwright

from jvapp.models import Employer, EmployerJob
from scrape.employer_scrapers import all_scrapers
from scrape.job_processor import JobProcessor

logger = logging.getLogger(__name__)
JS_LOAD_WAIT_MS = 30000 if settings.DEBUG else 60000
SKIP_SCRAPE_CUTOFF = datetime.timedelta(days=7)


async def get_browser(playwright):
    browser = await playwright.chromium.launch(headless=True)
    browser_context = await browser.new_context()
    browser_context.set_default_timeout(JS_LOAD_WAIT_MS)
    return browser_context

        
async def launch_scrapers(scraper_classes, skip_urls):
    # Scrape jobs from web pages
    async with async_playwright() as p:
        browser = await get_browser(p)
        scrapers = [sc(p, browser, skip_urls) for sc in scraper_classes]
        try:
            async_scrapers = [s.scrape_jobs() for s in scrapers]
            await asyncio.gather(*async_scrapers)
        except Exception:
            for scraper in scrapers:
                await scraper.close_connections()
            raise

    return scrapers
    
    
def run_job_scrapers(employer_names=None):
    if not employer_names:
        scraper_classes = all_scrapers.values()
    else:
        scraper_classes = [all_scrapers[employer_name] for employer_name in employer_names]

    # Make a map of employer -> list of recently scraped urls
    recent_employer_jobs = (
        EmployerJob.objects
        .filter(modified_dt__gt=datetime.datetime.now() - SKIP_SCRAPE_CUTOFF)
        .order_by('employer_id')
    )
    skip_urls_by_employer_name = {
        k: [ej.application_url for ej in v]
        for k, v in groupby(recent_employer_jobs, key=lambda ej: ej.employer.employer_name)
    }

    for scraper_class in scraper_classes:
        # Allow scrapers to fail so it doesn't impact other scrapers
        employer = None
        scrapers = []
        try:
            logger.info(f'Starting scraper for {scraper_class.employer_name}')
            try:
                employer = Employer.objects.get(employer_name=scraper_class.employer_name)
            except Employer.DoesNotExist:
                pass
            
            if employer and employer.last_job_scrape_success_dt:
                last_run_diff_minutes = (timezone.now() - employer.last_job_scrape_success_dt).total_seconds() / 60
                if (not settings.DEBUG) and last_run_diff_minutes < 180:
                    logger.info(f'Scraper successfully run in last 3 hours for {scraper_class.employer_name}. Skipping')
                    continue
            
            scrapers = asyncio.run(launch_scrapers([scraper_class], skip_urls_by_employer_name))
        
            # Process raw job data
            job_processor = JobProcessor()
            logger.info(f'Processing jobs for {scraper_class.employer_name}')
            for scraper in scrapers:
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
            logger.info(f'Running `finally` block for {scraper_class.employer_name} for {len(scrapers)} scrapers')
            for scraper in scrapers:
                asyncio.run(scraper.close_connections())
