import re

from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from scrape.base_scrapers import ApplicantProScraper, AshbyHQScraper, BambooHrScraper, BreezyScraper, \
    GreenhouseApiScraper, GreenhouseIframeScraper, \
    GreenhouseScraper, \
    LeverScraper, \
    PaylocityScraper, SmartRecruitersScraper, StandardJsScraper, StandardScraper, UltiProScraper, WorkableScraper, \
    WorkdayScraper
from scrape.custom_scraper.ancestry import AncestryScraper
from scrape.custom_scraper.ebay import EbayScraper
from scrape.custom_scraper.packsize import PacksizeScraper


class AngiScraper(GreenhouseScraper):
    employer_name = 'Angi'
    EMPLOYER_KEY = 'angi'
    
    
class AtlassianScraper(LeverScraper):
    employer_name = 'Atlassian'
    EMPLOYER_KEY = 'atlassian'
    
    
class AtomicScraper(LeverScraper):
    employer_name = 'Atomic'
    EMPLOYER_KEY = 'atomic'


class BenevityScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'benevity'
    employer_name = 'Benevity'


class BlueOriginScraper(WorkdayScraper):
    employer_name = 'Blue Origin'
    start_url = 'https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin/'
    
    
class CHGHealthcareScraper(WorkdayScraper):
    employer_name = 'CHG Healthcare'
    start_url = 'https://chghealthcare.wd1.myworkdayjobs.com/External/'
    job_department_menu_data_automation_id = 'jobFamily'
    job_department_form_data_automation_id = 'jobFamilyCheckboxGroup'
    
    
class CircleScraper(GreenhouseScraper):
    employer_name = 'Circle'
    EMPLOYER_KEY = 'circle'
    
    
class ClipboardHealthScraper(GreenhouseScraper):
    employer_name = 'Clipboard Health'
    EMPLOYER_KEY = 'clipboardhealth'
    
    
class ClozdScraper(LeverScraper):
    employer_name = 'Clozd'
    EMPLOYER_KEY = 'Clozd'
    
    
class DevotedHealthScraper(WorkdayScraper):
    employer_name = 'Devoted Health'
    start_url = 'https://devoted.wd1.myworkdayjobs.com/Devoted/'
    
    
class EntrataScraper(LeverScraper):
    employer_name = 'Entrata'
    EMPLOYER_KEY = 'entrata'


class EverCommerceScraper(WorkdayScraper):
    employer_name = 'EverCommerce'
    start_url = 'https://evercommerce.wd1.myworkdayjobs.com/EverCommerce_Careers/'
    
    
class FICOScraper(WorkdayScraper):
    employer_name = 'FICO'
    start_url = 'https://fico.wd1.myworkdayjobs.com/External/'
    
    
class ForwardScraper(LeverScraper):
    employer_name = 'Forward'
    EMPLOYER_KEY = 'goforward'
    
    
class HealthGorillaScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'healthgorilla'
    employer_name = 'Health Gorilla'
    
    
class HopperScraper(LeverScraper):
    employer_name = 'Hopper'
    EMPLOYER_KEY = 'hopper'


class InvenergyScraper(WorkdayScraper):
    employer_name = 'Invenergy'
    start_url = 'https://invenergyllc.wd1.myworkdayjobs.com/invenergycareers/'
    job_department_menu_data_automation_id = 'Department / Area-expand'
    job_department_form_data_automation_id = 'Department / Area-checkboxgroup'
    
    async def open_job_department_menu(self, page):
        try:
            await page.locator('css=[data-automation-id="more"]').click()
        except PlaywrightTimeoutError:
            # Try again
            await self.reload_page(page)
            await page.locator('css=[data-automation-id="more"]').click()
        await page.locator('css=[data-automation-id="Department / Area-header"]').click()
        await self.wait_for_el(page, 'div[data-automation-id="Department / Area-checkboxgroup"] label')
        
        
class KandjiScraper(LeverScraper):
    employer_name = 'Kandji'
    EMPLOYER_KEY = 'kandji'
    

class GalileoScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'galileo'
    employer_name = 'Galileo'


class GuildEducationScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'guild'
    employer_name = 'Guild Education'


class LaticreteInternationalScraper(WorkdayScraper):
    employer_name = 'LATICRETE International'
    start_url = 'https://laticrete.wd1.myworkdayjobs.com/laticreteinternational/'
    
    
class LeanDataScraper(LeverScraper):
    employer_name = 'Lean Data'
    EMPLOYER_KEY = 'leandatainc'


class LiveViewTechnologiesScraper(BambooHrScraper):
    EMPLOYER_KEY = 'lvt'
    employer_name = 'LiveView Technologies'


class LucidSoftwareScraper(GreenhouseScraper):
    employer_name = 'Lucid Software'
    EMPLOYER_KEY = 'lucidsoftware'
    
    
class MetabaseScraper(LeverScraper):
    employer_name = 'Metabase'
    EMPLOYER_KEY = 'metabase'
    
    
class MindbloomScraper(LeverScraper):
    employer_name = 'Mindbloom'
    EMPLOYER_KEY = 'mindbloom'
    
    
class NavaScraper(LeverScraper):
    employer_name = 'Nava'
    EMPLOYER_KEY = 'nava'
    
    
class NiceScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'nice'
    employer_name = 'Nice'


class NylasScraper(GreenhouseScraper):
    employer_name = 'Nylas'
    EMPLOYER_KEY = 'nylas'
    
    
class PerpayScraper(LeverScraper):
    employer_name = 'Perpay'
    EMPLOYER_KEY = 'perpay'
    
    
class ProofpointScraper(WorkdayScraper):
    employer_name = 'Proofpoint'
    start_url = 'https://proofpoint.wd5.myworkdayjobs.com/ProofpointCareers/'


class RecursionScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'recursionpharmaceuticals'
    employer_name = 'Recursion'


class RegrowScraper(LeverScraper):
    employer_name = 'Regrow'
    EMPLOYER_KEY = 'regrow.ag'
    
    
class RoScraper(LeverScraper):
    employer_name = 'Ro'
    EMPLOYER_KEY = 'ro'
    
    
class StubHubScraper(LeverScraper):
    employer_name = 'StubHub'
    EMPLOYER_KEY = 'StubHubHoldings'

        
class TechcyteScraper(BambooHrScraper):
    EMPLOYER_KEY = 'techcyte'
    employer_name = 'Techcyte'
    
    
class TendoScraper(LeverScraper):
    employer_name = 'Tendo'
    EMPLOYER_KEY = 'tendo'
    
    
class TheMxGroupScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'themxgroup'
    employer_name = 'The MX Group'

        
class TransactionNetworkServicesScraper(WorkdayScraper):
    employer_name = 'Transaction Network Services'
    start_url = 'https://tnsi.wd1.myworkdayjobs.com/Search/'
    
    
class VasionScraper(WorkableScraper):
    employer_name = 'Vasion'
    EMPLOYER_KEY = 'vasion'
    
    
class VeevaScraper(LeverScraper):
    employer_name = 'Veeva'
    EMPLOYER_KEY = 'veeva'
    
    def normalize_job_department(self, job_department):
        job_department_parts = re.split('[-–]', job_department)
        return job_department_parts[0].strip()
    
    
class VerkadaScraper(LeverScraper):
    employer_name = 'Verkada'
    EMPLOYER_KEY = 'verkada'
    
    
