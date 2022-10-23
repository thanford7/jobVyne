from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from spiders.employers import *

defaultSettings = get_project_settings()
defaultRunner = CrawlerRunner(defaultSettings)


def addCrawlers(runner, spiders):
    if not spiders:
        return
    for spider in spiders:
        runner.crawl(spider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())


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

if __name__ == '__main__':
    print('Running job scraper')
    # addCrawlers(defaultRunner, defaultSpiders)
    addCrawlers(defaultRunner, [Barn2DoorSpider])
    print('Added crawlers')
    reactor.run()
