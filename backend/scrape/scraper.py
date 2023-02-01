import asyncio
import logging

from playwright.async_api import async_playwright
from aiohttp import ClientSession

from scrape.employer_scrapers import all_scrapers
from scrape.job_processor import JobProcessor

logger = logging.getLogger(__name__)
JS_LOAD_WAIT_MS = 15000
        
        
async def launch_scrapers(scraper_classes, headless=True):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        browser_context = await browser.new_context()
        browser_context.set_default_timeout(JS_LOAD_WAIT_MS)
        async with ClientSession() as session:
            scrapers = [sc(browser_context, session) for sc in scraper_classes]
            async_scrapers = [s.scrape_jobs() for s in scrapers]
            await asyncio.gather(*async_scrapers)
            job_processor = JobProcessor()
            logger.info('Processing jobs')
            for scraper in scrapers:
                job_processor.process_jobs(scraper.job_items)
            logger.info('Finalizing all data')
            job_processor.finalize_data()
            logger.info('Scraping complete')

           
def run_job_scrapers(employer_names=None):
    if not employer_names:
        scraper_classes = all_scrapers.values()
    else:
        scraper_classes = [all_scrapers[employer_name] for employer_name in employer_names]
    logger.info('Starting scrapers')
    asyncio.run(launch_scrapers(scraper_classes, headless=True))
