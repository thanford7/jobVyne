import re

from scrape.base_scrapers import BambooHrScraper, BambooHrScraper2, GreenhouseIframeScraper, GreenhouseScraper, \
    LeverScraper, \
    WorkdayScraper
from scrape.custom_scraper.ebay import EbayScraper


class AngiScraper(GreenhouseScraper):
    employer_name = 'Angi'
    start_url = 'https://boards.greenhouse.io/angi'


class BenevityScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'benevity'
    employer_name = 'Benevity'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=benevity&b=https%3A%2F%2Fbenevity.com%2Fcareers'


class BlueOriginScraper(WorkdayScraper):
    employer_name = 'Blue Origin'
    start_url = 'https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin'
    
    
class CHGHealthcareScraper(WorkdayScraper):
    employer_name = 'CHG Healthcare'
    start_url = 'https://chghealthcare.wd1.myworkdayjobs.com/External'
    job_department_data_automation_id = 'jobFamily'
    job_department_form_data_automation_id = 'jobFamilyCheckboxGroup'
    
    
class CircleScraper(GreenhouseScraper):
    employer_name = 'Circle'
    start_url = 'https://boards.greenhouse.io/circle'
    
    
class ClipboardHealthScraper(GreenhouseScraper):
    employer_name = 'Clipboard Health'
    start_url = 'https://boards.greenhouse.io/clipboardhealth'
    
    
class ClozdScraper(LeverScraper):
    employer_name = 'Clozd'
    start_url = 'https://jobs.lever.co/Clozd'
    
    
class DevotedHealthScraper(WorkdayScraper):
    employer_name = 'Devoted Health'
    start_url = 'https://devoted.wd1.myworkdayjobs.com/Devoted'
    
    
class EntrataScraper(LeverScraper):
    employer_name = 'Entrata'
    start_url = 'https://jobs.lever.co/entrata'


class EverCommerceScraper(WorkdayScraper):
    employer_name = 'EverCommerce'
    start_url = 'https://evercommerce.wd1.myworkdayjobs.com/EverCommerce_Careers'
    
    
class FICOScraper(WorkdayScraper):
    employer_name = 'FICO'
    start_url = 'https://fico.wd1.myworkdayjobs.com/External'
    
    
class HealthGorillaScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'healthgorilla'
    employer_name = 'Health Gorilla'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=healthgorilla&b=https%3A%2F%2Fwww.healthgorilla.com%2Fhome%2Fcompany%2Fcareers%2Fjob-openings'
    
    
class HopperScraper(LeverScraper):
    employer_name = 'Hopper'
    start_url = 'https://jobs.lever.co/hopper'


class InvenergyScraper(WorkdayScraper):
    employer_name = 'Invenergy'
    start_url = 'https://invenergyllc.wd1.myworkdayjobs.com/invenergycareers'
    job_department_data_automation_id = 'Department / Area-expand'
    job_department_form_data_automation_id = 'Department / Area-checkboxgroup'
    
    async def open_job_department_menu(self, page):
        await page.locator('css=[data-automation-id="more"]').click()
        await page.locator('css=[data-automation-id="Department / Area-header"]').click()
        await self.wait_for_el(page, 'div[data-automation-id="Department / Area-checkboxgroup"] label')
        

class GalileoScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'galileo'
    employer_name = 'Galileo'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=galileo'


class GuildEducationScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'guild'
    employer_name = 'Guild Education'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=guild&b=https%3A%2F%2Fwww.guild.com%2Fopen-positions-at-guild'


class LaticreteInternationalScraper(WorkdayScraper):
    employer_name = 'LATICRETE International'
    start_url = 'https://laticrete.wd1.myworkdayjobs.com/laticreteinternational'


class LiveViewTechnologiesScraper(BambooHrScraper):
    employer_name = 'LiveView Technologies'
    start_url = 'https://lvt.bamboohr.com/careers'


class LucidSoftwareScraper(GreenhouseScraper):
    employer_name = 'Lucid Software'
    start_url = 'https://boards.greenhouse.io/lucidsoftware'
    
    
class NiceScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'nice'
    employer_name = 'Nice'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=nice'


class NylasScraper(GreenhouseScraper):
    employer_name = 'Nylas'
    start_url = 'https://boards.greenhouse.io/nylas'
    
    
class ProofpointScraper(WorkdayScraper):
    employer_name = 'Proofpoint'
    start_url = 'https://proofpoint.wd5.myworkdayjobs.com/ProofpointCareers'


class RecursionScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'recursionpharmaceuticals'
    employer_name = 'Recursion'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=recursionpharmaceuticals&b=https%3A%2F%2Fwww.recursion.com%2Fcareers'


class RegrowScraper(LeverScraper):
    employer_name = 'Regrow'
    start_url = 'https://jobs.lever.co/regrow.ag'
    
    
class RoScraper(LeverScraper):
    employer_name = 'Ro'
    start_url = 'https://jobs.lever.co/ro'

        
class TechcyteScraper(BambooHrScraper):
    employer_name = 'Techcyte'
    start_url = 'https://techcyte.bamboohr.com/careers'
    
    
class TendoScraper(LeverScraper):
    employer_name = 'Tendo'
    start_url = 'https://jobs.lever.co/tendo'
    
    
class TheMxGroupScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'themxgroup'
    employer_name = 'The MX Group'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=themxgroup&b=https%3A%2F%2Fwww.themxgroup.com%2Fcareers%2Fjob-openings%2F'

        
class TransactionNetworkServicesScraper(WorkdayScraper):
    employer_name = 'Transaction Network Services'
    start_url = 'https://tnsi.wd1.myworkdayjobs.com/Search'
    
    
class VasionScraper(BambooHrScraper2):
    employer_name = 'Vasion'
    start_url = 'https://printerlogic.bamboohr.com/jobs/'
    
    
class VeevaScraper(LeverScraper):
    employer_name = 'Veeva'
    start_url = 'https://jobs.lever.co/veeva/'
    
    def normalize_job_department(self, job_department):
        job_department_parts = re.split('[-–]', job_department)
        return job_department_parts[0].strip()
    
    
class VerkadaScraper(LeverScraper):
    employer_name = 'Verkada'
    start_url = 'https://jobs.lever.co/verkada/'
    
    
class VirtaHealthScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'virtahealth'
    employer_name = 'Virta Health'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=virtahealth'
    
    
class VivianHealthScraper(GreenhouseScraper):
    employer_name = 'Vivian Health'
    start_url = 'https://boards.greenhouse.io/vivian'
    
    
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
    AngiScraper.employer_name: AngiScraper,
    BenevityScraper.employer_name: BenevityScraper,
    CHGHealthcareScraper.employer_name: CHGHealthcareScraper,
    CircleScraper.employer_name: CircleScraper,
    ClozdScraper.employer_name: ClozdScraper,
    ClipboardHealthScraper.employer_name: ClipboardHealthScraper,
    DevotedHealthScraper.employer_name: DevotedHealthScraper,
    EbayScraper.employer_name: EbayScraper,
    EntrataScraper.employer_name: EntrataScraper,
    EverCommerceScraper.employer_name: EverCommerceScraper,
    FICOScraper.employer_name: FICOScraper,
    GalileoScraper.employer_name: GalileoScraper,
    GuildEducationScraper.employer_name: GuildEducationScraper,
    HealthGorillaScraper.employer_name: HealthGorillaScraper,
    HopperScraper.employer_name: HopperScraper,
    InvenergyScraper.employer_name: InvenergyScraper,
    LaticreteInternationalScraper.employer_name: LaticreteInternationalScraper,
    LiveViewTechnologiesScraper.employer_name: LiveViewTechnologiesScraper,
    LucidSoftwareScraper.employer_name: LucidSoftwareScraper,
    NiceScraper.employer_name: NiceScraper,
    NylasScraper.employer_name: NylasScraper,
    ProofpointScraper.employer_name: ProofpointScraper,
    RecursionScraper.employer_name: RecursionScraper,
    RegrowScraper.employer_name: RegrowScraper,
    RoScraper.employer_name: RoScraper,
    TechcyteScraper.employer_name: TechcyteScraper,
    TendoScraper.employer_name: TendoScraper,
    TheMxGroupScraper.employer_name: TheMxGroupScraper,
    TransactionNetworkServicesScraper.employer_name: TransactionNetworkServicesScraper,
    VasionScraper.employer_name: VasionScraper,
    VeevaScraper.employer_name: VeevaScraper,
    VerkadaScraper.employer_name: VerkadaScraper,
    VirtaHealthScraper.employer_name: VirtaHealthScraper,
    VivianHealthScraper.employer_name: VivianHealthScraper,
    WaystarScraper.employer_name: WaystarScraper,
    YoungLivingEssentialOilsScraper.employer_name: YoungLivingEssentialOilsScraper,
    ZelisScraper.employer_name: ZelisScraper
}
