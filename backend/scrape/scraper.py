import asyncio
import logging

from playwright.async_api import async_playwright

from jvapp.models import Employer
from scrape.employer_scrapers import all_scrapers
from scrape.job_processor import JobProcessor

logger = logging.getLogger(__name__)
JS_LOAD_WAIT_MS = 30000


async def get_browser(playwright):
    browser = await playwright.chromium.launch(headless=True)
    browser_context = await browser.new_context()
    browser_context.set_default_timeout(JS_LOAD_WAIT_MS)
    return browser

        
async def launch_scrapers(scraper_classes):
    # Scrape jobs from web pages
    async with async_playwright() as p:
        browser = await get_browser(p)
        scrapers = [sc(p, browser) for sc in scraper_classes]
        async_scrapers = [s.scrape_jobs() for s in scrapers]
        await asyncio.gather(*async_scrapers)
    
    return scrapers
    
    
def run_job_scrapers(employer_names=None):
    if not employer_names:
        scraper_classes = all_scrapers.values()
    else:
        scraper_classes = [all_scrapers[employer_name] for employer_name in employer_names]
    
    for scraper_class in scraper_classes:
        # Allow scrapers to fail so it doesn't impact other scrapers
        try:
            logger.info(f'Starting scraper for {scraper_class.employer_name}')
            scrapers = asyncio.run(launch_scrapers([scraper_class]))
        
            # Process raw job data
            job_processor = JobProcessor()
            logger.info(f'Processing jobs for {scraper_class.employer_name}')
            for scraper in scrapers:
                job_processor.process_jobs(scraper.job_items)
            logger.info(f'Finalizing all data for {scraper_class.employer_name}')
            job_processor.finalize_data()
            logger.info(f'Scraping complete for {scraper_class.employer_name}')
        except Exception as e:
            employer = Employer.objects.get(employer_name=scraper_class.employer_name)
            employer.has_job_scrape_failure = True
            employer.save()
            logger.exception(f'Error occurred while scraping jobs for {scraper_class.employer_name}', exc_info=e)