class VestaTechScraper(LeverScraper):
    employer_name = 'Vesta Tech'
    EMPLOYER_KEY = 'vesta-tech'
    
    
class VirtaHealthScraper(AshbyHQScraper):
    EMPLOYER_KEY = 'virtahealth'
    employer_name = 'Virta Health'
    
    
class VivianHealthScraper(GreenhouseScraper):
    employer_name = 'Vivian Health'
    EMPLOYER_KEY = 'vivian'
    
    
class WaystarScraper(WorkdayScraper):
    employer_name = 'Waystar'
    start_url = 'https://waystar.wd1.myworkdayjobs.com/Waystar/'
    
    
class YoungLivingEssentialOilsScraper(WorkdayScraper):
    employer_name = 'Young Living Essential Oils'
    start_url = 'https://youngliving.wd5.myworkdayjobs.com/YLEO/'
    
    
class ZelisScraper(WorkdayScraper):
    employer_name = 'Zelis'
    start_url = 'https://zelis.wd1.myworkdayjobs.com/ZelisCareers/'
    
    
class SideScraper(LeverScraper):
    employer_name = 'Side'
    EMPLOYER_KEY = 'sideinc'
    
    
class CuldesacScraper(LeverScraper):
    employer_name = 'Culdesac'
    EMPLOYER_KEY = 'culdesac'
    
    
class MetronomeScraper(LeverScraper):
    employer_name = 'Metronome'
    EMPLOYER_KEY = 'getmetronome'
    
    
class KlarnaScraper(LeverScraper):
    employer_name = 'Klarna'
    EMPLOYER_KEY = 'klarna'
    
    
class CoformaScraper(LeverScraper):
    employer_name = 'Coforma'
    EMPLOYER_KEY = 'coforma'
    
    
class BrightwheelScraper(LeverScraper):
    employer_name = 'Brightwheel'
    EMPLOYER_KEY = 'brightwheel'
    
    
class MaterialSecurityScraper(LeverScraper):
    employer_name = 'Material Security'
    EMPLOYER_KEY = 'MaterialSecurity'
    
    
class WhoopScraper(LeverScraper):
    employer_name = 'Whoop'
    EMPLOYER_KEY = 'whoop'
    
    
class AttentiveScraper(LeverScraper):
    employer_name = 'Attentive'
    EMPLOYER_KEY = 'attentive'
    
    
class WealthsimpleScraper(LeverScraper):
    employer_name = 'Wealthsimple'
    EMPLOYER_KEY = 'wealthsimple'
    
    
class FanaticsScraper(LeverScraper):
    employer_name = 'Fanatics'
    EMPLOYER_KEY = 'fanatics'
    
    
class PlusgradeScraper(LeverScraper):
    employer_name = 'Plusgrade'
    EMPLOYER_KEY = 'plusgrade'
    
    
class LinktreeScraper(LeverScraper):
    employer_name = 'Linktree'
    EMPLOYER_KEY = 'linktree'
    
    
class KickstarterScraper(LeverScraper):
    employer_name = 'Kickstarter'
    EMPLOYER_KEY = 'kickstarter'
    
    
class AnthropicScraper(LeverScraper):
    employer_name = 'Anthropic'
    EMPLOYER_KEY = 'Anthropic'
    
    
class ElsevierScraper(WorkdayScraper):
    employer_name = 'Elsevier'
    start_url = 'https://relx.wd3.myworkdayjobs.com/ElsevierJobs/'
    
    
class OverjetScraper(GreenhouseScraper):
    employer_name = 'Overjet'
    EMPLOYER_KEY = 'overjet'
    
    
class TwoULaundryScraper(BreezyScraper):
    employer_name = '2ULaundry'
    EMPLOYER_KEY = '2ulaundry'
    
    
class ZocdocScraper(GreenhouseApiScraper):
    EMPLOYER_KEY = 'zocdoc'
    employer_name = 'Zocdoc'
    
    
class AvettaScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'avetta'
    employer_name = 'Avetta'
    
    
class KoalaHealthScraper(LeverScraper):
    employer_name = 'Koala Health'
    EMPLOYER_KEY = 'koalahealth'
    
    
class CambiaHealthSolutionsScraper(WorkdayScraper):
    employer_name = 'Cambia Health Solutions'
    start_url = 'https://cambiahealth.wd1.myworkdayjobs.com/External/'
    job_department_menu_data_automation_id = 'Job_Category'
    job_department_form_data_automation_id = 'Job_CategoryCheckboxGroup'
    
    
class AffirmScraper(GreenhouseScraper):
    employer_name = 'Affirm'
    EMPLOYER_KEY = 'affirm'
    
    
class AddeparScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'addepar1'
    employer_name = 'Addepar'
    

class WaymarkScraper(GreenhouseScraper):
    employer_name = 'Waymark'
    EMPLOYER_KEY = 'waymark'
    
    
class VivintScraper(WorkdayScraper):
    employer_name = 'Vivint'
    start_url = 'https://vivint.wd5.myworkdayjobs.com/vivintjobs/'
    has_job_departments = False
    
    
class FabricScraper(LeverScraper):
    employer_name = 'fabric'
    EMPLOYER_KEY = 'fabric'
    
    
class UnderdogFantasyScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'underdogfantasy'
    employer_name = 'Underdog Fantasy'
    

class TixrScraper(LeverScraper):
    employer_name = 'Tixr'
    EMPLOYER_KEY = 'Tixr'
    
    
class Mach49Scraper(GreenhouseScraper):
    employer_name = 'Mach49'
    EMPLOYER_KEY = 'mach49'
    
    
class HouzzScraper(WorkdayScraper):
    employer_name = 'Houzz'
    start_url = 'https://houzz.wd5.myworkdayjobs.com/External/'
    
    
class AccessoScraper(LeverScraper):
    employer_name = 'accesso'
    EMPLOYER_KEY = 'accesso'
    
    
class SeedHealthScraper(GreenhouseScraper):
    employer_name = 'Seed Health'
    EMPLOYER_KEY = 'seed'
    

class RoktScraper(WorkableScraper):
    employer_name = 'Rokt'
    EMPLOYER_KEY = 'rokt'
    
    
class ConsensusScraper(LeverScraper):
    employer_name = 'Consensus'
    EMPLOYER_KEY = 'goconsensus'
    
    
class LoopScraper(GreenhouseScraper):
    employer_name = 'Loop'
    EMPLOYER_KEY = 'loop'
    

class LoopReturnsScraper(LeverScraper):
    employer_name = 'Loop Returns'
    EMPLOYER_KEY = 'loopreturns'
    
    
class SentiLinkScraper(GreenhouseScraper):
    employer_name = 'SentiLink'
    EMPLOYER_KEY = 'sentilink'
    

class GrayDigitalScraper(GreenhouseScraper):
    employer_name = 'Gray Digital'
    EMPLOYER_KEY = 'graydigital'
    
    
class FoursquareScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'foursquare26'
    employer_name = 'Foursquare'
    
    
class StashScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'stashinvest'
    employer_name = 'Stash'
    

class NacelleScraper(GreenhouseScraper):
    employer_name = 'Nacelle'
    EMPLOYER_KEY = 'nacelle'
    
    
class CopilotIQScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = 'copilotiq'
    employer_name = 'CopilotIQ'
    
    
