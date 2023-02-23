import asyncio
import logging

from playwright.async_api import async_playwright

from scrape.base_scrapers import get_browser
from scrape.employer_scrapers import all_scrapers
from scrape.job_processor import JobProcessor
from scrape.proxy import ProxyGetter

logger = logging.getLogger(__name__)
BROWSER_COUNT = 10

        
async def launch_scrapers(scraper_classes):
    # Scrape jobs from web pages
    proxy_getter = ProxyGetter()
    async with async_playwright() as p:
        # Get a bunch of proxy browsers to avoid IP bans
        proxies = proxy_getter.get_proxies(proxy_count=BROWSER_COUNT)
        browsers = await asyncio.gather(*[get_browser(p, proxy) for proxy in proxies])
        scrapers = [sc(browsers, p, proxy_getter) for sc in scraper_classes]
        async_scrapers = [s.scrape_jobs() for s in scrapers]
        await asyncio.gather(*async_scrapers)
    
    return scrapers
    
    
def run_job_scrapers(employer_names=None):
    if not employer_names:
        scraper_classes = all_scrapers.values()
    else:
        scraper_classes = [all_scrapers[employer_name] for employer_name in employer_names]
    logger.info('Starting scrapers')
    scrapers = asyncio.run(launch_scrapers(scraper_classes))
    
    # Process raw job data
    job_processor = JobProcessor()
    logger.info('Processing jobs')
    for scraper in scrapers:
        job_processor.process_jobs(scraper.job_items)
    logger.info('Finalizing all data')
    job_processor.finalize_data()
    logger.info('Scraping complete')
