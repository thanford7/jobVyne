from scrape.base_scrapers import BambooHrScraper, GreenhouseIframeScraper, GreenhouseScraper, LeverScraper, \
    WorkdayScraper


class BenevityScraper(GreenhouseIframeScraper):
    employer_name = 'Benevity'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=benevity&b=https%3A%2F%2Fbenevity.com%2Fcareers'


class BlueOriginScraper(WorkdayScraper):
    employer_name = 'Blue Origin'
    start_url = 'https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin'
    
    
class ClipboardHealthScraper(GreenhouseScraper):
    employer_name = 'Clipboard Health'
    start_url = 'https://boards.greenhouse.io/clipboardhealth'
    
    
class DevotedHealthScraper(WorkdayScraper):
    employer_name = 'Devoted Health'
    start_url = 'https://devoted.wd1.myworkdayjobs.com/Devoted'


class EverCommerceScraper(WorkdayScraper):
    employer_name = 'EverCommerce'
    start_url = 'https://evercommerce.wd1.myworkdayjobs.com/EverCommerce_Careers'
    
    
class HealthGorillaScraper(GreenhouseIframeScraper):
    employer_name = 'Health Gorilla'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=healthgorilla&b=https%3A%2F%2Fwww.healthgorilla.com%2Fhome%2Fcompany%2Fcareers%2Fjob-openings'


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


class NylasScraper(GreenhouseScraper):
    employer_name = 'Nylas'
    start_url = 'https://boards.greenhouse.io/nylas'
    
    
class ProofpointScraper(WorkdayScraper):
    employer_name = 'Proofpoint'
    start_url = 'https://proofpoint.wd5.myworkdayjobs.com/ProofpointCareers'


class RecursionScraper(GreenhouseIframeScraper):
    employer_name = 'Recursion'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=recursionpharmaceuticals&b=https%3A%2F%2Fwww.recursion.com%2Fcareers'


class RegrowScraper(LeverScraper):
    employer_name = 'Regrow'
    start_url = 'https://jobs.lever.co/regrow.ag'

        
class TechcyteScraper(BambooHrScraper):
    employer_name = 'Techcyte'
    start_url = 'https://techcyte.bamboohr.com/careers'
    
    
class TheMxGroupScraper(GreenhouseIframeScraper):
    employer_name = 'The MX Group'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=themxgroup&b=https%3A%2F%2Fwww.themxgroup.com%2Fcareers%2Fjob-openings%2F'

        
class TransactionNetworkServicesScraper(WorkdayScraper):
    employer_name = 'Transaction Network Services'
    start_url = 'https://tnsi.wd1.myworkdayjobs.com/Search'
    
    
class VerkadaScraper(LeverScraper):
    employer_name = 'Verkada'
    start_url = 'https://jobs.lever.co/verkada/'
    
    
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
    BenevityScraper.employer_name: BenevityScraper,
    ClipboardHealthScraper.employer_name: ClipboardHealthScraper,
    DevotedHealthScraper.employer_name: DevotedHealthScraper,
    EverCommerceScraper.employer_name: EverCommerceScraper,
    InvenergyScraper.employer_name: InvenergyScraper,
    HealthGorillaScraper.employer_name: HealthGorillaScraper,
    GuildEducationScraper.employer_name: GuildEducationScraper,
    NylasScraper.employer_name: NylasScraper,
    ProofpointScraper.employer_name: ProofpointScraper,
    RecursionScraper.employer_name: RecursionScraper,
    RegrowScraper.employer_name: RegrowScraper,
    TechcyteScraper.employer_name: TechcyteScraper,
    TheMxGroupScraper.employer_name: TheMxGroupScraper,
    TransactionNetworkServicesScraper.employer_name: TransactionNetworkServicesScraper,
    VerkadaScraper.employer_name: VerkadaScraper,
    WaystarScraper.employer_name: WaystarScraper,
    YoungLivingEssentialOilsScraper.employer_name: YoungLivingEssentialOilsScraper,
    ZelisScraper.employer_name: ZelisScraper
}