class OmadaHealthScraper(GreenhouseScraper):
    employer_name = 'Omada Health'
    EMPLOYER_KEY = 'omadahealth'
    
    
class WeaveHQScraper(GreenhouseScraper):
    employer_name = 'Weave HQ'
    EMPLOYER_KEY = 'weavehq'
    

class One800ContactsScraper(GreenhouseIframeScraper):
    EMPLOYER_KEY = '1800contacts'
    employer_name = '1-800 Contacts'
    
    
class GoatGroupScraper(GreenhouseScraper):
    employer_name = 'Goat Group'
    EMPLOYER_KEY = 'goatgroup'
    
    
class NorthAmericanBancardScraper(WorkdayScraper):
    employer_name = 'North American Bancard'
    start_url = 'https://nabancard.wd1.myworkdayjobs.com/nab/'
    has_job_departments = False
    
    
class BeamBenefitsScraper(LeverScraper):
    employer_name = 'Beam Benefits'
    EMPLOYER_KEY = 'beam'
    
    
class CollectiveHealthScraper(GreenhouseIframeScraper):
    employer_name = 'Collective Health'
    EMPLOYER_KEY = 'collectivehealth'
    
    
class ZenBusinessScraper(LeverScraper):
    employer_name = 'ZenBusiness'
    EMPLOYER_KEY = 'zenbusiness'
    

class IntegrityMarketingScraper(WorkdayScraper):
    employer_name = 'Integriy Marketing'
    start_url = 'https://integritymarketing.wd1.myworkdayjobs.com/Integrity/'
    has_job_departments = False
    
    
class BeyondIdentityScraper(GreenhouseIframeScraper):
    employer_name = 'Beyond Identity'
    EMPLOYER_KEY = 'beyondidentity'
    
    
class EnableScraper(LeverScraper):
    employer_name = 'Enable'
    EMPLOYER_KEY = 'enable'
    
    
class DoorDashScraper(GreenhouseIframeScraper):
    employer_name = 'DoorDash'
    EMPLOYER_KEY = 'doordash'
    
    
class SnackpassScraper(GreenhouseScraper):
    employer_name = 'Snackpass'
    EMPLOYER_KEY = 'snackpass'
    
    
class GunterGroupScraper(GreenhouseScraper):
    employer_name = 'The Gunter Group'
    EMPLOYER_KEY = 'guntergroup'
    
    
class BigDConstructionScraper(UltiProScraper):
    # Not working currently
    employer_name = 'Big-D Construction'
    start_url = 'https://recruiting2.ultipro.com/BIG1005BGDC/JobBoard/a1b85713-c4d6-4da4-98fa-9080a291bd18/'
    
    
class CricutScraper(SmartRecruitersScraper):
    employer_name = 'Cricut'
    EMPLOYER_KEY = 'Cricut'
    

class StriderTechnologiesScraper(GreenhouseScraper):
    employer_name = 'Strider Technologies'
    EMPLOYER_KEY = 'stridertechnologies'
    
    
class KodiakCakesScraper(GreenhouseScraper):
    employer_name = 'Kodiak Cakes'
    EMPLOYER_KEY = 'kodiakcakes'
    
    
class SalesRabbitScraper(BreezyScraper):
    employer_name = 'SalesRabbit'
    EMPLOYER_KEY = 'salesrabbit'
    
    
class NerdUnitedScraper(PaylocityScraper):
    employer_name = 'Nerd United'
    start_url = 'https://recruiting.paylocity.com/recruiting/jobs/All/9e9935d0-3f49-4c1b-a11d-8d44bbc026cf/Nerd-United-DAO-LLC'
    
    
class SkullCandyScraper(ApplicantProScraper):
    employer_name = 'Skullcandy'
    EMPLOYER_KEY = 'skullcandy'
    

class FLSmidthScraper(WorkdayScraper):
    employer_name = 'FLSmidth'
    start_url = 'https://flsmidth.wd3.myworkdayjobs.com/FLS_Global/'
    
    
class BobsledScraper(GreenhouseIframeScraper):
    employer_name = 'Bobsled'
    EMPLOYER_KEY = 'bobsledinc'
    
    
class RouteScraper(GreenhouseIframeScraper):
    employer_name = 'Route'
    EMPLOYER_KEY = 'route'
    
    
class WeirScraper(WorkdayScraper):
    employer_name = 'Weir'
    start_url = 'https://weir.wd3.myworkdayjobs.com/Weir_External_Careers'
    job_department_form_data_automation_id = 'Job Family-checkboxgroup'
    
    async def open_job_department_menu(self, page):
        await page.locator('css=button[data-automation-id="more"]').click()
        await page.locator('css=button[data-automation-id="Job Family-expand"]').click()
        await self.wait_for_el(
            page, f'div[data-automation-id="{self.job_department_form_data_automation_id}"] label'
        )
        
        
class MedelyScraper(AshbyHQScraper):
    employer_name = 'Medely'
    EMPLOYER_KEY = 'medely'
    
    
class PearlHealthScraper(GreenhouseScraper):
    employer_name = 'Pearl Health'
    EMPLOYER_KEY = 'pearlhealth'
    
    
class NorthSpyreScraper(GreenhouseScraper):
    employer_name = 'Northspyre'
    EMPLOYER_KEY = 'northspyre'
    
    
class OutdoorsyScraper(WorkableScraper):
    employer_name = 'Outdoorsy'
    EMPLOYER_KEY = 'outdoorsy'
    
    
class MadhiveScraper(GreenhouseScraper):
    employer_name = 'Madhive'
    EMPLOYER_KEY = 'madhive'
    
    
class GlossGeniusScraper(GreenhouseScraper):
    employer_name = 'GlossGenius'
    EMPLOYER_KEY = 'glossgenius'
    
    
class GatherScraper(GreenhouseScraper):
    employer_name = 'Gather'
    EMPLOYER_KEY = 'gather'
    
    
class WaabiScraper(LeverScraper):
    employer_name = 'Waabi'
    EMPLOYER_KEY = 'waabi'
    
    
class MemoraHealthScraper(GreenhouseScraper):
    employer_name = 'Memora Health'
    EMPLOYER_KEY = 'memorahealth'
    
    
class LeafLinkScraper(GreenhouseScraper):
    employer_name = 'LeafLink'
    EMPLOYER_KEY = 'leaflink'
    
    
class RewindScraper(LeverScraper):
    employer_name = 'Rewind'
    EMPLOYER_KEY = 'rewind.ai'
    
    
class HungryrootScraper(GreenhouseScraper):
    employer_name = 'Hungryroot'
    EMPLOYER_KEY = 'hungryroot'
    
    
class PulleyScraper(AshbyHQScraper):
    employer_name = 'Pulley'
    EMPLOYER_KEY = 'Pulley'
    
    
class BoulevardScraper(GreenhouseScraper):
    employer_name = 'Boulevard'
    EMPLOYER_KEY = 'boulevard'
    
    
class PostScraper(AshbyHQScraper):
    employer_name = 'Post'
    EMPLOYER_KEY = 'Post'
    
    
class NautilusLabsScraper(GreenhouseIframeScraper):
    employer_name = 'Nautilus Labs'
    EMPLOYER_KEY = 'nautiluslabs'
    

class DatabookScraper(GreenhouseScraper):
    employer_name = 'Databook'
    EMPLOYER_KEY = 'databook'
    
    
