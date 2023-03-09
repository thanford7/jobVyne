from scrape.base_scrapers import BambooHrScraper, GreenhouseIframeScraper, GreenhouseScraper, WorkdayScraper


class BlueOriginScraper(WorkdayScraper):
    employer_name = 'Blue Origin'
    start_url = 'https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin'
    
    
class ClipboardHealthScraper(GreenhouseScraper):
    employer_name = 'Clipboard Health'
    start_url = 'https://boards.greenhouse.io/clipboardhealth'


class EverCommerceScraper(WorkdayScraper):
    employer_name = 'EverCommerce'
    start_url = 'https://evercommerce.wd1.myworkdayjobs.com/EverCommerce_Careers'


class InvenergyScraper(WorkdayScraper):
    employer_name = 'Invenergy'
    start_url = 'https://invenergyllc.wd1.myworkdayjobs.com/invenergycareers'
    job_department_data_automation_id = 'Department / Area-expand'
    job_department_form_data_automation_id = 'Department / Area-checkboxgroup'
    
    async def open_job_department_menu(self, page):
        await page.locator('css=[data-automation-id="more"]').click()
        await page.locator('css=[data-automation-id="Department / Area-header"]').click()
        await self.wait_for_el(page, 'div[data-automation-id="Department / Area-checkboxgroup"] label')
        

class GuildEducationScraper(GreenhouseIframeScraper):
    employer_name = 'Guild Education'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=guildeducation&b=https%3A%2F%2Fwww.guildeducation.com%2Fabout-us%2Fcareers%2Fopen-positions%2F'
        
        
class TechcyteScraper(BambooHrScraper):
    employer_name = 'Techcyte'
    start_url = 'https://techcyte.bamboohr.com/careers'
    
    
class TheMxGroupScraper(GreenhouseIframeScraper):
    employer_name = 'The MX Group'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=themxgroup&b=https%3A%2F%2Fwww.themxgroup.com%2Fcareers%2Fjob-openings%2F'

        
class TransactionNetworkServicesScraper(WorkdayScraper):
    employer_name = 'Transaction Network Services'
    start_url = 'https://tnsi.wd1.myworkdayjobs.com/Search'
    
    
class WaystarScraper(WorkdayScraper):
    employer_name = 'Waystar'
    start_url = 'https://waystar.wd1.myworkdayjobs.com/Waystar'
    
    
class YoungLivingEssentialOilsScraper(WorkdayScraper):
    employer_name = 'Young Living Essential Oils'
    start_url = 'https://youngliving.wd5.myworkdayjobs.com/YLEO'
    
    
class ZelisScraper(WorkdayScraper):
    employer_name = 'Zelis'
    start_url = 'https://zelis.wd1.myworkdayjobs.com/ZelisCareers'
    
# BlueOriginScraper.employer_name: BlueOriginScraper,
all_scrapers = {
    ClipboardHealthScraper.employer_name: ClipboardHealthScraper,
    EverCommerceScraper.employer_name: EverCommerceScraper,
    InvenergyScraper.employer_name: InvenergyScraper,
    GuildEducationScraper.employer_name: GuildEducationScraper,
    TechcyteScraper.employer_name: TechcyteScraper,
    TheMxGroupScraper.employer_name: TheMxGroupScraper,
    TransactionNetworkServicesScraper.employer_name: TransactionNetworkServicesScraper,
    WaystarScraper.employer_name: WaystarScraper,
    YoungLivingEssentialOilsScraper.employer_name: YoungLivingEssentialOilsScraper,
    ZelisScraper.employer_name: ZelisScraper
}
