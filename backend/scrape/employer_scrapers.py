from scrape.base_scrapers import GreenhouseScraper, WorkdayScraper


class BlueOriginScraper(WorkdayScraper):
    employer_name = 'Blue Origin'
    start_url = 'https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin'
    

class InvenergyScraper(WorkdayScraper):
    employer_name = 'Invenergy'
    start_url = 'https://invenergyllc.wd1.myworkdayjobs.com/invenergycareers'
    job_department_data_automation_id = 'Department / Area-expand'
    job_department_form_data_automation_id = 'Department / Area-checkboxgroup'
    
    async def open_job_department_menu(self, page):
        await page.locator('css=[data-automation-id="more"]').click()
        await page.locator('css=[data-automation-id="Department / Area-header"]').click()
        await self.wait_for_el(page, 'div[data-automation-id="Department / Area-checkboxgroup"] label')
        

class GuildEducationScraper(GreenhouseScraper):
    IS_JS_REQUIRED = True
    employer_name = 'Guild Education'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=guildeducation&b=https%3A%2F%2Fwww.guildeducation.com%2Fabout-us%2Fcareers%2Fopen-positions%2F'
    job_item_page_wait_sel = None
    
    async def do_job_page_js(self, page):
        html_dom = await self.get_page_html(page)
        iframe_url = html_dom.xpath('//*[@id="grnhse_iframe"]/@src').get()
        await page.goto(iframe_url)

all_scrapers = {
    BlueOriginScraper.employer_name: BlueOriginScraper,
    InvenergyScraper.employer_name: InvenergyScraper,
    GuildEducationScraper.employer_name: GuildEducationScraper,
}