class NexlaScraper(GreenhouseScraper):
    employer_name = 'Nexla'
    EMPLOYER_KEY = 'nexla'
    
    
class PollyScraper(LeverScraper):
    employer_name = 'Polly'
    EMPLOYER_KEY = 'pollyex'
    
    
class AdaScraper(LeverScraper):
    employer_name = 'Ada'
    EMPLOYER_KEY = 'ada'
    
    
class ValimailScraper(GreenhouseScraper):
    employer_name = 'Valimail'
    EMPLOYER_KEY = 'valimailinc'
    
    
class ClimateAiScraper(LeverScraper):
    employer_name = 'ClimateAi'
    EMPLOYER_KEY = 'climateai'
    
    
class KintsugiScraper(GreenhouseScraper):
    employer_name = 'Kintsugi'
    EMPLOYER_KEY = 'kintsugi'
    
    
class CrossBorderSolutionsScraper(GreenhouseScraper):
    employer_name = 'CrossBorder Solutions'
    EMPLOYER_KEY = 'crossbordersolutions'
    
    
class PointScraper(GreenhouseIframeScraper):
    employer_name = 'Point'
    EMPLOYER_KEY = 'pointdigitalfinance'
    
    
class TetraScienceScraper(WorkableScraper):
    employer_name = 'TetraScience'
    EMPLOYER_KEY = 'tetrascience'
    
    
class OutriderScraper(LeverScraper):
    employer_name = 'Outrider'
    EMPLOYER_KEY = 'outrider'
    
    
class ReforgeScraper(GreenhouseScraper):
    employer_name = 'Reforge'
    EMPLOYER_KEY = 'reforge'
    
    
class AtoBScraper(LeverScraper):
    employer_name = 'AtoB'
    EMPLOYER_KEY = 'atob'
    
    
class TrunkScraper(LeverScraper):
    employer_name = 'Trunk'
    EMPLOYER_KEY = 'trunkio'
    
    
class HelmAiScraper(LeverScraper):
    """No longer working. Might have gone out of business"""
    employer_name = 'Helm.ai'
    EMPLOYER_KEY = 'helm'
    
    
class RayaScraper(LeverScraper):
    employer_name = 'Raya'
    EMPLOYER_KEY = 'raya'
    
    
class SquareScraper(SmartRecruitersScraper):
    employer_name = 'Square'
    EMPLOYER_KEY = 'Square'
    
    
class ServiceTitanScraper(WorkdayScraper):
    employer_name = 'ServiceTitan'
    start_url = 'https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan/'
    
    
class GrowTherapyScraper(GreenhouseScraper):
    employer_name = 'Grow Therapy'
    EMPLOYER_KEY = 'growtherapy'
    
    
class GitHubScraper(GreenhouseScraper):
    employer_name = 'GitHub'
    EMPLOYER_KEY = 'github'
    
    
class BintiScraper(GreenhouseScraper):
    employer_name = 'Binti'
    EMPLOYER_KEY = 'binti'
    
    
class WhatnotScraper(GreenhouseScraper):
    employer_name = 'Whatnot'
    EMPLOYER_KEY = 'whatnot'
    
    
class VarsityTutorsScraper(GreenhouseScraper):
    employer_name = 'Varsity Tutors'
    EMPLOYER_KEY = 'varsitytutors'
    

class ServiceNowScraper(SmartRecruitersScraper):
    employer_name = 'ServiceNow'
    EMPLOYER_KEY = 'ServiceNow'
    
    
class AutodeskScraper(WorkdayScraper):
    employer_name = 'Autodesk'
    start_url = 'https://autodesk.wd1.myworkdayjobs.com/en-US/Ext/'
    

class CruiseScraper(GreenhouseIframeScraper):
    employer_name = 'Cruise'
    EMPLOYER_KEY = 'cruise'
    
    
class HelloFreshScraper(GreenhouseIframeScraper):
    employer_name = 'HelloFresh'
    EMPLOYER_KEY = 'hellofresh'
    
    def process_location_text(self, location_text):
        if ';' in location_text:
            return [l.strip() for l in location_text.split(';')]
        elif 'or ' in location_text:
            return [l.strip() for l in location_text.split('or ')]
        elif len(location_text) > 50:
            location_parts = [l.strip() for l in location_text.split(',')]
            locations = []
            location = None
            for idx, location_text_part in enumerate(location_parts):
                if idx % 3 == 0:
                    if location:
                        locations.append(location)
                    location = location_text_part
                else:
                    location += f', {location_text_part}'
            if location not in locations:
                locations.append(location)
            return locations
        else:
            return location_text

    
class OsmindScraper(LeverScraper):
    employer_name = 'Osmind'
    EMPLOYER_KEY = 'Osmind'
    
    
class IncludedHealthScraper(LeverScraper):
    employer_name = 'Included Health'
    EMPLOYER_KEY = 'includedhealth'
    
    
class MotionalScraper(GreenhouseIframeScraper):
    employer_name = 'Motional'
    EMPLOYER_KEY = 'motional'
    
    
class AtticusScraper(GreenhouseScraper):
    employer_name = 'Atticus'
    EMPLOYER_KEY = 'atticus'
    
    
class OnBoardScraper(GreenhouseScraper):
    employer_name = 'OnBoard'
    EMPLOYER_KEY = 'onboardmeetings'
    
    
class RedditScraper(GreenhouseScraper):
    employer_name = 'Reddit'
    EMPLOYER_KEY = 'reddit'
    
    
class ChiefScraper(GreenhouseScraper):
    employer_name = 'Chief'
    EMPLOYER_KEY = 'chief'
    
    
class LocusScraper(SmartRecruitersScraper):
    employer_name = 'Locus Robotics'
    EMPLOYER_KEY = 'LocusRobotics'
    
    
class ArticulateScraper(GreenhouseScraper):
    employer_name = 'Articulate'
    EMPLOYER_KEY = 'articulate'
    
    
class StairwellScraper(GreenhouseScraper):
    employer_name = 'Stairwell'
    EMPLOYER_KEY = 'stairwell'
    
    
class StitchFixScraper(GreenhouseIframeScraper):
    employer_name = 'Stitch Fix'
    EMPLOYER_KEY = 'stitchfix'
    
    
class StordScraper(GreenhouseScraper):
    employer_name = 'Stord'
    EMPLOYER_KEY = 'stord13'
    
    
class DiscordScraper(GreenhouseApiScraper):
    employer_name = 'Discord'
    EMPLOYER_KEY = 'discord'
    
    
class AthleticGreensScraper(WorkableScraper):
    employer_name = 'Athletic Greens'
    EMPLOYER_KEY = 'athletic-greens-hiring'
    

class InstacartScraper(GreenhouseIframeScraper):
    employer_name = 'Instacart'
    EMPLOYER_KEY = 'instacart'
    
    
class StacklokScraper(GreenhouseIframeScraper):
    employer_name = 'Stacklok'
    EMPLOYER_KEY = 'stacklok'
    
    
class PulumiScraper(GreenhouseScraper):
    employer_name = 'Pulumi'
    EMPLOYER_KEY = 'pulumicorporation'
    
    
class SmartAssetScraper(GreenhouseScraper):
    employer_name = 'SmartAsset'
    EMPLOYER_KEY = 'smartasset'
    
    
class InstabaseScraper(GreenhouseIframeScraper):
    employer_name = 'Instabase'
    EMPLOYER_KEY = 'instabase'
    
    
