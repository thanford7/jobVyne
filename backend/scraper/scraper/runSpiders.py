from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.reactor import install_reactor
from twisted.internet import defer, reactor

from scraper.scraper.spiders.employers import *
from scraper.scraper import settings

# Can't use get_project_settings function because it relies on the crawler being run from the scraper working directory
crawler_settings = Settings()
crawler_settings.setmodule(settings)
# default_runner = CrawlerProcess(crawler_settings)
default_runner = CrawlerRunner(crawler_settings)

# def add_crawlers(runner, spiders):
#     if not spiders:
#         return
#     for spider in spiders:
#         runner.crawl(spider)

# @defer.inlineCallbacks
# def crawl_all(spiders):
#     if not spiders:
#         return
#     for spider in spiders:
#         yield default_runner.crawl(spider)
#
#     reactor.stop()


def crawl_all(spiders):
    if not spiders:
        return
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    for spider in spiders:
        default_runner.crawl(spider)
    
    d = default_runner.join()
    d.addBoth(lambda _: reactor.stop())


default_spiders = {
    # employer_name: SpiderClass
    BlueOriginSpider.employer_name: BlueOriginSpider
}


def run_crawlers(employer_names=None):
    print('Start crawling')
    if not employer_names:
        crawl_all(default_spiders.values())
        # add_crawlers(default_runner, list(default_spiders.values()))
    else:
        spiders = (default_spiders[employer_name] for employer_name in employer_names)
        crawl_all(spiders)
        # add_crawlers(default_runner, spiders)
    print('Finished crawling')
    reactor.run()

# if __name__ == '__main__':
#     run_crawlers()
