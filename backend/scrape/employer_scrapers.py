import re

from scrape.base_scrapers import BambooHrScraper, BambooHrScraper2, BreezyScraper, GreenhouseIframeScraper, \
    GreenhouseScraper, \
    LeverScraper, \
    WorkdayScraper
from scrape.custom_scraper.ebay import EbayScraper
from scrape.custom_scraper.pinterest import PinterestScraper


class AngiScraper(GreenhouseScraper):
    employer_name = 'Angi'
    start_url = 'https://boards.greenhouse.io/angi'
    
    
class AtlassianScraper(LeverScraper):
    employer_name = 'Atlassian'
    start_url = 'https://jobs.lever.co/atlassian'
    
    
class AtomicScraper(LeverScraper):
    employer_name = 'Atomic'
    start_url = 'https://jobs.lever.co/atomic'


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
    
    
class ForwardScraper(LeverScraper):
    employer_name = 'Forward'
    start_url = 'https://jobs.lever.co/goforward'
    
    
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
        
        
class KandjiScraper(LeverScraper):
    employer_name = 'Kandji'
    start_url = 'https://jobs.lever.co/kandji'
        

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
    
    
class LeanDataScraper(LeverScraper):
    employer_name = 'Lean Data'
    start_url = 'https://jobs.lever.co/leandatainc'


class LiveViewTechnologiesScraper(BambooHrScraper):
    employer_name = 'LiveView Technologies'
    start_url = 'https://lvt.bamboohr.com/careers'


class LucidSoftwareScraper(GreenhouseScraper):
    employer_name = 'Lucid Software'
    start_url = 'https://boards.greenhouse.io/lucidsoftware'
    
    
class MetabaseScraper(LeverScraper):
    employer_name = 'Metabase'
    start_url = 'https://jobs.lever.co/metabase'
    
    
class MindbloomScraper(LeverScraper):
    employer_name = 'Mindbloom'
    start_url = 'https://jobs.lever.co/mindbloom'
    
    
class NavaScraper(LeverScraper):
    employer_name = 'Nava'
    start_url = 'https://jobs.lever.co/nava'
    
    
class NiceScraper(GreenhouseIframeScraper):
    GREENHOUSE_JOB_BOARD_DOMAIN = 'nice'
    employer_name = 'Nice'
    start_url = 'https://boards.greenhouse.io/embed/job_board?for=nice'


class NylasScraper(GreenhouseScraper):
    employer_name = 'Nylas'
    start_url = 'https://boards.greenhouse.io/nylas'
    
    
class PerpayScraper(LeverScraper):
    employer_name = 'Perpay'
    start_url = 'https://jobs.lever.co/perpay'
    
    
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
    
    
class StubHubScraper(LeverScraper):
    employer_name = 'StubHub'
    start_url = 'https://jobs.lever.co/StubHubHoldings'

        
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
    
    
class VestaTechScraper(LeverScraper):
    employer_name = 'Vesta Tech'
    start_url = 'https://jobs.lever.co/vesta-tech'
    
    
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
    
    
class SideScraper(LeverScraper):
    employer_name = 'Side'
    start_url = 'https://jobs.lever.co/sideinc'
    
    
class CuldesacScraper(LeverScraper):
    employer_name = 'Culdesac'
    start_url = 'https://jobs.lever.co/culdesac'
    
    
class MetronomeScraper(LeverScraper):
    employer_name = 'Metronome'
    start_url = 'https://jobs.lever.co/getmetronome'
    
    
class KlarnaScraper(LeverScraper):
    employer_name = 'Klarna'
    start_url = 'https://jobs.lever.co/klarna'
    
    
class CoformaScraper(LeverScraper):
    employer_name = 'Coforma'
    start_url = 'https://jobs.lever.co/coforma'
    
    
class BrightwheelScraper(LeverScraper):
    employer_name = 'Brightwheel'
    start_url = 'https://jobs.lever.co/brightwheel'
    
    
class MaterialSecurityScraper(LeverScraper):
    employer_name = 'Material Security'
    start_url = 'https://jobs.lever.co/MaterialSecurity'
    
    
class WhoopScraper(LeverScraper):
    employer_name = 'Whoop'
    start_url = 'https://jobs.lever.co/whoop'
    
    
class AttentiveScraper(LeverScraper):
    employer_name = 'Attentive'
    start_url = 'https://jobs.lever.co/attentive'
    
    
class WealthsimpleScraper(LeverScraper):
    employer_name = 'Wealthsimple'
    start_url = 'https://jobs.lever.co/wealthsimple'
    
    
class FanaticsScraper(LeverScraper):
    employer_name = 'Fanatics'
    start_url = 'https://jobs.lever.co/fanatics'
    
    
class PlusgradeScraper(LeverScraper):
    employer_name = 'Plusgrade'
    start_url = 'https://jobs.lever.co/plusgrade'
    
    
class LinktreeScraper(LeverScraper):
    employer_name = 'Linktree'
    start_url = 'https://jobs.lever.co/linktree'
    
    