class BioRenderScraper(LeverScraper):
    employer_name = 'BioRender'
    EMPLOYER_KEY = 'biorender'
    
    
class StellarCyberScraper(WorkableScraper):
    employer_name = 'Stellar Cyber'
    EMPLOYER_KEY = 'stellar-cyber'
    
    
class StellarHealthScraper(GreenhouseScraper):
    employer_name = 'Stellar Health'
    EMPLOYER_KEY = 'stellarhealth'
    

class SixSenseScraper(GreenhouseIframeScraper):
    employer_name = '6sense'
    EMPLOYER_KEY = '6sense'
    
    
class BillionToOneScraper(GreenhouseScraper):
    employer_name = 'BillionToOne'
    EMPLOYER_KEY = 'billiontoone'
    
    
class NunaScraper(GreenhouseScraper):
    employer_name = 'Nuna'
    EMPLOYER_KEY = 'nuna'
    
    
class UpstartScraper(GreenhouseIframeScraper):
    employer_name = 'Upstart'
    EMPLOYER_KEY = 'upstart'
    
    
class EtsyScraper(SmartRecruitersScraper):
    employer_name = 'Etsy'
    EMPLOYER_KEY = 'Etsy2'
    
    
class EasyPostScraper(LeverScraper):
    employer_name = 'EasyPost'
    EMPLOYER_KEY = 'easypost-2'
    
    
class CabifyScraper(GreenhouseScraper):
    employer_name = 'Cabify'
    EMPLOYER_KEY = 'cabify'
    
    
class UpsideScraper(GreenhouseIframeScraper):
    employer_name = 'Upside'
    EMPLOYER_KEY = 'ericbuckleygetupsidegreenhouseio'
    
    
class AutomoxScraper(LeverScraper):
    employer_name = 'Automox'
    EMPLOYER_KEY = 'automox'
    
    
class ProcoreTechnologiesScraper(SmartRecruitersScraper):
    employer_name = 'Procore Technologies'
    EMPLOYER_KEY = 'ProcoreTechnologies'
    
    
class SmartsheetScraper(GreenhouseScraper):
    employer_name = 'Smartsheet'
    EMPLOYER_KEY = 'smartsheet'
    
    
class DivvyHomesScraper(GreenhouseScraper):
    employer_name = 'Divvy Homes'
    EMPLOYER_KEY = 'divvyhomes'
    

class ManticoreGamesScraper(GreenhouseApiScraper):
    employer_name = 'Manticore Games'
    EMPLOYER_KEY = 'manticoregames'
    
    
class GustoScraper(GreenhouseScraper):
    employer_name = 'Gusto'
    EMPLOYER_KEY = 'gusto'
    
    
class MoovScraper(GreenhouseScraper):
    employer_name = 'Moov'
    EMPLOYER_KEY = 'moovfinancial'
    
    
class ExponentialScraper(AshbyHQScraper):
    employer_name = 'Exponential'
    EMPLOYER_KEY = 'exponential'
    
    
class SproutSocialScraper(GreenhouseApiScraper):
    employer_name = 'Sprout Social'
    EMPLOYER_KEY = 'sproutsocial'
    
    
class VestwellScraper(GreenhouseIframeScraper):
    employer_name = 'Vestwell'
    EMPLOYER_KEY = 'vestwell'
    
    
class HandshakeScraper(GreenhouseIframeScraper):
    employer_name = 'Handshake'
    EMPLOYER_KEY = 'joinhandshake'
    
    
class InovalonScraper(GreenhouseApiScraper):
    employer_name = 'Inovalon'
    EMPLOYER_KEY = 'inovalon'
    
    
class AltruistScraper(GreenhouseIframeScraper):
    employer_name = 'Altruist'
    EMPLOYER_KEY = 'altruist'
    
    
class AffinityScraper(GreenhouseIframeScraper):
    employer_name = 'Affinity'
    EMPLOYER_KEY = 'affinity'
    
    
class EquipmentShareScraper(GreenhouseIframeScraper):
    employer_name = 'EquipmentShare'
    EMPLOYER_KEY = 'equipmentsharecom'
    
    
class AirbnbScraper(GreenhouseIframeScraper):
    employer_name = 'Airbnb'
    EMPLOYER_KEY = 'airbnb'
    
    def process_location_text(self, location_text):
        return 'Remote'
    
    
class IterativeScraper(LeverScraper):
    employer_name = 'iterative.ai'
    EMPLOYER_KEY = 'iterative'
    
    
class IoGlobalScraper(WorkableScraper):
    employer_name = 'IO Global'
    EMPLOYER_KEY = 'io-global'


class CadreScraper(GreenhouseScraper):
    employer_name = 'Cadre'
    EMPLOYER_KEY = 'cadre'
    
    
class PangeaScraper(GreenhouseScraper):
    employer_name = 'Pangea'
    EMPLOYER_KEY = 'pangea'
    
    
class BrightflowAIScraper(GreenhouseScraper):
    employer_name = 'Brightflow AI'
    EMPLOYER_KEY = 'brightflowai'
    
    
class EvolveScraper(GreenhouseScraper):
    employer_name = 'Evolve'
    EMPLOYER_KEY = 'evolvevacationrental'
    
    
class PostscriptScraper(GreenhouseScraper):
    employer_name = 'Postscript'
    EMPLOYER_KEY = 'postscript'
    
    
class GroqScraper(GreenhouseIframeScraper):
    employer_name = 'Groq'
    EMPLOYER_KEY = 'groq'
    
    
class DbtLabsScraper(GreenhouseScraper):
    employer_name = 'dbt Labs'
    EMPLOYER_KEY = 'dbtlabsinc'
    
    
class VeryGoodSecurityScraper(GreenhouseScraper):
    employer_name = 'Very Good Security'
    EMPLOYER_KEY = 'verygoodsecurity'
    
    
class CloseScraper(LeverScraper):
    employer_name = 'Close'
    EMPLOYER_KEY = 'close.io'
    
    
class CodeOrgScraper(GreenhouseScraper):
    employer_name = 'Code.org'
    EMPLOYER_KEY = 'codeorg'
    
    
class PluralsightScraper(WorkdayScraper):
    employer_name = 'Pluralsight'
    start_url = 'https://pluralsight.wd1.myworkdayjobs.com/en-US/Careers/'
    # Not all departments are categorized so we don't want to miss any
    has_job_departments = False
    # job_department_menu_data_automation_id = 'jobCategory'
    # job_department_form_data_automation_id = 'jobCategoryCheckboxGroup'
    
    
class IseeScraper(LeverScraper):
    employer_name = 'ISEE'
    EMPLOYER_KEY = 'isee'
    
    
class MediaMathScraper(GreenhouseApiScraper):
    employer_name = 'MediaMath'
    EMPLOYER_KEY = 'mediamath'
    
    
class QadScraper(SmartRecruitersScraper):
    employer_name = 'QAD'
    EMPLOYER_KEY = 'QADInc'
    
    
class FigmaScraper(GreenhouseScraper):
    employer_name = 'Figma'
    EMPLOYER_KEY = 'figma'
    
    
class LatchScraper(GreenhouseApiScraper):
    employer_name = 'Latch'
    EMPLOYER_KEY = 'LATCH'
    
    
