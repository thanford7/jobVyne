from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraper.scraper.spiders.employers import *
from scraper.scraper import settings

# Can't use get_project_settings function because it relies on the crawler being run from the scraper working directory
crawler_settings = Settings()
crawler_settings.setmodule(settings)
defaultRunner = CrawlerProcess(crawler_settings)


def add_crawlers(runner, spiders):
    if not spiders:
        return
    for spider in spiders:
        runner.crawl(spider)


defaultSpiders = [
    AttentiveSpider,
    Barn2DoorSpider,
    BounteousSpider,
    BlockRenovationSpider,
    ComplyAdvantageSpider,
    ExabeamSpider,
    GradleSpider,
    HavenlySpider,
    CoverGeniusSpider,
    CurologySpider,
    DISQOSpider,
    FlorenceHealthcareSpider,
    FLYRLabsSpider,
    FountainSpider,
    HiveSpider,
    HospitalIQSpider,
    IroncladSpider,
    JerrySpider,
    KandjiSpider,
    KindbodySpider,
    LeapSpider,
    LiberisSpider,
    LinkSquaresSpider,
    MediaflySpider,
    MolocoSpider,
    NomadHealthSpider,
    OnnaSpider,
    OutschoolSpider,
    PilotSpider,
    ProdegeSpider,
    QuartetHealthSpider,
    QuipSpider,
    ZoomoSpider
]


def run_crawlers():
    print('Running job scraper')
    # addCrawlers(defaultRunner, defaultSpiders)
    add_crawlers(defaultRunner, [HospitalIQSpider])
    print('Added crawlers')
    defaultRunner.start()

# if __name__ == '__main__':
#     run_crawlers()
