import re

from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from scrape.base_scrapers import ApplicantProScraper, AshbyHQScraper, BambooHrScraper, BreezyScraper, \
    GreenhouseIframeScraper, \
    GreenhouseScraper, \
    LeverScraper, \
    PaylocityScraper, SmartRecruitersScraper, StandardJsScraper, StandardScraper, UltiProScraper, WorkableScraper, \
    WorkdayScraper
from scrape.custom_scraper.ancestry import AncestryScraper
from scrape.custom_scraper.coinbase import CoinbaseScraper
from scrape.custom_scraper.ebay import EbayScraper
from scrape.custom_scraper.packsize import PacksizeScraper
from scrape.custom_scraper.pinterest import PinterestScraper


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
    job_department_data_automation_id = 'jobFamily'
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
    job_department_data_automation_id = 'Department / Area-expand'
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
    
    
class ZocdocScraper(GreenhouseIframeScraper):
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
    job_department_data_automation_id = 'Job_Category'
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
    
    
class OsmindScraper(LeverScraper):
    employer_name = 'Osmind'
    EMPLOYER_KEY = 'Osmind'
    
    
class IncludedHealthScraper(LeverScraper):
    employer_name = 'Included Health'
    EMPLOYER_KEY = 'includedhealth'
    

# TODO: Build a new scraper for PhenomPeople ats
# class AdobeScraper():
#     employer_name = 'Adobe'
#     start_url = 'https://careers.adobe.com/us/en/c/'

# EbayScraper.employer_name: EbayScraper,
# PinterestScraper.employer_name: PinterestScraper,
# CoinbaseScraper.employer_name: CoinbaseScraper
test_scrapers = {
    # HelloFreshScraper.employer_name: HelloFreshScraper,
}


all_scrapers = {
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
    HelmAiScraper.employer_name: HelmAiScraper,
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
    MedelyScraper.employer_name: MedelyScraper,
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
    BigDConstructionScraper.employer_name: BigDConstructionScraper,
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