class KickstarterScraper(LeverScraper):
    employer_name = 'Kickstarter'
    start_url = 'https://jobs.lever.co/kickstarter'
    
    
class AnthropicScraper(LeverScraper):
    employer_name = 'Anthropic'
    start_url = 'https://jobs.lever.co/Anthropic'
    
    
class ElsevierScraper(WorkdayScraper):
    employer_name = 'Elsevier'
    start_url = 'https://relx.wd3.myworkdayjobs.com/ElsevierJobs'
    
    
class OverjetScraper(GreenhouseScraper):
    employer_name = 'Overjet'
    start_url = 'https://boards.greenhouse.io/overjet'
    
    
class TwoULaundry(BreezyScraper):
    employer_name = '2ULaundry'
    start_url = 'https://2ulaundry.breezy.hr/'

    
# BlueOriginScraper.employer_name: BlueOriginScraper,
# EbayScraper.employer_name: EbayScraper,
all_scrapers = {
    AngiScraper.employer_name: AngiScraper,
    AnthropicScraper.employer_name: AnthropicScraper,
    AtlassianScraper.employer_name: AtlassianScraper,
    AtomicScraper.employer_name: AtomicScraper,
    AttentiveScraper.employer_name: AttentiveScraper,
    BenevityScraper.employer_name: BenevityScraper,
    BrightwheelScraper.employer_name: BrightwheelScraper,
    CHGHealthcareScraper.employer_name: CHGHealthcareScraper,
    CircleScraper.employer_name: CircleScraper,
    ClozdScraper.employer_name: ClozdScraper,
    ClipboardHealthScraper.employer_name: ClipboardHealthScraper,
    CuldesacScraper.employer_name: CuldesacScraper,
    DevotedHealthScraper.employer_name: DevotedHealthScraper,
    ElsevierScraper.employer_name: ElsevierScraper,
    EntrataScraper.employer_name: EntrataScraper,
    EverCommerceScraper.employer_name: EverCommerceScraper,
    FICOScraper.employer_name: FICOScraper,
    ForwardScraper.employer_name: ForwardScraper,
    GalileoScraper.employer_name: GalileoScraper,
    GuildEducationScraper.employer_name: GuildEducationScraper,
    HealthGorillaScraper.employer_name: HealthGorillaScraper,
    HopperScraper.employer_name: HopperScraper,
    InvenergyScraper.employer_name: InvenergyScraper,
    KandjiScraper.employer_name: KandjiScraper,
    KlarnaScraper.employer_name: KlarnaScraper,
    LaticreteInternationalScraper.employer_name: LaticreteInternationalScraper,
    LeanDataScraper.employer_name: LeanDataScraper,
    LinktreeScraper.employer_name: LinktreeScraper,
    LiveViewTechnologiesScraper.employer_name: LiveViewTechnologiesScraper,
    LucidSoftwareScraper.employer_name: LucidSoftwareScraper,
    MaterialSecurityScraper.employer_name: MaterialSecurityScraper,
    MetabaseScraper.employer_name: MetabaseScraper,
    MetronomeScraper.employer_name: MetronomeScraper,
    MindbloomScraper.employer_name: MindbloomScraper,
    NavaScraper.employer_name: NavaScraper,
    NiceScraper.employer_name: NiceScraper,
    NylasScraper.employer_name: NylasScraper,
    PerpayScraper.employer_name: PerpayScraper,
    PinterestScraper.employer_name: PinterestScraper,
    PlusgradeScraper.employer_name: PlusgradeScraper,
    ProofpointScraper.employer_name: ProofpointScraper,
    RecursionScraper.employer_name: RecursionScraper,
    RegrowScraper.employer_name: RegrowScraper,
    RoScraper.employer_name: RoScraper,
    SideScraper.employer_name: SideScraper,
    StubHubScraper.employer_name: StubHubScraper,
    TechcyteScraper.employer_name: TechcyteScraper,
    TendoScraper.employer_name: TendoScraper,
    TheMxGroupScraper.employer_name: TheMxGroupScraper,
    TransactionNetworkServicesScraper.employer_name: TransactionNetworkServicesScraper,
    TwoULaundry.employer_name: TwoULaundry,
    VasionScraper.employer_name: VasionScraper,
    VeevaScraper.employer_name: VeevaScraper,
    VerkadaScraper.employer_name: VerkadaScraper,
    VestaTechScraper.employer_name: VestaTechScraper,
    VirtaHealthScraper.employer_name: VirtaHealthScraper,
    VivianHealthScraper.employer_name: VivianHealthScraper,
    WaystarScraper.employer_name: WaystarScraper,
    WealthsimpleScraper.employer_name: WealthsimpleScraper,
    WhoopScraper.employer_name: WhoopScraper,
    YoungLivingEssentialOilsScraper.employer_name: YoungLivingEssentialOilsScraper,
    ZelisScraper.employer_name: ZelisScraper
}