class SuperhumanScraper(GreenhouseIframeScraper):
    employer_name = 'Superhuman'
    EMPLOYER_KEY = 'superhuman'


class ZillowScraper(WorkdayScraper):
    employer_name = 'Zillow'
    start_url = 'https://zillow.wd5.myworkdayjobs.com/en-US/Zillow_Group_External/'
    has_job_departments = False
    
    
class ApolloScraper(GreenhouseScraper):
    employer_name = 'Apollo.io'
    EMPLOYER_KEY = 'apolloio'
    
    
class ThumbtackScraper(GreenhouseScraper):
    employer_name = 'Thumbtack'
    EMPLOYER_KEY = 'thumbtack'
    
    
class SolvScraper(LeverScraper):
    employer_name = 'Solv'
    EMPLOYER_KEY = 'solvhealth'
    
    
class VehoScraper(LeverScraper):
    employer_name = 'Veho'
    EMPLOYER_KEY = 'veho'
    
    
class QuizletScraper(LeverScraper):
    employer_name = 'Quizlet'
    EMPLOYER_KEY = 'quizlet-2'
    
    
class EndorLabsScraper(GreenhouseScraper):
    employer_name = 'Endor Labs'
    EMPLOYER_KEY = 'endorlabs'
    

class WarblerLabsScraper(LeverScraper):
    employer_name = 'Warbler Labs'
    EMPLOYER_KEY = 'WarblerLabs'
    
    
class Epsilon3Scraper(LeverScraper):
    employer_name = 'Epsilon3'
    EMPLOYER_KEY = 'epsilon3'
    
    
class BlockchainsScraper(GreenhouseIframeScraper):
    employer_name = 'Blockchains'
    EMPLOYER_KEY = 'blockchainsmanagementinc'
    
    
class CollibraScraper(GreenhouseApiScraper):
    employer_name = 'Collibra'
    EMPLOYER_KEY = 'collibra'
    
    
class QuotientScraper(LeverScraper):
    employer_name = 'Quotient'
    EMPLOYER_KEY = 'quotient'
    
    
class FoundScraper(GreenhouseScraper):
    employer_name = 'Found'
    EMPLOYER_KEY = 'found'
    
    
class Shift5Scraper(GreenhouseScraper):
    employer_name = 'Shift5'
    EMPLOYER_KEY = 'shift5'
    
    
class GrindrScraper(GreenhouseScraper):
    employer_name = 'Grindr'
    EMPLOYER_KEY = 'grindr'

 
class ZuoraScraper(GreenhouseApiScraper):
    employer_name = 'Zuora'
    EMPLOYER_KEY = 'zuora'
    
    
class Restaurant365Scraper(LeverScraper):
    employer_name = 'Restaurant365'
    EMPLOYER_KEY = 'restaurant365'
    
    
class WeightsAndBiasesScraper(LeverScraper):
    employer_name = 'Weights & Biases'
    EMPLOYER_KEY = 'wandb'
    
    
class CloudflareScraper(GreenhouseApiScraper):
    employer_name = 'Cloudflare'
    EMPLOYER_KEY = 'cloudflare'
    
    
class MapboxScraper(GreenhouseApiScraper):
    employer_name = 'Mapbox'
    EMPLOYER_KEY = 'mapbox'
    
    
class PindropScraper(GreenhouseIframeScraper):
    employer_name = 'Pindrop'
    EMPLOYER_KEY = 'pindropsecurity'
    

class CanonicalScraper(GreenhouseScraper):
    employer_name = 'Canonical'
    EMPLOYER_KEY = 'canonical'
    
    
class RampScraper(GreenhouseScraper):
    employer_name = 'Ramp'
    EMPLOYER_KEY = 'ramp'
    
    
class ImplyScraper(GreenhouseIframeScraper):
    employer_name = 'Imply'
    EMPLOYER_KEY = 'imply'
    
    
class MavenScraper(GreenhouseScraper):
    employer_name = 'Maven'
    EMPLOYER_KEY = 'mavenclinic'
    
    
class PhantomScraper(GreenhouseApiScraper):
    employer_name = 'Phantom'
    EMPLOYER_KEY = 'phantom45'
    
    
class CriblScraper(GreenhouseIframeScraper):
    employer_name = 'Cribl'
    EMPLOYER_KEY = 'cribl'
    
    
class PaxosScraper(GreenhouseApiScraper):
    employer_name = 'Paxos'
    EMPLOYER_KEY = 'joinpaxos'
    
    
class QualcommScraper(WorkdayScraper):
    employer_name = 'Qualcomm'
    start_url = 'https://qualcomm.wd5.myworkdayjobs.com/en-US/External/'
    
    
class ModernHealthScraper(GreenhouseScraper):
    employer_name = 'Modern Health'
    EMPLOYER_KEY = 'modernhealth'
    
    
class FastlyScraper(GreenhouseIframeScraper):
    employer_name = 'Fastly'
    EMPLOYER_KEY = 'fastly'
    
    
class PinterestScraper(GreenhouseIframeScraper):
    employer_name = 'Pinterest'
    EMPLOYER_KEY = 'pinterest'
    
    
class CoinbaseScraper(GreenhouseApiScraper):
    employer_name = 'Coinbase'
    EMPLOYER_KEY = 'coinbase'
    
    
class RobinhoodScraper(GreenhouseIframeScraper):
    employer_name = 'Robinhood'
    EMPLOYER_KEY = 'robinhood'
    
    
class OnfidoScraper(LeverScraper):
    employer_name = 'Onfido'
    EMPLOYER_KEY = 'onfido'
    

class JamCityScraper(LeverScraper):
    employer_name = 'Jam City'
    EMPLOYER_KEY = 'jamcity'
    

# TODO: Build a new scraper for PhenomPeople ats
# class AdobeScraper():
#     employer_name = 'Adobe'
#     start_url = 'https://careers.adobe.com/us/en/c/'

# EbayScraper.employer_name: EbayScraper,
test_scrapers = {
}


