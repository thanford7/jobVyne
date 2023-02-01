from scrape.base_scrapers import WorkdayScraper


class BlueOriginScraper(WorkdayScraper):
    employer_name = 'Blue Origin'
    start_url = 'https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin'

all_scrapers = {
    BlueOriginScraper.employer_name: BlueOriginScraper
}