all_scrapers = {
    JamCityScraper.employer_name: JamCityScraper,
    OnfidoScraper.employer_name: OnfidoScraper,
    RobinhoodScraper.employer_name: RobinhoodScraper,
    CoinbaseScraper.employer_name: CoinbaseScraper,
    PinterestScraper.employer_name: PinterestScraper,
    InovalonScraper.employer_name: InovalonScraper,
    SproutSocialScraper.employer_name: SproutSocialScraper,
    ManticoreGamesScraper.employer_name: ManticoreGamesScraper,
    CollibraScraper.employer_name: CollibraScraper,
    LatchScraper.employer_name: LatchScraper,
    MediaMathScraper.employer_name: MediaMathScraper,
    ZuoraScraper.employer_name: ZuoraScraper,
    CloudflareScraper.employer_name: CloudflareScraper,
    MapboxScraper.employer_name: MapboxScraper,
    PhantomScraper.employer_name: PhantomScraper,
    PaxosScraper.employer_name: PaxosScraper,
    FastlyScraper.employer_name: FastlyScraper,
    ModernHealthScraper.employer_name: ModernHealthScraper,
    QualcommScraper.employer_name: QualcommScraper,
    CriblScraper.employer_name: CriblScraper,
    MavenScraper.employer_name: MavenScraper,
    ImplyScraper.employer_name: ImplyScraper,
    RampScraper.employer_name: RampScraper,
    CanonicalScraper.employer_name: CanonicalScraper,
    FanaticsScraper.employer_name: FanaticsScraper,
    PindropScraper.employer_name: PindropScraper,
    WeightsAndBiasesScraper.employer_name: WeightsAndBiasesScraper,
    Restaurant365Scraper.employer_name: Restaurant365Scraper,
    GrindrScraper.employer_name: GrindrScraper,
    Shift5Scraper.employer_name: Shift5Scraper,
    FoundScraper.employer_name: FoundScraper,
    QuotientScraper.employer_name: QuotientScraper,
    BlockchainsScraper.employer_name: BlockchainsScraper,
    Epsilon3Scraper.employer_name: Epsilon3Scraper,
    WarblerLabsScraper.employer_name: WarblerLabsScraper,
    EndorLabsScraper.employer_name: EndorLabsScraper,
    QuizletScraper.employer_name: QuizletScraper,
    VehoScraper.employer_name: VehoScraper,
    SolvScraper.employer_name: SolvScraper,
    ThumbtackScraper.employer_name: ThumbtackScraper,
    ApolloScraper.employer_name: ApolloScraper,
    ZillowScraper.employer_name: ZillowScraper,
    SuperhumanScraper.employer_name: SuperhumanScraper,
    FigmaScraper.employer_name: FigmaScraper,
    QadScraper.employer_name: QadScraper,
    IseeScraper.employer_name: IseeScraper,
    IoGlobalScraper.employer_name: IoGlobalScraper,
    AirbnbScraper.employer_name: AirbnbScraper,
    PluralsightScraper.employer_name: PluralsightScraper,
    MedelyScraper.employer_name: MedelyScraper,
    EquipmentShareScraper.employer_name: EquipmentShareScraper,
    AffinityScraper.employer_name: AffinityScraper,
    AltruistScraper.employer_name: AltruistScraper,
    HandshakeScraper.employer_name: HandshakeScraper,
    VestwellScraper.employer_name: VestwellScraper,
    ExponentialScraper.employer_name: ExponentialScraper,
    MoovScraper.employer_name: MoovScraper,
    GustoScraper.employer_name: GustoScraper,
    DivvyHomesScraper.employer_name: DivvyHomesScraper,
    SmartsheetScraper.employer_name: SmartsheetScraper,
    ProcoreTechnologiesScraper.employer_name: ProcoreTechnologiesScraper,
    AutomoxScraper.employer_name: AutomoxScraper,
    IterativeScraper.employer_name: IterativeScraper,
    CodeOrgScraper.employer_name: CodeOrgScraper,
    CloseScraper.employer_name: CloseScraper,
    VeryGoodSecurityScraper.employer_name: VeryGoodSecurityScraper,
    DbtLabsScraper.employer_name: DbtLabsScraper,
    GroqScraper.employer_name: GroqScraper,
    PostscriptScraper.employer_name: PostscriptScraper,
    EvolveScraper.employer_name: EvolveScraper,
    BrightflowAIScraper.employer_name: BrightflowAIScraper,
    PangeaScraper.employer_name: PangeaScraper,
    CadreScraper.employer_name: CadreScraper,
    HelloFreshScraper.employer_name: HelloFreshScraper,
    DiscordScraper.employer_name: DiscordScraper,
    SixSenseScraper.employer_name: SixSenseScraper,
    BillionToOneScraper.employer_name: BillionToOneScraper,
    NunaScraper.employer_name: NunaScraper,
    UpstartScraper.employer_name: UpstartScraper,
    EtsyScraper.employer_name: EtsyScraper,
    EasyPostScraper.employer_name: EasyPostScraper,
    CabifyScraper.employer_name: CabifyScraper,
    UpsideScraper.employer_name: UpsideScraper,
    AthleticGreensScraper.employer_name: AthleticGreensScraper,
    InstacartScraper.employer_name: InstacartScraper,
    StacklokScraper.employer_name: StacklokScraper,
    PulumiScraper.employer_name: PulumiScraper,
    SmartAssetScraper.employer_name: SmartAssetScraper,
    InstabaseScraper.employer_name: InstabaseScraper,
    BioRenderScraper.employer_name: BioRenderScraper,
    StellarCyberScraper.employer_name: StellarCyberScraper,
    StellarHealthScraper.employer_name: StellarHealthScraper,
    MotionalScraper.employer_name: MotionalScraper,
    AtticusScraper.employer_name: AtticusScraper,
    OnBoardScraper.employer_name: OnBoardScraper,
    RedditScraper.employer_name: RedditScraper,
    ChiefScraper.employer_name: ChiefScraper,
    LocusScraper.employer_name: LocusScraper,
    ArticulateScraper.employer_name: ArticulateScraper,
    StairwellScraper.employer_name: StairwellScraper,
    StitchFixScraper.employer_name: StitchFixScraper,
    StordScraper.employer_name: StordScraper,
    VarsityTutorsScraper.employer_name: VarsityTutorsScraper,
    ServiceNowScraper.employer_name: ServiceNowScraper,
    AutodeskScraper.employer_name: AutodeskScraper,
    CruiseScraper.employer_name: CruiseScraper,
    OsmindScraper.employer_name: OsmindScraper,
    IncludedHealthScraper.employer_name: IncludedHealthScraper,
    ClimateAiScraper.employer_name: ClimateAiScraper,
    TetraScienceScraper.employer_name: TetraScienceScraper,
    OutdoorsyScraper.employer_name: OutdoorsyScraper,
    NautilusLabsScraper.employer_name: NautilusLabsScraper,
    ServiceTitanScraper.employer_name: ServiceTitanScraper,
    GrowTherapyScraper.employer_name: GrowTherapyScraper,
    GitHubScraper.employer_name: GitHubScraper,
    BintiScraper.employer_name: BintiScraper,
    WhatnotScraper.employer_name: WhatnotScraper,
    OutriderScraper.employer_name: OutriderScraper,
    ReforgeScraper.employer_name: ReforgeScraper,
    AtoBScraper.employer_name: AtoBScraper,
    TrunkScraper.employer_name: TrunkScraper,
    # HelmAiScraper.employer_name: HelmAiScraper,
    RayaScraper.employer_name: RayaScraper,
    SquareScraper.employer_name: SquareScraper,
    KintsugiScraper.employer_name: KintsugiScraper,
    CrossBorderSolutionsScraper.employer_name: CrossBorderSolutionsScraper,
    PointScraper.employer_name: PointScraper,
    DatabookScraper.employer_name: DatabookScraper,
    NexlaScraper.employer_name: NexlaScraper,
    PollyScraper.employer_name: PollyScraper,
    AdaScraper.employer_name: AdaScraper,
    ValimailScraper.employer_name: ValimailScraper,
    MadhiveScraper.employer_name: MadhiveScraper,
    GlossGeniusScraper.employer_name: GlossGeniusScraper,
    GatherScraper.employer_name: GatherScraper,
    WaabiScraper.employer_name: WaabiScraper,
    MemoraHealthScraper.employer_name: MemoraHealthScraper,
    LeafLinkScraper.employer_name: LeafLinkScraper,
    RewindScraper.employer_name: RewindScraper,
    HungryrootScraper.employer_name: HungryrootScraper,
    PulleyScraper.employer_name: PulleyScraper,
    BoulevardScraper.employer_name: BoulevardScraper,
    PostScraper.employer_name: PostScraper,
    PearlHealthScraper.employer_name: PearlHealthScraper,
    NorthSpyreScraper.employer_name: NorthSpyreScraper,
    WeirScraper.employer_name: WeirScraper,
    RouteScraper.employer_name: RouteScraper,
    BobsledScraper.employer_name: BobsledScraper,
    FLSmidthScraper.employer_name: FLSmidthScraper,
    SkullCandyScraper.employer_name: SkullCandyScraper,
    NerdUnitedScraper.employer_name: NerdUnitedScraper,
    StriderTechnologiesScraper.employer_name: StriderTechnologiesScraper,
    KodiakCakesScraper.employer_name: KodiakCakesScraper,
    SalesRabbitScraper.employer_name: SalesRabbitScraper,
    CricutScraper.employer_name: CricutScraper,
    # BigDConstructionScraper.employer_name: BigDConstructionScraper,
    GunterGroupScraper.employer_name: GunterGroupScraper,
    BlueOriginScraper.employer_name: BlueOriginScraper,
    DoorDashScraper.employer_name: DoorDashScraper,
    BeyondIdentityScraper.employer_name: BeyondIdentityScraper,
    IntegrityMarketingScraper.employer_name: IntegrityMarketingScraper,
    NorthAmericanBancardScraper.employer_name: NorthAmericanBancardScraper,
    SnackpassScraper.employer_name: SnackpassScraper,
    EnableScraper.employer_name: EnableScraper,
    BeamBenefitsScraper.employer_name: BeamBenefitsScraper,
    CollectiveHealthScraper.employer_name: CollectiveHealthScraper,
    ZenBusinessScraper.employer_name: ZenBusinessScraper,
    GoatGroupScraper.employer_name: GoatGroupScraper,
    PacksizeScraper.employer_name: PacksizeScraper,
    One800ContactsScraper.employer_name: One800ContactsScraper,
    AncestryScraper.employer_name: AncestryScraper,
    WeaveHQScraper.employer_name: WeaveHQScraper,
    RoktScraper.employer_name: RoktScraper,
    OmadaHealthScraper.employer_name: OmadaHealthScraper,
    AccessoScraper.employer_name: AccessoScraper,
    AddeparScraper.employer_name: AddeparScraper,
    AffirmScraper.employer_name: AffirmScraper,
    AngiScraper.employer_name: AngiScraper,
    AnthropicScraper.employer_name: AnthropicScraper,
    AtlassianScraper.employer_name: AtlassianScraper,
    AtomicScraper.employer_name: AtomicScraper,
    AttentiveScraper.employer_name: AttentiveScraper,
    AvettaScraper.employer_name: AvettaScraper,
    BenevityScraper.employer_name: BenevityScraper,
    BrightwheelScraper.employer_name: BrightwheelScraper,
    CambiaHealthSolutionsScraper.employer_name: CambiaHealthSolutionsScraper,
    CHGHealthcareScraper.employer_name: CHGHealthcareScraper,
    CircleScraper.employer_name: CircleScraper,
    ClozdScraper.employer_name: ClozdScraper,
    ClipboardHealthScraper.employer_name: ClipboardHealthScraper,
    ConsensusScraper.employer_name: ConsensusScraper,
    CopilotIQScraper.employer_name: CopilotIQScraper,
    CuldesacScraper.employer_name: CuldesacScraper,
    DevotedHealthScraper.employer_name: DevotedHealthScraper,
    ElsevierScraper.employer_name: ElsevierScraper,
    EntrataScraper.employer_name: EntrataScraper,
    EverCommerceScraper.employer_name: EverCommerceScraper,
    FabricScraper.employer_name: FabricScraper,
    FICOScraper.employer_name: FICOScraper,
    ForwardScraper.employer_name: ForwardScraper,
    FoursquareScraper.employer_name: FoursquareScraper,
    GalileoScraper.employer_name: GalileoScraper,
    GrayDigitalScraper.employer_name: GrayDigitalScraper,
    GuildEducationScraper.employer_name: GuildEducationScraper,
    HealthGorillaScraper.employer_name: HealthGorillaScraper,
    HopperScraper.employer_name: HopperScraper,
    InvenergyScraper.employer_name: InvenergyScraper,
    KandjiScraper.employer_name: KandjiScraper,
    KlarnaScraper.employer_name: KlarnaScraper,
    KoalaHealthScraper.employer_name: KoalaHealthScraper,
    LaticreteInternationalScraper.employer_name: LaticreteInternationalScraper,
    LeanDataScraper.employer_name: LeanDataScraper,
    LinktreeScraper.employer_name: LinktreeScraper,
    LiveViewTechnologiesScraper.employer_name: LiveViewTechnologiesScraper,
    LoopScraper.employer_name: LoopScraper,
    LoopReturnsScraper.employer_name: LoopReturnsScraper,
    LucidSoftwareScraper.employer_name: LucidSoftwareScraper,
    Mach49Scraper.employer_name: Mach49Scraper,
    MaterialSecurityScraper.employer_name: MaterialSecurityScraper,
    MetabaseScraper.employer_name: MetabaseScraper,
    MetronomeScraper.employer_name: MetronomeScraper,
    MindbloomScraper.employer_name: MindbloomScraper,
    NacelleScraper.employer_name: NacelleScraper,
    NavaScraper.employer_name: NavaScraper,
    NiceScraper.employer_name: NiceScraper,
    NylasScraper.employer_name: NylasScraper,
    PerpayScraper.employer_name: PerpayScraper,
    PlusgradeScraper.employer_name: PlusgradeScraper,
    ProofpointScraper.employer_name: ProofpointScraper,
    RecursionScraper.employer_name: RecursionScraper,
    RegrowScraper.employer_name: RegrowScraper,
    RoScraper.employer_name: RoScraper,
    SeedHealthScraper.employer_name: SeedHealthScraper,
    SentiLinkScraper.employer_name: SentiLinkScraper,
    SideScraper.employer_name: SideScraper,
    StashScraper.employer_name: StashScraper,
    StubHubScraper.employer_name: StubHubScraper,
    TechcyteScraper.employer_name: TechcyteScraper,
    TendoScraper.employer_name: TendoScraper,
    TheMxGroupScraper.employer_name: TheMxGroupScraper,
    TixrScraper.employer_name: TixrScraper,
    TransactionNetworkServicesScraper.employer_name: TransactionNetworkServicesScraper,
    TwoULaundryScraper.employer_name: TwoULaundryScraper,
    UnderdogFantasyScraper.employer_name: UnderdogFantasyScraper,
    VasionScraper.employer_name: VasionScraper,
    VeevaScraper.employer_name: VeevaScraper,
    VerkadaScraper.employer_name: VerkadaScraper,
    VestaTechScraper.employer_name: VestaTechScraper,
    VirtaHealthScraper.employer_name: VirtaHealthScraper,
    VivianHealthScraper.employer_name: VivianHealthScraper,
    VivintScraper.employer_name: VivintScraper,
    WaymarkScraper.employer_name: WaymarkScraper,
    WaystarScraper.employer_name: WaystarScraper,
    WealthsimpleScraper.employer_name: WealthsimpleScraper,
    WhoopScraper.employer_name: WhoopScraper,
    YoungLivingEssentialOilsScraper.employer_name: YoungLivingEssentialOilsScraper,
    ZelisScraper.employer_name: ZelisScraper,
    ZocdocScraper.employer_name: ZocdocScraper
}
