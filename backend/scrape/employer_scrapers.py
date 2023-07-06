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
    

class ArteraScraper(LeverScraper):
    employer_name = 'Artera'
    EMPLOYER_KEY = 'artera'


class DeepwatchScraper(GreenhouseApiScraper):
    employer_name = 'Deepwatch'
    EMPLOYER_KEY = 'deepwatchinc'


class Singularity6Scraper(GreenhouseApiScraper):
    employer_name = 'Singularity 6'
    EMPLOYER_KEY = 'singularity6'


class CrestaScraper(LeverScraper):
    employer_name = 'Cresta'
    EMPLOYER_KEY = 'cresta'


class VMwareScraper(WorkdayScraper):
    has_job_departments = False
    employer_name = 'VMware'
    start_url = 'https://vmware.wd1.myworkdayjobs.com/en-US/VMware/'


class NuveiScraper(WorkableScraper):
    employer_name = 'Nuvei'
    EMPLOYER_KEY = 'nuvei'


class OpentableScraper(GreenhouseScraper):
    employer_name = 'OpenTable'
    EMPLOYER_KEY = 'opentable'


class MongodbScraper(GreenhouseApiScraper):
    employer_name = 'MongoDB'
    EMPLOYER_KEY = 'mongodb'


class SkimsScraper(LeverScraper):
    employer_name = 'Skims'
    EMPLOYER_KEY = 'SKIMS'


class TuringScraper(GreenhouseScraper):
    employer_name = 'Turing'
    EMPLOYER_KEY = 'turing'


class RemoteScraper(GreenhouseScraper):
    employer_name = 'Remote'
    EMPLOYER_KEY = 'remotecom'


class TreasureDataScraper(GreenhouseApiScraper):
    employer_name = 'Treasure Data'
    EMPLOYER_KEY = 'treasuredata'


class AlphasenseScraper(GreenhouseScraper):
    employer_name = 'AlphaSense'
    EMPLOYER_KEY = 'alphasense'


class KHealthScraper(GreenhouseScraper):
    employer_name = 'K Health'
    EMPLOYER_KEY = 'khealth'


class RelativitySpaceScraper(GreenhouseApiScraper):
    employer_name = 'Relativity Space'
    EMPLOYER_KEY = 'relativity'


class CoalitionScraper(GreenhouseScraper):
    employer_name = 'Coalition'
    EMPLOYER_KEY = 'coalition'


class ParloaScraper(GreenhouseApiScraper):
    employer_name = 'Parloa'
    EMPLOYER_KEY = 'parloa'


class FiskerScraper(WorkdayScraper):
    employer_name = 'Fisker'
    start_url = 'https://fisker.wd1.myworkdayjobs.com/en-US/Fisker_Careers/'
    has_job_departments = False


class CheckrScraper(GreenhouseScraper):
    employer_name = 'Checkr'
    EMPLOYER_KEY = 'checkr'


class PayuScraper(LeverScraper):
    employer_name = 'PayU'
    EMPLOYER_KEY = 'payu'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class WorkdayCoScraper(WorkdayScraper):
    employer_name = 'Workday'
    start_url = 'https://workday.wd5.myworkdayjobs.com/en-US/Workday/'
    has_job_departments = False


class OktaScraper(GreenhouseApiScraper):
    employer_name = 'Okta'
    EMPLOYER_KEY = 'okta'


class FlexportScraper(GreenhouseScraper):
    employer_name = 'Flexport'
    EMPLOYER_KEY = 'flexport'


class FlatironHealthScraper(GreenhouseApiScraper):
    employer_name = 'Flatiron Health'
    EMPLOYER_KEY = 'flatironhealth'


class DynatraceScraper(SmartRecruitersScraper):
    employer_name = 'Dynatrace'
    EMPLOYER_KEY = 'Dynatrace1'


class OkxScraper(GreenhouseScraper):
    employer_name = 'OKX'
    EMPLOYER_KEY = 'okx'


class AbnormalSecurityScraper(GreenhouseApiScraper):
    employer_name = 'Abnormal Security'
    EMPLOYER_KEY = 'abnormalsecurity'


class BetterupScraper(GreenhouseScraper):
    employer_name = 'BetterUp'
    EMPLOYER_KEY = 'betterup'


class GlovoScraper(GreenhouseApiScraper):
    employer_name = 'Glovo'
    EMPLOYER_KEY = 'glovo'


class AkiliScraper(GreenhouseApiScraper):
    employer_name = 'Akili'
    EMPLOYER_KEY = 'akiliinteractive'


class LastminuteScraper(SmartRecruitersScraper):
    employer_name = 'lastminute.com'
    EMPLOYER_KEY = 'lastminutecom'


class NvidiaScraper(WorkdayScraper):
    employer_name = 'NVIDIA'
    start_url = 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/'
    has_job_departments = False


class HpScraper(WorkdayScraper):
    employer_name = 'HP'
    start_url = 'https://hp.wd5.myworkdayjobs.com/en-US/ExternalCareerSite/'
    has_job_departments = False


class HpeScraper(WorkdayScraper):
    employer_name = 'HPE'
    start_url = 'https://hpe.wd5.myworkdayjobs.com/en-US/Jobsathpe/'
    has_job_departments = False


class DoubleverifyScraper(GreenhouseScraper):
    employer_name = 'DoubleVerify'
    EMPLOYER_KEY = 'doubleverify'


class AspireScraper(GreenhouseScraper):
    employer_name = 'Aspire'
    EMPLOYER_KEY = 'aspire'


class FiscalnoteScraper(LeverScraper):
    employer_name = 'FiscalNote'
    EMPLOYER_KEY = 'fiscalnote'


class NextInsuranceScraper(GreenhouseApiScraper):
    employer_name = 'Next Insurance'
    EMPLOYER_KEY = 'nextinsurance66'


class RoivantScraper(GreenhouseScraper):
    employer_name = 'Roivant'
    EMPLOYER_KEY = 'roivantsciences'


class ModulrScraper(GreenhouseApiScraper):
    employer_name = 'Modulr'
    EMPLOYER_KEY = 'modulrfinance'


class WilsonSonsiniScraper(WorkdayScraper):
    employer_name = 'Wilson Sonsini'
    start_url = 'https://wsgr.wd1.myworkdayjobs.com/en-US/WSGR/'
    has_job_departments = False


class StripeScraper(GreenhouseApiScraper):
    employer_name = 'Stripe'
    EMPLOYER_KEY = 'stripe'


class HudsonRiverTradingScraper(GreenhouseApiScraper):
    employer_name = 'Hudson River Trading'
    EMPLOYER_KEY = 'wehrtyou'


class KavakScraper(GreenhouseScraper):
    employer_name = 'Kavak'
    EMPLOYER_KEY = 'kavakcareers'


class HeadwayScraper(GreenhouseScraper):
    employer_name = 'Headway'
    EMPLOYER_KEY = 'headway'


class JaneStreetScraper(GreenhouseScraper):
    employer_name = 'Jane Street'
    EMPLOYER_KEY = 'janestreet'


class GetsafeScraper(GreenhouseScraper):
    employer_name = 'GetSafe'
    EMPLOYER_KEY = 'getsafe'


class ZscalerScraper(SmartRecruitersScraper):
    employer_name = 'Zscaler'
    EMPLOYER_KEY = 'Zscaler'


class Point72Scraper(GreenhouseScraper):
    employer_name = 'Point72'
    EMPLOYER_KEY = 'point72'


class MessariScraper(GreenhouseScraper):
    employer_name = 'Messari'
    EMPLOYER_KEY = 'messari'


class SpacexScraper(GreenhouseApiScraper):
    employer_name = 'SpaceX'
    EMPLOYER_KEY = 'spacex'


class AstSpacemobileScraper(GreenhouseApiScraper):
    employer_name = 'AST SpaceMobile'
    EMPLOYER_KEY = 'astspacemobile'


class TakealotScraper(GreenhouseScraper):
    employer_name = 'takealot.com'
    EMPLOYER_KEY = 'takealotcom'


class RiotGamesScraper(GreenhouseApiScraper):
    employer_name = 'Riot Games'
    EMPLOYER_KEY = 'riotgames'


class ThunesScraper(GreenhouseApiScraper):
    employer_name = 'Thunes'
    EMPLOYER_KEY = 'thunes'


class CompstakScraper(LeverScraper):
    employer_name = 'CompStak'
    EMPLOYER_KEY = 'compstak'


class GopuffScraper(LeverScraper):
    employer_name = 'goPuff'
    EMPLOYER_KEY = 'gopuff'


class CredScraper(LeverScraper):
    employer_name = 'CRED'
    EMPLOYER_KEY = 'cred'


class ChewyScraper(GreenhouseApiScraper):
    employer_name = 'Chewy'
    EMPLOYER_KEY = 'chewycom'


class FoodpandaScraper(GreenhouseScraper):
    employer_name = 'Foodpanda'
    EMPLOYER_KEY = 'foodpandapakistan'


class TipaltiScraper(GreenhouseApiScraper):
    employer_name = 'Tipalti'
    EMPLOYER_KEY = 'tipaltisolutions'


class OcadoScraper(WorkdayScraper):
    employer_name = 'Ocado'
    start_url = 'https://ocado.wd3.myworkdayjobs.com/en-US/OcadoGroupCareers/'
    has_job_departments = False


class AdevintaScraper(SmartRecruitersScraper):
    employer_name = 'Adevinta'
    EMPLOYER_KEY = 'Adevinta'


class MedallionScraper(GreenhouseApiScraper):
    employer_name = 'Medallion'
    EMPLOYER_KEY = 'medallion'


class AvaloqGroupScraper(SmartRecruitersScraper):
    employer_name = 'Avaloq Group'
    EMPLOYER_KEY = 'Avaloq1'


class BluevineScraper(GreenhouseScraper):
    employer_name = 'BlueVine'
    EMPLOYER_KEY = 'bluevineus'


class AgodaScraper(GreenhouseApiScraper):
    employer_name = 'Agoda'
    EMPLOYER_KEY = 'agoda'


class PeekScraper(LeverScraper):
    employer_name = 'Peek'
    EMPLOYER_KEY = 'peek'


class LevadataScraper(LeverScraper):
    employer_name = 'LevaData'
    EMPLOYER_KEY = 'levadata'


class UsertestingScraper(GreenhouseApiScraper):
    employer_name = 'UserTesting'
    EMPLOYER_KEY = 'usertesting48'


class TsImagineScraper(GreenhouseApiScraper):
    employer_name = 'TS Imagine'
    EMPLOYER_KEY = 'tsimagine'


class PaytrixScraper(WorkableScraper):
    employer_name = 'Paytrix'
    EMPLOYER_KEY = 'paytrix'


class CybercubeScraper(LeverScraper):
    employer_name = 'CyberCube'
    EMPLOYER_KEY = 'cybcube'


class ArkoseLabsScraper(GreenhouseScraper):
    employer_name = 'Arkose Labs'
    EMPLOYER_KEY = 'arkoselabs'


class GotoScraper(LeverScraper):
    employer_name = 'GoTo'
    EMPLOYER_KEY = 'GoToGroup'


class NubankScraper(GreenhouseScraper):
    employer_name = 'Nubank'
    EMPLOYER_KEY = 'nubank'


class GostudentScraper(GreenhouseApiScraper):
    employer_name = 'GoStudent'
    EMPLOYER_KEY = 'gostudent'


class ExpressvpnScraper(GreenhouseApiScraper):
    employer_name = 'ExpressVPN'
    EMPLOYER_KEY = 'expressvpn'


class CareemScraper(GreenhouseScraper):
    employer_name = 'Careem'
    EMPLOYER_KEY = 'careem'


class OneMedicalScraper(GreenhouseApiScraper):
    employer_name = 'One Medical'
    EMPLOYER_KEY = 'onemedical'


class DeliveryHeroScraper(WorkdayScraper):
    employer_name = 'Delivery Hero'
    start_url = 'https://deliveryhero.wd3.myworkdayjobs.com/en-US/DH/'
    has_job_departments = False


class OpenxScraper(LeverScraper):
    employer_name = 'OpenX'
    EMPLOYER_KEY = 'openx'


class CheckoutScraper(SmartRecruitersScraper):
    employer_name = 'Checkout.com'
    EMPLOYER_KEY = 'Checkoutcom1'


class AdyenScraper(GreenhouseScraper):
    employer_name = 'Adyen'
    EMPLOYER_KEY = 'adyen'


class PaloAltoNetworksScraper(SmartRecruitersScraper):
    employer_name = 'Palo Alto Networks'
    EMPLOYER_KEY = 'PaloAltoNetworks2'


class BackMarketScraper(LeverScraper):
    employer_name = 'Back Market'
    EMPLOYER_KEY = 'backmarket'


class BynderScraper(GreenhouseScraper):
    employer_name = 'Bynder'
    EMPLOYER_KEY = 'bynderjobs'


class ArchiproScraper(WorkableScraper):
    employer_name = 'ArchiPro'
    EMPLOYER_KEY = 'archipro-3'


class MarshmallowScraper(AshbyHQScraper):
    employer_name = 'Marshmallow'
    EMPLOYER_KEY = 'marshmallow'


class GrabScraper(WorkdayScraper):
    employer_name = 'Grab'
    start_url = 'https://grab.wd3.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class SaviyntScraper(LeverScraper):
    employer_name = 'Saviynt'
    EMPLOYER_KEY = 'saviynt'


class SentineloneScraper(GreenhouseApiScraper):
    employer_name = 'SentinelOne'
    EMPLOYER_KEY = 'sentinellabs'


class QuantexaScraper(WorkableScraper):
    employer_name = 'Quantexa'
    EMPLOYER_KEY = 'quantexa'


class TetrascienceScraper(WorkableScraper):
    employer_name = 'TetraScience'
    EMPLOYER_KEY = 'tetrascience'


class SportradarScraper(WorkdayScraper):
    employer_name = 'Sportradar'
    start_url = 'https://sportradar.wd3.myworkdayjobs.com/en-US/sportradar_careers/'
    has_job_departments = False


class NxpSemiScraper(WorkdayScraper):
    employer_name = 'NXP Semi'
    start_url = 'https://nxp.wd3.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class DeelScraper(AshbyHQScraper):
    employer_name = 'Deel'
    EMPLOYER_KEY = 'deel'


class HingeHealthScraper(LeverScraper):
    employer_name = 'Hinge Health'
    EMPLOYER_KEY = 'hingehealth'


class TokenMetricsScraper(LeverScraper):
    employer_name = 'Token Metrics'
    EMPLOYER_KEY = 'tokenmetrics'


class AltoScraper(GreenhouseScraper):
    employer_name = 'Alto'
    EMPLOYER_KEY = 'altoira'


class ZyngaScraper(GreenhouseApiScraper):
    employer_name = 'Zynga'
    EMPLOYER_KEY = 'zynga'


class WorkatoScraper(GreenhouseScraper):
    employer_name = 'Workato'
    EMPLOYER_KEY = 'workato'


class IconiqScraper(GreenhouseScraper):
    employer_name = 'ICONIQ'
    EMPLOYER_KEY = 'iconiqcapital'


class FlutterEntertainmentScraper(WorkdayScraper):
    employer_name = 'Flutter Entertainment'
    start_url = 'https://flutterbe.wd3.myworkdayjobs.com/en-US/FlutterInt_External/'
    has_job_departments = False


class Project44Scraper(GreenhouseScraper):
    employer_name = 'project44'
    EMPLOYER_KEY = 'project44'


class PlaytechScraper(SmartRecruitersScraper):
    employer_name = 'Playtech'
    EMPLOYER_KEY = 'Playtech'


class IovLabsScraper(LeverScraper):
    employer_name = 'IOV Labs'
    EMPLOYER_KEY = 'iovlabs'


class SumupScraper(GreenhouseApiScraper):
    employer_name = 'SumUp'
    EMPLOYER_KEY = 'sumup'


class ZellerScraper(LeverScraper):
    employer_name = 'Zeller'
    EMPLOYER_KEY = 'Zeller'


class PecanAiScraper(GreenhouseApiScraper):
    employer_name = 'Pecan AI'
    EMPLOYER_KEY = 'pecanai'


class AllegroScraper(SmartRecruitersScraper):
    employer_name = 'Allegro'
    EMPLOYER_KEY = 'Allegro'


class ShopmonkeyScraper(GreenhouseApiScraper):
    employer_name = 'Shopmonkey'
    EMPLOYER_KEY = 'shopmonkey'


class RappiScraper(WorkdayScraper):
    employer_name = 'Rappi'
    start_url = 'https://rappi.wd3.myworkdayjobs.com/es/Rappi_jobs/'
    has_job_departments = False


class AccentureScraper(WorkdayScraper):
    employer_name = 'Accenture'
    start_url = 'https://accenture.wd3.myworkdayjobs.com/en-US/AccentureCareers/'
    has_job_departments = False


class BlockScraper(SmartRecruitersScraper):
    employer_name = 'Block (Square)'
    EMPLOYER_KEY = 'Square'


class PaytmScraper(LeverScraper):
    employer_name = 'Paytm'
    EMPLOYER_KEY = 'paytm'


class TripadvisorScraper(GreenhouseScraper):
    employer_name = 'Tripadvisor'
    EMPLOYER_KEY = 'tripadvisor'


class AmadeusScraper(WorkdayScraper):
    employer_name = 'Amadeus'
    start_url = 'https://amadeus.wd3.myworkdayjobs.com/en-US/jobs/'
    has_job_departments = False


class CrossRiverBankScraper(GreenhouseApiScraper):
    employer_name = 'Cross River Bank'
    EMPLOYER_KEY = 'crossriverbank'


class DaznScraper(LeverScraper):
    employer_name = 'DAZN'
    EMPLOYER_KEY = 'dazn'


class LtkScraper(GreenhouseScraper):
    employer_name = 'LTK'
    EMPLOYER_KEY = 'shopltk'


class AdobeScraper(WorkdayScraper):
    employer_name = 'Adobe'
    start_url = 'https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced/'
    has_job_departments = False


class ReltioScraper(GreenhouseScraper):
    employer_name = 'Reltio'
    EMPLOYER_KEY = 'reltio'


class BerlinBrandsGroupScraper(GreenhouseScraper):
    employer_name = 'Berlin Brands Group'
    EMPLOYER_KEY = 'berlinbrands'


class PointclickcareScraper(LeverScraper):
    employer_name = 'PointClickCare'
    EMPLOYER_KEY = 'pointclickcare'


class FanduelScraper(GreenhouseApiScraper):
    employer_name = 'FanDuel'
    EMPLOYER_KEY = 'fanduel'


class ScalableCapitalScraper(SmartRecruitersScraper):
    employer_name = 'Scalable Capital'
    EMPLOYER_KEY = 'ScalableGmbH'


class UnybrandsScraper(GreenhouseScraper):
    employer_name = 'Unybrands'
    EMPLOYER_KEY = 'unybrands'


class ArrayScraper(GreenhouseApiScraper):
    employer_name = 'Array'
    EMPLOYER_KEY = 'array'


class InmobiScraper(GreenhouseScraper):
    employer_name = 'InMobi'
    EMPLOYER_KEY = 'inmobi'


class QuantstampScraper(AshbyHQScraper):
    employer_name = 'Quantstamp'
    EMPLOYER_KEY = 'quantstamp'


class GympassScraper(GreenhouseApiScraper):
    employer_name = 'Gympass'
    EMPLOYER_KEY = 'gympass'


class F5Scraper(WorkdayScraper):
    employer_name = 'F5'
    start_url = 'https://ffive.wd5.myworkdayjobs.com/en-US/f5jobs/'
    has_job_departments = False


class IncodeTechnologiesScraper(GreenhouseScraper):
    employer_name = 'Incode Technologies'
    EMPLOYER_KEY = 'incode'


class SprinklrScraper(WorkdayScraper):
    employer_name = 'Sprinklr'
    start_url = 'https://sprinklr.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class XepelinScraper(LeverScraper):
    employer_name = 'Xepelin'
    EMPLOYER_KEY = 'xepelin'


class CambridgeMobileScraper(GreenhouseApiScraper):
    employer_name = 'Cambridge Mobile Telematics'
    EMPLOYER_KEY = 'cambridgemobiletelematics'


class FrubanaScraper(LeverScraper):
    employer_name = 'Frubana'
    EMPLOYER_KEY = 'frubana'


class OloScraper(LeverScraper):
    employer_name = 'Olo'
    EMPLOYER_KEY = 'olo'


class ThescoreScraper(GreenhouseScraper):
    employer_name = 'theScore'
    EMPLOYER_KEY = 'scoremediaandgaminginc'


class DatabricksScraper(GreenhouseApiScraper):
    employer_name = 'Databricks'
    EMPLOYER_KEY = 'databricks'


class X1Scraper(LeverScraper):
    employer_name = 'X1'
    EMPLOYER_KEY = 'x1creditcard'


class TridgeScraper(GreenhouseApiScraper):
    employer_name = 'Tridge'
    EMPLOYER_KEY = 'tridge'


class AntlerScraper(GreenhouseScraper):
    employer_name = 'Antler'
    EMPLOYER_KEY = 'antler'


class ElasticScraper(GreenhouseApiScraper):
    employer_name = 'Elastic'
    EMPLOYER_KEY = 'elastic'


class DatadogScraper(GreenhouseApiScraper):
    employer_name = 'Datadog'
    EMPLOYER_KEY = 'datadog'


class SesoScraper(GreenhouseScraper):
    employer_name = 'Seso'
    EMPLOYER_KEY = 'sesolabor'


class WallapopScraper(GreenhouseScraper):
    employer_name = 'Wallapop'
    EMPLOYER_KEY = 'wallapop'


class OvertimeScraper(GreenhouseScraper):
    employer_name = 'Overtime'
    EMPLOYER_KEY = 'overtime'


class DexcareScraper(LeverScraper):
    employer_name = 'DexCare'
    EMPLOYER_KEY = 'dexcarehealth'


class SeatgeekScraper(GreenhouseApiScraper):
    employer_name = 'SeatGeek'
    EMPLOYER_KEY = 'seatgeek'


class FormlabsScraper(GreenhouseApiScraper):
    employer_name = 'Formlabs'
    EMPLOYER_KEY = 'formlabs'


class TravelokaScraper(WorkdayScraper):
    employer_name = 'Traveloka'
    start_url = 'https://traveloka.wd3.myworkdayjobs.com/en-US/Traveloka/'
    has_job_departments = False


class ElevatebioScraper(GreenhouseScraper):
    employer_name = 'ElevateBio'
    EMPLOYER_KEY = 'elevatebio'


class TenXGenomicsScraper(GreenhouseApiScraper):
    employer_name = '10X Genomics'
    EMPLOYER_KEY = '10xgenomics'


class ZetaGlobalScraper(GreenhouseApiScraper):
    employer_name = 'Zeta Global'
    EMPLOYER_KEY = 'zetaglobal'


class CompassScraper(GreenhouseApiScraper):
    employer_name = 'Compass'
    EMPLOYER_KEY = 'urbancompass'


class EbanxScraper(GreenhouseScraper):
    employer_name = 'EBANX'
    EMPLOYER_KEY = 'ebanx'


class TrustpilotScraper(GreenhouseApiScraper):
    employer_name = 'Trustpilot'
    EMPLOYER_KEY = 'trustpilot'


class IntelScraper(WorkdayScraper):
    employer_name = 'Intel'
    start_url = 'https://intel.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class ImagenScraper(GreenhouseScraper):
    employer_name = 'Imagen'
    EMPLOYER_KEY = 'imagentechnologies'


class AbcFitnessScraper(WorkdayScraper):
    employer_name = 'ABC Fitness'
    start_url = 'https://abcfinancial.wd5.myworkdayjobs.com/en-US/ABCFinancialServices/'
    has_job_departments = False


class MonzoScraper(GreenhouseScraper):
    employer_name = 'Monzo'
    EMPLOYER_KEY = 'monzo'


class TrimbleScraper(WorkdayScraper):
    employer_name = 'Trimble'
    start_url = 'https://trimble.wd1.myworkdayjobs.com/en-US/TrimbleCareers/'
    has_job_departments = False


class LaunchdarklyScraper(GreenhouseScraper):
    employer_name = 'LaunchDarkly'
    EMPLOYER_KEY = 'launchdarkly'


class SwordHealthScraper(LeverScraper):
    employer_name = 'Sword Health'
    EMPLOYER_KEY = 'swordhealth'


class BranchScraper(GreenhouseApiScraper):
    employer_name = 'Branch'
    EMPLOYER_KEY = 'branch'


class WoltScraper(SmartRecruitersScraper):
    employer_name = 'Wolt'
    EMPLOYER_KEY = 'Wolt'


class FeaturespaceScraper(GreenhouseApiScraper):
    employer_name = 'Featurespace'
    EMPLOYER_KEY = 'featurespace'


class GlobalfoundriesScraper(WorkdayScraper):
    employer_name = 'GlobalFoundries'
    start_url = 'https://globalfoundries.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class OscarHealthScraper(GreenhouseApiScraper):
    employer_name = 'Oscar Health'
    EMPLOYER_KEY = 'oscar'


class SeismicScraper(GreenhouseApiScraper):
    employer_name = 'Seismic'
    EMPLOYER_KEY = 'seismicsoftware'


class RyeScraper(AshbyHQScraper):
    employer_name = 'Rye'
    EMPLOYER_KEY = 'rye'


class MaxarScraper(WorkdayScraper):
    employer_name = 'Maxar'
    start_url = 'https://maxar.wd1.myworkdayjobs.com/en-US/MAXAR/'
    has_job_departments = False


class ChargepointScraper(GreenhouseApiScraper):
    employer_name = 'ChargePoint'
    EMPLOYER_KEY = 'chargepoint'


class IrobotScraper(WorkdayScraper):
    employer_name = 'iRobot'
    start_url = 'https://irobot.wd5.myworkdayjobs.com/en-US/iRobot/'
    has_job_departments = False


class PismoScraper(GreenhouseScraper):
    employer_name = 'Pismo'
    EMPLOYER_KEY = 'pismo'


class RocketLabScraper(GreenhouseScraper):
    employer_name = 'Rocket Lab'
    EMPLOYER_KEY = 'rocketlab'


class UnitedmastersScraper(GreenhouseScraper):
    employer_name = 'UnitedMasters'
    EMPLOYER_KEY = 'unitedmasters'


class JoorScraper(GreenhouseApiScraper):
    employer_name = 'JOOR'
    EMPLOYER_KEY = 'joor'


class TheFarmersDogScraper(GreenhouseScraper):
    employer_name = 'The Farmer’s Dog'
    EMPLOYER_KEY = 'thefarmersdog'


class MoonpigScraper(LeverScraper):
    employer_name = 'Moonpig'
    EMPLOYER_KEY = 'moonpig'


class JeevesScraper(LeverScraper):
    employer_name = 'Jeeves'
    EMPLOYER_KEY = 'tryjeeves'


class CakeDefiScraper(GreenhouseScraper):
    employer_name = 'Cake DeFi'
    EMPLOYER_KEY = 'cakedefi'


class ViantScraper(LeverScraper):
    employer_name = 'Viant'
    EMPLOYER_KEY = 'viantinc'


class OptimoveScraper(GreenhouseScraper):
    employer_name = 'Optimove'
    EMPLOYER_KEY = 'optimove'


class HikeScraper(WorkableScraper):
    employer_name = 'Hike'
    EMPLOYER_KEY = 'hike'


class PelotonScraper(GreenhouseApiScraper):
    employer_name = 'Peloton'
    EMPLOYER_KEY = 'peloton'


class AivenScraper(GreenhouseApiScraper):
    employer_name = 'Aiven'
    EMPLOYER_KEY = 'aiven36'


class ClearcoverScraper(GreenhouseScraper):
    employer_name = 'Clearcover'
    EMPLOYER_KEY = 'clearcover'


class WayfairScraper(GreenhouseApiScraper):
    employer_name = 'Wayfair'
    EMPLOYER_KEY = 'wayfair'


class AppsflyerScraper(GreenhouseApiScraper):
    employer_name = 'AppsFlyer'
    EMPLOYER_KEY = 'appsflyer'


class PaypalScraper(WorkdayScraper):
    employer_name = 'PayPal'
    start_url = 'https://paypal.wd1.myworkdayjobs.com/en-US/jobs/'
    has_job_departments = False


class GohealthScraper(GreenhouseScraper):
    employer_name = 'GoHealth'
    EMPLOYER_KEY = 'gohealth'


class HealthverityScraper(LeverScraper):
    employer_name = 'HealthVerity'
    EMPLOYER_KEY = 'healthverity'


class RokuScraper(GreenhouseApiScraper):
    employer_name = 'Roku'
    EMPLOYER_KEY = 'roku'


class CleoScraper(GreenhouseScraper):
    employer_name = 'Cleo'
    EMPLOYER_KEY = 'cleoai'


class ToastScraper(GreenhouseApiScraper):
    employer_name = 'Toast'
    EMPLOYER_KEY = 'toast'


class TovalaScraper(LeverScraper):
    employer_name = 'Tovala'
    EMPLOYER_KEY = 'tovala'


class FarfetchScraper(LeverScraper):
    employer_name = 'Farfetch'
    EMPLOYER_KEY = 'farfetch'


class ConstellationScraper(WorkdayScraper):
    employer_name = 'Constellation'
    start_url = 'https://cbrands.wd5.myworkdayjobs.com/en-US/CBI_External_Careers/'
    has_job_departments = False


class BettermentScraper(GreenhouseApiScraper):
    employer_name = 'Betterment'
    EMPLOYER_KEY = 'betterment'


class IntappScraper(WorkdayScraper):
    employer_name = 'Intapp'
    start_url = 'https://intapp.wd1.myworkdayjobs.com/en-US/Intapp/'
    has_job_departments = False


class VuoriScraper(SmartRecruitersScraper):
    employer_name = 'Vuori'
    EMPLOYER_KEY = 'VuoriInc'


class OcrolusScraper(GreenhouseScraper):
    employer_name = 'Ocrolus'
    EMPLOYER_KEY = 'ocrolusinc'


class TwoKScraper(GreenhouseScraper):
    employer_name = '2K'
    EMPLOYER_KEY = '2k'


class CelonisScraper(GreenhouseScraper):
    employer_name = 'Celonis'
    EMPLOYER_KEY = 'celonis'


class Dream11Scraper(LeverScraper):
    employer_name = 'Dream11'
    EMPLOYER_KEY = 'dreamsports'


class PubnubScraper(GreenhouseApiScraper):
    employer_name = 'PubNub'
    EMPLOYER_KEY = 'pubnub'


class PaltaScraper(GreenhouseScraper):
    employer_name = 'Palta'
    EMPLOYER_KEY = 'paltaltd'


class CostarGroupScraper(WorkdayScraper):
    employer_name = 'CoStar Group'
    start_url = 'https://costar.wd1.myworkdayjobs.com/en-US/CoStarCareers/'
    has_job_departments = False


class SnykScraper(GreenhouseScraper):
    employer_name = 'Snyk'
    EMPLOYER_KEY = 'snyk'


class RelativityScraper(LeverScraper):
    employer_name = 'Relativity'
    EMPLOYER_KEY = 'relativity'


class BitgetScraper(WorkableScraper):
    employer_name = 'Bitget'
    EMPLOYER_KEY = 'bitget'


class EngagesmartScraper(GreenhouseApiScraper):
    employer_name = 'EngageSmart'
    EMPLOYER_KEY = 'engagesmart'


class DoctolibScraper(GreenhouseScraper):
    employer_name = 'Doctolib'
    EMPLOYER_KEY = 'doctolib'


class RazorGroupScraper(GreenhouseScraper):
    employer_name = 'Razor Group'
    EMPLOYER_KEY = 'razorgroupgmbh'


class VoxMediaScraper(GreenhouseApiScraper):
    employer_name = 'Vox Media'
    EMPLOYER_KEY = 'voxmedia'


class AltruistiqScraper(GreenhouseScraper):
    employer_name = 'Altruistiq'
    EMPLOYER_KEY = 'altruistiq'


class UpworkScraper(GreenhouseScraper):
    employer_name = 'Upwork'
    EMPLOYER_KEY = 'upwork'


class HubspotScraper(GreenhouseApiScraper):
    employer_name = 'Hubspot'
    EMPLOYER_KEY = 'hubspotjobs'


class ClearbitScraper(LeverScraper):
    employer_name = 'Clearbit'
    EMPLOYER_KEY = 'clearbit'


class CazooScraper(GreenhouseScraper):
    employer_name = 'Cazoo'
    EMPLOYER_KEY = 'cazoo'


class XeroScraper(LeverScraper):
    employer_name = 'Xero'
    EMPLOYER_KEY = 'xero'


class CybereasonScraper(GreenhouseApiScraper):
    employer_name = 'Cybereason'
    EMPLOYER_KEY = 'cybereason'


class CarvanaScraper(GreenhouseApiScraper):
    employer_name = 'Carvana'
    EMPLOYER_KEY = 'carvana'


class DataikuScraper(GreenhouseScraper):
    employer_name = 'Dataiku'
    EMPLOYER_KEY = 'dataiku'


class CrowdstrikeScraper(WorkdayScraper):
    employer_name = 'CrowdStrike'
    start_url = 'https://crowdstrike.wd5.myworkdayjobs.com/en-US/crowdstrikecareers/'
    has_job_departments = False


class CartaScraper(GreenhouseScraper):
    employer_name = 'Carta'
    EMPLOYER_KEY = 'carta'


class PachamaScraper(LeverScraper):
    employer_name = 'Pachama'
    EMPLOYER_KEY = 'pachama'


class ForterScraper(GreenhouseScraper):
    employer_name = 'Forter'
    EMPLOYER_KEY = 'forter'


class WizScraper(GreenhouseScraper):
    employer_name = 'Wiz'
    EMPLOYER_KEY = 'wizinc'


class PomeloCareScraper(GreenhouseScraper):
    employer_name = 'Pomelo Care'
    EMPLOYER_KEY = 'pomelocare'


class AirwallexScraper(LeverScraper):
    employer_name = 'Airwallex'
    EMPLOYER_KEY = 'airwallex'


class SoloIoScraper(GreenhouseScraper):
    employer_name = 'Solo.io'
    EMPLOYER_KEY = 'soloioinc'


class CanvaScraper(LeverScraper):
    employer_name = 'Canva'
    EMPLOYER_KEY = 'canva'


class ParabolaScraper(GreenhouseScraper):
    employer_name = 'Parabola'
    EMPLOYER_KEY = 'parabola'


class BinanceScraper(LeverScraper):
    employer_name = 'Binance'
    EMPLOYER_KEY = 'binance'


class CompanycamScraper(GreenhouseApiScraper):
    employer_name = 'CompanyCam'
    EMPLOYER_KEY = 'companycam'


class PayhawkScraper(GreenhouseScraper):
    employer_name = 'Payhawk'
    EMPLOYER_KEY = 'payhawkio'


class ChocoScraper(GreenhouseApiScraper):
    employer_name = 'Choco'
    EMPLOYER_KEY = 'choco'


class TeyaScraper(SmartRecruitersScraper):
    employer_name = 'Teya'
    EMPLOYER_KEY = 'Teya'


class TrengoScraper(LeverScraper):
    employer_name = 'Trengo'
    EMPLOYER_KEY = 'Trengobv'


class MosaicScraper(LeverScraper):
    employer_name = 'Mosaic'
    EMPLOYER_KEY = 'mosaic-2'


class ForwardNetworksScraper(GreenhouseScraper):
    employer_name = 'Forward Networks'
    EMPLOYER_KEY = 'forwardnetworks'


class YapilyScraper(WorkableScraper):
    employer_name = 'Yapily'
    EMPLOYER_KEY = 'yapily'


class TealbookScraper(LeverScraper):
    employer_name = 'TealBook'
    EMPLOYER_KEY = 'tealbook'


class TalkdeskScraper(GreenhouseApiScraper):
    employer_name = 'TalkDesk'
    EMPLOYER_KEY = 'talkdesk'


class BenchlingScraper(GreenhouseApiScraper):
    employer_name = 'Benchling'
    EMPLOYER_KEY = 'benchling'


class SylveraScraper(LeverScraper):
    employer_name = 'Sylvera'
    EMPLOYER_KEY = 'sylvera'


class DocplannerScraper(SmartRecruitersScraper):
    employer_name = 'DocPlanner'
    EMPLOYER_KEY = 'Docplanner'


class XentralScraper(LeverScraper):
    employer_name = 'Xentral'
    EMPLOYER_KEY = 'xentral'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class CoupangScraper(GreenhouseApiScraper):
    employer_name = 'Coupang'
    EMPLOYER_KEY = 'coupang'


class SuperpedestrianScraper(LeverScraper):
    employer_name = 'Superpedestrian'
    EMPLOYER_KEY = 'superpedestrian'


class DeliverooScraper(GreenhouseScraper):
    employer_name = 'Deliveroo'
    EMPLOYER_KEY = 'deliveroo'


class GrafanaScraper(GreenhouseScraper):
    employer_name = 'Grafana'
    EMPLOYER_KEY = 'grafanalabs'


class OrcaSecurityScraper(GreenhouseApiScraper):
    employer_name = 'Orca Security'
    EMPLOYER_KEY = 'orcasecurity'


class TrustlyScraper(LeverScraper):
    employer_name = 'Trustly'
    EMPLOYER_KEY = 'trustly'


class SmsAssistScraper(WorkdayScraper):
    employer_name = 'SMS Assist'
    start_url = 'https://smsassist.wd5.myworkdayjobs.com/en-US/SMSAssistcareers/'
    has_job_departments = False


class SkyflowScraper(GreenhouseScraper):
    employer_name = 'Skyflow'
    EMPLOYER_KEY = 'skyflow'


class AppliedIntuitionScraper(GreenhouseApiScraper):
    employer_name = 'Applied Intuition'
    EMPLOYER_KEY = 'appliedintuition'


class GohenryScraper(WorkableScraper):
    employer_name = 'GoHenry'
    EMPLOYER_KEY = 'gohenry'


class NavanScraper(GreenhouseApiScraper):
    employer_name = 'Navan'
    EMPLOYER_KEY = 'tripactions'


class ElevateK12Scraper(GreenhouseApiScraper):
    employer_name = 'Elevate K-12'
    EMPLOYER_KEY = 'elevatek12'


class HumuScraper(GreenhouseScraper):
    employer_name = 'Humu'
    EMPLOYER_KEY = 'humu'


class PleoScraper(GreenhouseScraper):
    employer_name = 'Pleo'
    EMPLOYER_KEY = 'pleo'


class WonoloScraper(LeverScraper):
    employer_name = 'Wonolo'
    EMPLOYER_KEY = 'wonolo'


class GitlabScraper(GreenhouseScraper):
    employer_name = 'GitLab'
    EMPLOYER_KEY = 'gitlab'


class WooScraper(GreenhouseScraper):
    employer_name = 'Woo'
    EMPLOYER_KEY = 'woonetwork'


class OpengovScraper(LeverScraper):
    employer_name = 'OpenGov'
    EMPLOYER_KEY = 'opengov'


class OnesignalScraper(GreenhouseScraper):
    employer_name = 'OneSignal'
    EMPLOYER_KEY = 'onesignal'


class KeeperSecurityScraper(WorkableScraper):
    employer_name = 'Keeper Security'
    EMPLOYER_KEY = 'keepersecurity'


class HarnessScraper(LeverScraper):
    employer_name = 'Harness'
    EMPLOYER_KEY = 'harness'


class TaxfyleScraper(LeverScraper):
    employer_name = 'Taxfyle'
    EMPLOYER_KEY = 'taxfyle'


class TiltingPointScraper(GreenhouseApiScraper):
    employer_name = 'Tilting Point'
    EMPLOYER_KEY = 'tiltingpoint'


class HivebriteScraper(LeverScraper):
    employer_name = 'Hivebrite'
    EMPLOYER_KEY = 'hivebrite'


class HeyjobsScraper(AshbyHQScraper):
    employer_name = 'HeyJobs'
    EMPLOYER_KEY = 'heyjobs'


class ZoominfoScraper(GreenhouseApiScraper):
    employer_name = 'Zoominfo'
    EMPLOYER_KEY = 'zoominfo'


class ToriiScraper(GreenhouseApiScraper):
    employer_name = 'Torii'
    EMPLOYER_KEY = 'toriihq'


class AtmosphereTvScraper(GreenhouseApiScraper):
    employer_name = 'Atmosphere TV'
    EMPLOYER_KEY = 'atmosphere'


class StarlingBankScraper(WorkableScraper):
    employer_name = 'Starling Bank'
    EMPLOYER_KEY = 'starling-bank'


class GlorifyScraper(WorkableScraper):
    employer_name = 'Glorify'
    EMPLOYER_KEY = 'glorify'


class MytrafficScraper(LeverScraper):
    employer_name = 'Mytraffic'
    EMPLOYER_KEY = 'mytraffic'


class CharlesScraper(GreenhouseScraper):
    employer_name = 'Charles'
    EMPLOYER_KEY = 'charles'


class SpotifyScraper(LeverScraper):
    employer_name = 'Spotify'
    EMPLOYER_KEY = 'spotify'


class AnalogDevicesScraper(WorkdayScraper):
    employer_name = 'Analog Devices'
    start_url = 'https://analogdevices.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class FormaScraper(AshbyHQScraper):
    employer_name = 'Forma'
    EMPLOYER_KEY = 'forma'


class CrusoeEnergyScraper(AshbyHQScraper):
    employer_name = 'Crusoe Energy'
    EMPLOYER_KEY = 'Crusoe'


class TealiumScraper(WorkdayScraper):
    employer_name = 'Tealium'
    start_url = 'https://tealium.wd1.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class NetskopeScraper(GreenhouseApiScraper):
    employer_name = 'Netskope'
    EMPLOYER_KEY = 'netskope'


class BackbaseScraper(GreenhouseScraper):
    employer_name = 'Backbase'
    EMPLOYER_KEY = 'workatbackbase'


class NuvemshopScraper(WorkableScraper):
    employer_name = 'Nuvemshop'
    EMPLOYER_KEY = 'tiendanube-nuvemshop'


class SalesforceScraper(WorkdayScraper):
    employer_name = 'Salesforce'
    start_url = 'https://salesforce.wd12.myworkdayjobs.com/External_Career_Site/'
    has_job_departments = False


class HippoScraper(GreenhouseApiScraper):
    employer_name = 'Hippo'
    EMPLOYER_KEY = 'hippo70'


class ImpossibleFoodsScraper(LeverScraper):
    employer_name = 'Impossible Foods'
    EMPLOYER_KEY = 'impossiblefoods'


class AkqaScraper(GreenhouseApiScraper):
    employer_name = 'AKQA'
    EMPLOYER_KEY = 'akqa'


class DiligentRoboticsScraper(GreenhouseScraper):
    employer_name = 'Diligent Robotics'
    EMPLOYER_KEY = 'diligentrobotics'


class HumanInterestScraper(GreenhouseScraper):
    employer_name = 'Human Interest'
    EMPLOYER_KEY = 'humaninterest'


class CohesityScraper(GreenhouseApiScraper):
    employer_name = 'Cohesity'
    EMPLOYER_KEY = 'cohesity'


class SevenshiftsScraper(GreenhouseScraper):
    employer_name = '7shifts'
    EMPLOYER_KEY = '7shifts'


class KlaviyoScraper(GreenhouseApiScraper):
    employer_name = 'Klaviyo'
    EMPLOYER_KEY = 'klaviyo'


class TrivagoScraper(GreenhouseApiScraper):
    employer_name = 'trivago'
    EMPLOYER_KEY = 'trivago'


class FreshworksScraper(SmartRecruitersScraper):
    employer_name = 'Freshworks'
    EMPLOYER_KEY = 'Freshworks'


class CartoScraper(LeverScraper):
    employer_name = 'Carto'
    EMPLOYER_KEY = 'cartodb'


class VannevarLabsScraper(LeverScraper):
    employer_name = 'Vannevar Labs'
    EMPLOYER_KEY = 'vannevarlabs-2'


class RechargeScraper(GreenhouseScraper):
    employer_name = 'ReCharge'
    EMPLOYER_KEY = 'recharge'


class ZipScraper(GreenhouseScraper):
    employer_name = 'Zip'
    EMPLOYER_KEY = 'zip'


class AristaNetworksScraper(SmartRecruitersScraper):
    employer_name = 'Arista Networks'
    EMPLOYER_KEY = 'AristaNetworks'


class BeaconScraper(GreenhouseScraper):
    employer_name = 'Beacon'
    EMPLOYER_KEY = 'beaconplatform'


class WorkstreamScraper(GreenhouseApiScraper):
    employer_name = 'Workstream'
    EMPLOYER_KEY = 'workstream'


class FireblocksScraper(GreenhouseApiScraper):
    employer_name = 'Fireblocks'
    EMPLOYER_KEY = 'fireblocks'


class FubotvScraper(GreenhouseApiScraper):
    employer_name = 'FuboTV'
    EMPLOYER_KEY = 'fubotv'


class SimilarwebScraper(GreenhouseScraper):
    employer_name = 'SimilarWeb'
    EMPLOYER_KEY = 'similarweb'


class DellScraper(WorkdayScraper):
    employer_name = 'Dell'
    start_url = 'https://dell.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class TideScraper(GreenhouseScraper):
    employer_name = 'Tide'
    EMPLOYER_KEY = 'tide'


class KlaScraper(WorkdayScraper):
    employer_name = 'KLA'
    start_url = 'https://kla.wd1.myworkdayjobs.com/en-US/Search/'
    has_job_departments = False


class LodgifyScraper(LeverScraper):
    employer_name = 'Lodgify'
    EMPLOYER_KEY = 'lodgify'


class RewindSoftwareScraper(SmartRecruitersScraper):
    employer_name = 'Rewind Software'
    EMPLOYER_KEY = 'RewindSoftware'


class TaboolaScraper(GreenhouseApiScraper):
    employer_name = 'Taboola'
    EMPLOYER_KEY = 'taboola'


class FivetranScraper(GreenhouseApiScraper):
    employer_name = 'FiveTran'
    EMPLOYER_KEY = 'fivetran'


class DruvaScraper(GreenhouseApiScraper):
    employer_name = 'Druva'
    EMPLOYER_KEY = 'druva'


class LetsDoThisScraper(WorkableScraper):
    employer_name = 'Let\'s Do This'
    EMPLOYER_KEY = 'lets-do-this'


class FreenowScraper(GreenhouseScraper):
    employer_name = 'FREENOW'
    EMPLOYER_KEY = 'freenow'


class WebflowScraper(GreenhouseScraper):
    employer_name = 'Webflow'
    EMPLOYER_KEY = 'webflow'


class BeyondtrustScraper(GreenhouseScraper):
    employer_name = 'BeyondTrust'
    EMPLOYER_KEY = 'beyondtrust'


class TwoUScraper(GreenhouseScraper):
    employer_name = '2U'
    EMPLOYER_KEY = '2u'


class IvaluaScraper(GreenhouseApiScraper):
    employer_name = 'Ivalua'
    EMPLOYER_KEY = 'ivalua'


class SolarwindsScraper(GreenhouseApiScraper):
    employer_name = 'SolarWinds'
    EMPLOYER_KEY = 'solarwinds'


class GeniusSportsScraper(GreenhouseApiScraper):
    employer_name = 'Genius Sports'
    EMPLOYER_KEY = 'geniussports'


class LyraHealthScraper(LeverScraper):
    employer_name = 'Lyra Health'
    EMPLOYER_KEY = 'lyrahealth'


class ImmersiveLabsScraper(GreenhouseApiScraper):
    employer_name = 'Immersive Labs'
    EMPLOYER_KEY = 'immersivelabs'


class HealthjoyScraper(GreenhouseScraper):
    employer_name = 'HealthJoy'
    EMPLOYER_KEY = 'healthjoy'


class AiseraScraper(GreenhouseScraper):
    employer_name = 'Aisera'
    EMPLOYER_KEY = 'aiserajobs'


class VestiaireScraper(GreenhouseApiScraper):
    employer_name = 'Vestiaire'
    EMPLOYER_KEY = 'vestiairecollective'


class BrazeScraper(GreenhouseApiScraper):
    employer_name = 'Braze'
    EMPLOYER_KEY = 'braze'


class TheHutGroupScraper(GreenhouseApiScraper):
    employer_name = 'The Hut Group'
    EMPLOYER_KEY = 'thehutgroup'


class SamsungScraper(WorkdayScraper):
    employer_name = 'Samsung'
    start_url = 'https://sec.wd3.myworkdayjobs.com/en-US/Samsung_Careers/'
    has_job_departments = False


class SleeperScraper(AshbyHQScraper):
    employer_name = 'Sleeper'
    EMPLOYER_KEY = 'sleeper'


class SamsaraScraper(GreenhouseApiScraper):
    employer_name = 'Samsara'
    EMPLOYER_KEY = 'samsara'


class AcronisScraper(GreenhouseScraper):
    employer_name = 'Acronis'
    EMPLOYER_KEY = 'acronis'


class WrapbookScraper(GreenhouseApiScraper):
    employer_name = 'Wrapbook'
    EMPLOYER_KEY = 'wrapbook'


class ZoneAndCoScraper(WorkableScraper):
    employer_name = 'Zone & Co'
    EMPLOYER_KEY = 'zoneandco'


class JamfScraper(GreenhouseApiScraper):
    employer_name = 'JAMF'
    EMPLOYER_KEY = 'jamf'


class LiquibaseScraper(GreenhouseApiScraper):
    employer_name = 'Liquibase'
    EMPLOYER_KEY = 'liquibase'


class GlintsScraper(LeverScraper):
    employer_name = 'Glints'
    EMPLOYER_KEY = 'glints'


class MudflapScraper(GreenhouseApiScraper):
    employer_name = 'Mudflap'
    EMPLOYER_KEY = 'mudflap'


class BabylonHealthScraper(GreenhouseScraper):
    employer_name = 'Babylon Health'
    EMPLOYER_KEY = 'babylon'


class KlueScraper(LeverScraper):
    employer_name = 'Klue'
    EMPLOYER_KEY = 'klue'


class AstranisScraper(GreenhouseScraper):
    employer_name = 'Astranis'
    EMPLOYER_KEY = 'astranis'


class OmnipresentScraper(GreenhouseScraper):
    employer_name = 'Omnipresent'
    EMPLOYER_KEY = 'omnipresent'


class TemplafyScraper(GreenhouseScraper):
    employer_name = 'Templafy'
    EMPLOYER_KEY = 'templafy'


class OutbrainScraper(GreenhouseScraper):
    employer_name = 'Outbrain'
    EMPLOYER_KEY = 'outbraininc'


class AssembledScraper(GreenhouseScraper):
    employer_name = 'Assembled'
    EMPLOYER_KEY = 'assembled'


class NiumScraper(LeverScraper):
    employer_name = 'Nium'
    EMPLOYER_KEY = 'nium'


class GwiScraper(GreenhouseApiScraper):
    employer_name = 'GWI'
    EMPLOYER_KEY = 'globalwebindex'


class Three60learningScraper(LeverScraper):
    employer_name = '360learning'
    EMPLOYER_KEY = '360learning'


class GrouponScraper(WorkdayScraper):
    employer_name = 'Groupon'
    start_url = 'https://grab.wd3.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class FiservScraper(WorkdayScraper):
    employer_name = 'Fiserv'
    start_url = 'https://fiserv.wd5.myworkdayjobs.com/en-US/EXT/'
    has_job_departments = False


class AspentechScraper(WorkdayScraper):
    employer_name = 'AspenTech'
    start_url = 'https://aspentech.wd5.myworkdayjobs.com/en-US/aspentech/'
    has_job_departments = False


class Cars24Scraper(WorkableScraper):
    employer_name = 'Cars24'
    EMPLOYER_KEY = 'cars24'


class HazelHealthScraper(GreenhouseScraper):
    employer_name = 'Hazel Health'
    EMPLOYER_KEY = 'hazel'


class QumuloScraper(GreenhouseApiScraper):
    employer_name = 'Qumulo'
    EMPLOYER_KEY = 'qumulo'


class BlinkistScraper(GreenhouseScraper):
    employer_name = 'Blinkist'
    EMPLOYER_KEY = 'blinkist'


class SmartlyScraper(GreenhouseApiScraper):
    employer_name = 'Smartly'
    EMPLOYER_KEY = 'smartlyio'


class QualysScraper(WorkdayScraper):
    employer_name = 'Qualys'
    start_url = 'https://qualys.wd5.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class MobileyeScraper(LeverScraper):
    employer_name = 'Mobileye'
    EMPLOYER_KEY = 'mobileye'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class LumafieldScraper(LeverScraper):
    employer_name = 'Lumafield'
    EMPLOYER_KEY = 'lumafield'


class FisScraper(WorkdayScraper):
    employer_name = 'FIS'
    start_url = 'https://fis.wd5.myworkdayjobs.com/en-US/SearchJobs/'
    has_job_departments = False


class RingcentralScraper(WorkdayScraper):
    employer_name = 'RingCentral'
    start_url = 'https://ringcentral.wd1.myworkdayjobs.com/en-US/RingCentral_Careers/'
    has_job_departments = False


class BoxScraper(GreenhouseScraper):
    employer_name = 'Box'
    EMPLOYER_KEY = 'boxinc'


class UpguardScraper(LeverScraper):
    employer_name = 'UpGuard'
    EMPLOYER_KEY = 'upguard'


class TrendMicroScraper(WorkdayScraper):
    employer_name = 'Trend Micro'
    start_url = 'https://trendmicro.wd3.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class Auto1GroupScraper(SmartRecruitersScraper):
    employer_name = 'Auto1 Group'
    EMPLOYER_KEY = 'Auto1'


class PandadocScraper(GreenhouseApiScraper):
    employer_name = 'PandaDoc'
    EMPLOYER_KEY = 'pandadoc'


class TruliooScraper(GreenhouseApiScraper):
    employer_name = 'Trulioo'
    EMPLOYER_KEY = 'trulioo'


class PersonaScraper(LeverScraper):
    employer_name = 'Persona'
    EMPLOYER_KEY = 'persona'


class NinefinScraper(WorkableScraper):
    employer_name = '9fin'
    EMPLOYER_KEY = '9fin'


class TigeraScraper(GreenhouseApiScraper):
    employer_name = 'Tigera'
    EMPLOYER_KEY = 'tigera'


class PeakAiScraper(GreenhouseScraper):
    employer_name = 'Peak AI'
    EMPLOYER_KEY = 'peakailimited'


class SinchScraper(WorkableScraper):
    employer_name = 'Sinch'
    EMPLOYER_KEY = 'sinch'


class PitchbookScraper(GreenhouseScraper):
    employer_name = 'Pitchbook'
    EMPLOYER_KEY = 'pitchbookdata'


class QuintoandarScraper(WorkableScraper):
    employer_name = 'QuintoAndar'
    EMPLOYER_KEY = 'quintoandar'


class DlocalScraper(LeverScraper):
    employer_name = 'dLocal'
    EMPLOYER_KEY = 'dlocal'


class MeritScraper(LeverScraper):
    employer_name = 'Merit'
    EMPLOYER_KEY = 'merit'


class LaceworkScraper(GreenhouseApiScraper):
    employer_name = 'Lacework'
    EMPLOYER_KEY = 'lacework'


class ApolloIoScraper(GreenhouseScraper):
    employer_name = 'Apollo.io'
    EMPLOYER_KEY = 'apolloio'


class ExpediaScraper(WorkdayScraper):
    employer_name = 'Expedia'
    start_url = 'https://expedia.wd5.myworkdayjobs.com/en-US/search/'
    has_job_departments = False


class KlookScraper(WorkdayScraper):
    employer_name = 'Klook'
    start_url = 'https://klook.wd3.myworkdayjobs.com/en-US/KlookCareers/'
    has_job_departments = False


class PreplyScraper(GreenhouseApiScraper):
    employer_name = 'Preply'
    EMPLOYER_KEY = 'preply'


class VectraAiScraper(GreenhouseScraper):
    employer_name = 'Vectra AI'
    EMPLOYER_KEY = 'vectranetworks'


class IncortaScraper(LeverScraper):
    employer_name = 'Incorta'
    EMPLOYER_KEY = 'incorta'


class ShelfIoScraper(GreenhouseApiScraper):
    employer_name = 'Shelf.io'
    EMPLOYER_KEY = 'shelf'


class PaymongoScraper(LeverScraper):
    employer_name = 'PayMongo'
    EMPLOYER_KEY = 'paymongo'


class TekionScraper(GreenhouseScraper):
    employer_name = 'Tekion'
    EMPLOYER_KEY = 'tekion'


class AlchemyScraper(GreenhouseScraper):
    employer_name = 'Alchemy'
    EMPLOYER_KEY = 'alchemy'


class AxiosScraper(GreenhouseScraper):
    employer_name = 'Axios'
    EMPLOYER_KEY = 'axios'


class GrailScraper(LeverScraper):
    employer_name = 'GRAIL'
    EMPLOYER_KEY = 'grailbio'


class RippleScraper(GreenhouseApiScraper):
    employer_name = 'Ripple'
    EMPLOYER_KEY = 'ripple'


class CandidlyScraper(GreenhouseScraper):
    employer_name = 'Candidly'
    EMPLOYER_KEY = 'candidly'


class OzowScraper(GreenhouseScraper):
    employer_name = 'Ozow'
    EMPLOYER_KEY = 'ozow'


class LatticeScraper(GreenhouseApiScraper):
    employer_name = 'Lattice'
    EMPLOYER_KEY = 'lattice'


class KnakScraper(GreenhouseApiScraper):
    employer_name = 'Knak'
    EMPLOYER_KEY = 'knak'


class DuolingoScraper(GreenhouseScraper):
    employer_name = 'Duolingo'
    EMPLOYER_KEY = 'duolingo'


class EvertrueScraper(GreenhouseApiScraper):
    employer_name = 'EverTrue'
    EMPLOYER_KEY = 'evertrue'


class LandingaiScraper(LeverScraper):
    employer_name = 'LandingAI'
    EMPLOYER_KEY = 'landing'


class EcoreScraper(GreenhouseScraper):
    employer_name = 'e-core'
    EMPLOYER_KEY = 'ecore'


class PostmanScraper(GreenhouseScraper):
    employer_name = 'Postman'
    EMPLOYER_KEY = 'postman'


class JobberScraper(GreenhouseScraper):
    employer_name = 'Jobber'
    EMPLOYER_KEY = 'jobber'


class GleanScraper(GreenhouseScraper):
    employer_name = 'Glean'
    EMPLOYER_KEY = 'gleanwork'


class MozillaScraper(GreenhouseScraper):
    employer_name = 'Mozilla'
    EMPLOYER_KEY = 'mozilla'


class RobloxScraper(GreenhouseApiScraper):
    employer_name = 'Roblox'
    EMPLOYER_KEY = 'roblox'


class EvolutioniqScraper(GreenhouseApiScraper):
    employer_name = 'EvolutionIQ'
    EMPLOYER_KEY = 'evolutioniq'


class HologramScraper(GreenhouseScraper):
    employer_name = 'Hologram'
    EMPLOYER_KEY = 'hologram'


class ClickupScraper(GreenhouseScraper):
    employer_name = 'ClickUp'
    EMPLOYER_KEY = 'clickup'


class SparrowScraper(GreenhouseScraper):
    employer_name = 'Sparrow'
    EMPLOYER_KEY = 'sparrow'


class WorkivaScraper(WorkdayScraper):
    employer_name = 'Workiva'
    start_url = 'https://workiva.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class RecoraScraper(GreenhouseScraper):
    employer_name = 'Recora'
    EMPLOYER_KEY = 'recorainc'


class MasterclassScraper(GreenhouseApiScraper):
    employer_name = 'Masterclass'
    EMPLOYER_KEY = 'masterclass'


class VendrScraper(GreenhouseScraper):
    employer_name = 'Vendr'
    EMPLOYER_KEY = 'vendr'


class OriginScraper(GreenhouseApiScraper):
    employer_name = 'Origin'
    EMPLOYER_KEY = 'originfinancial'


class LandisScraper(GreenhouseApiScraper):
    employer_name = 'Landis'
    EMPLOYER_KEY = 'landis'


class StellateScraper(GreenhouseScraper):
    employer_name = 'Stellate'
    EMPLOYER_KEY = 'stellate'


class RocketreachScraper(GreenhouseScraper):
    employer_name = 'RocketReach'
    EMPLOYER_KEY = 'rocketreach'


class ScaleScraper(GreenhouseScraper):
    employer_name = 'Scale'
    EMPLOYER_KEY = 'scaleai'


class RedisLabsScraper(GreenhouseApiScraper):
    employer_name = 'Redis Labs'
    EMPLOYER_KEY = 'redislabs'


class NarvarScraper(GreenhouseScraper):
    employer_name = 'Narvar'
    EMPLOYER_KEY = 'narvar'


class MethodScraper(GreenhouseScraper):
    employer_name = 'Method'
    EMPLOYER_KEY = 'method'


class HumaScraper(LeverScraper):
    employer_name = 'Huma'
    EMPLOYER_KEY = 'huma'


class N26Scraper(GreenhouseApiScraper):
    employer_name = 'N26'
    EMPLOYER_KEY = 'n26'


class CodecademyScraper(GreenhouseApiScraper):
    employer_name = 'Codecademy'
    EMPLOYER_KEY = 'codeacademy'


class BuilderAiScraper(WorkableScraper):
    employer_name = 'Builder.ai'
    EMPLOYER_KEY = 'builderai'


class FocalScraper(GreenhouseScraper):
    employer_name = 'Focal'
    EMPLOYER_KEY = 'focalsystems'


class PatreonScraper(GreenhouseScraper):
    employer_name = 'Patreon'
    EMPLOYER_KEY = 'patreon'


class NextdoorScraper(GreenhouseApiScraper):
    employer_name = 'Nextdoor'
    EMPLOYER_KEY = 'nextdoor'


class ShipbobScraper(GreenhouseScraper):
    employer_name = 'ShipBob'
    EMPLOYER_KEY = 'shipbobinc'


class NumeradeScraper(GreenhouseApiScraper):
    employer_name = 'Numerade'
    EMPLOYER_KEY = 'numeradecareers'


class VedaScraper(LeverScraper):
    employer_name = 'Veda'
    EMPLOYER_KEY = 'vedadata'


class HomeboundScraper(GreenhouseScraper):
    employer_name = 'Homebound'
    EMPLOYER_KEY = 'homebound'


class AtBayScraper(GreenhouseScraper):
    employer_name = 'At-Bay'
    EMPLOYER_KEY = 'atbayjobs'


class PayoneerScraper(GreenhouseApiScraper):
    employer_name = 'Payoneer'
    EMPLOYER_KEY = 'payoneer'


class AlgoliaScraper(GreenhouseScraper):
    employer_name = 'Algolia'
    EMPLOYER_KEY = 'algolia'


class HowlScraper(GreenhouseScraper):
    employer_name = 'Howl'
    EMPLOYER_KEY = 'howl'


class PursuitScraper(GreenhouseScraper):
    employer_name = 'Pursuit'
    EMPLOYER_KEY = 'pursuit'


class AirslateScraper(LeverScraper):
    employer_name = 'airSlate'
    EMPLOYER_KEY = 'airslate'


class LulaScraper(GreenhouseScraper):
    employer_name = 'Lula'
    EMPLOYER_KEY = 'lula'


class CamundaScraper(GreenhouseApiScraper):
    employer_name = 'Camunda'
    EMPLOYER_KEY = 'camundaservices'


class EfisheryScraper(GreenhouseScraper):
    employer_name = 'eFishery'
    EMPLOYER_KEY = 'efishery'
    
    def process_location_text(self, location_text):
        locations = super().process_location_text(location_text)
        new_locations = []
        for location in locations:
            if 'anywhere' in location.lower():
                location = 'Remote'
            elif 'office' in location.lower():
                location = 'Cimenyan, Indonesia'
            new_locations.append(location)
        return new_locations


class CleverScraper(GreenhouseApiScraper):
    employer_name = 'Clever'
    EMPLOYER_KEY = 'clever'


class AccelbyteScraper(GreenhouseApiScraper):
    employer_name = 'AccelByte'
    EMPLOYER_KEY = 'accelbyte'


class RidgelineScraper(GreenhouseApiScraper):
    employer_name = 'Ridgeline'
    EMPLOYER_KEY = 'ridgeline'


class ApiiroScraper(GreenhouseApiScraper):
    employer_name = 'Apiiro'
    EMPLOYER_KEY = 'apiiro'


class GateIoScraper(LeverScraper):
    employer_name = 'Gate.io'
    EMPLOYER_KEY = 'gate.io'


class ViaScraper(GreenhouseScraper):
    employer_name = 'Via'
    EMPLOYER_KEY = 'via'


class MomentiveScraper(GreenhouseScraper):
    employer_name = 'Momentive'
    EMPLOYER_KEY = 'surveymonkey'


class GlobalPaymentsScraper(WorkdayScraper):
    employer_name = 'Global Payments'
    start_url = 'https://tsys.wd1.myworkdayjobs.com/en-US/TSYS/'
    has_job_departments = False


class BubbleScraper(GreenhouseScraper):
    employer_name = 'Bubble'
    EMPLOYER_KEY = 'bubble'


class MatterLabsScraper(LeverScraper):
    employer_name = 'Matter Labs'
    EMPLOYER_KEY = 'matterlabs'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class GenDigitalScraper(WorkdayScraper):
    employer_name = 'Gen Digital'
    start_url = 'https://gen.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class BitwardenScraper(GreenhouseApiScraper):
    employer_name = 'Bitwarden'
    EMPLOYER_KEY = 'bitwarden'


class SuperComScraper(LeverScraper):
    employer_name = 'Super.com'
    EMPLOYER_KEY = 'super-com'


class MatchGroupScraper(LeverScraper):
    employer_name = 'Match Group'
    EMPLOYER_KEY = 'matchgroup'


class BondFinancialScraper(GreenhouseScraper):
    employer_name = 'Bond Financial'
    EMPLOYER_KEY = 'bondfinancialtechnologies'


class BlackbirdAiScraper(WorkableScraper):
    employer_name = 'Blackbird AI'
    EMPLOYER_KEY = 'blackbirdai'


class FairmatScraper(LeverScraper):
    employer_name = 'Fairmat'
    EMPLOYER_KEY = 'Fairmat'


class TencentScraper(WorkdayScraper):
    employer_name = 'Tencent'
    start_url = 'https://tencent.wd1.myworkdayjobs.com/en-US/Tencent_Careers/'
    has_job_departments = False


class PineconeScraper(GreenhouseApiScraper):
    employer_name = 'Pinecone'
    EMPLOYER_KEY = 'hypercube'


class WeaveScraper(GreenhouseScraper):
    employer_name = 'Weave'
    EMPLOYER_KEY = 'weavehq'


class BrilliantScraper(LeverScraper):
    employer_name = 'Brilliant'
    EMPLOYER_KEY = 'brilliant'


class DuneAnalyticsScraper(AshbyHQScraper):
    employer_name = 'Dune Analytics'
    EMPLOYER_KEY = 'dune'


class Q2HoldingsScraper(WorkdayScraper):
    employer_name = 'Q2 Holdings'
    start_url = 'https://q2ebanking.wd5.myworkdayjobs.com/en-US/Q2/'
    has_job_departments = False


class UnitScraper(AshbyHQScraper):
    employer_name = 'Unit'
    EMPLOYER_KEY = 'unit'


class PanoramaScraper(GreenhouseScraper):
    employer_name = 'Panorama'
    EMPLOYER_KEY = 'panoramaed'


class InflectionAiScraper(GreenhouseScraper):
    employer_name = 'Inflection AI'
    EMPLOYER_KEY = 'inflectionai'


class ArizeAiScraper(GreenhouseScraper):
    employer_name = 'Arize AI'
    EMPLOYER_KEY = 'arizeai'


class FairmarkitScraper(GreenhouseApiScraper):
    employer_name = 'Fairmarkit'
    EMPLOYER_KEY = 'fairmarkit'


class StellarScraper(GreenhouseScraper):
    employer_name = 'Stellar'
    EMPLOYER_KEY = 'stellar'


class VirtruScraper(GreenhouseScraper):
    employer_name = 'Virtru'
    EMPLOYER_KEY = 'virtru'


class AsteraLabsScraper(GreenhouseScraper):
    employer_name = 'Astera Labs'
    EMPLOYER_KEY = 'asteralabs'


class FloScraper(GreenhouseScraper):
    employer_name = 'Flo'
    EMPLOYER_KEY = 'flohealth'


class InstaworkScraper(GreenhouseScraper):
    employer_name = 'Instawork'
    EMPLOYER_KEY = 'instawork'


class BankedScraper(GreenhouseScraper):
    employer_name = 'Banked'
    EMPLOYER_KEY = 'banked'


class WellthScraper(GreenhouseScraper):
    employer_name = 'Wellth'
    EMPLOYER_KEY = 'wellth'


class TwilioScraper(GreenhouseScraper):
    employer_name = 'Twilio'
    EMPLOYER_KEY = 'twilio'


class AgoricScraper(GreenhouseApiScraper):
    employer_name = 'Agoric'
    EMPLOYER_KEY = 'agoric'


class TigergraphScraper(GreenhouseScraper):
    employer_name = 'TigerGraph'
    EMPLOYER_KEY = 'tigergraph'


class EnteraScraper(GreenhouseScraper):
    employer_name = 'Entera'
    EMPLOYER_KEY = 'entera'


class DexterityScraper(LeverScraper):
    employer_name = 'Dexterity'
    EMPLOYER_KEY = 'dexterity'


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
    SuperComScraper.employer_name: SuperComScraper,
    PineconeScraper.employer_name: PineconeScraper,
    AgoricScraper.employer_name: AgoricScraper,
    TigergraphScraper.employer_name: TigergraphScraper,
    EnteraScraper.employer_name: EnteraScraper,
    DexterityScraper.employer_name: DexterityScraper,
    WeaveScraper.employer_name: WeaveScraper,
    BrilliantScraper.employer_name: BrilliantScraper,
    DuneAnalyticsScraper.employer_name: DuneAnalyticsScraper,
    Q2HoldingsScraper.employer_name: Q2HoldingsScraper,
    UnitScraper.employer_name: UnitScraper,
    PanoramaScraper.employer_name: PanoramaScraper,
    InflectionAiScraper.employer_name: InflectionAiScraper,
    ArizeAiScraper.employer_name: ArizeAiScraper,
    FairmarkitScraper.employer_name: FairmarkitScraper,
    StellarScraper.employer_name: StellarScraper,
    VirtruScraper.employer_name: VirtruScraper,
    AsteraLabsScraper.employer_name: AsteraLabsScraper,
    FloScraper.employer_name: FloScraper,
    InstaworkScraper.employer_name: InstaworkScraper,
    BankedScraper.employer_name: BankedScraper,
    WellthScraper.employer_name: WellthScraper,
    TwilioScraper.employer_name: TwilioScraper,
    TencentScraper.employer_name: TencentScraper,
    MatchGroupScraper.employer_name: MatchGroupScraper,
    BondFinancialScraper.employer_name: BondFinancialScraper,
    BlackbirdAiScraper.employer_name: BlackbirdAiScraper,
    FairmatScraper.employer_name: FairmatScraper,
    GenDigitalScraper.employer_name: GenDigitalScraper,
    BitwardenScraper.employer_name: BitwardenScraper,
    ApiiroScraper.employer_name: ApiiroScraper,
    GateIoScraper.employer_name: GateIoScraper,
    MatterLabsScraper.employer_name: MatterLabsScraper,
    CodecademyScraper.employer_name: CodecademyScraper,
    NumeradeScraper.employer_name: NumeradeScraper,
    CamundaScraper.employer_name: CamundaScraper,
    EfisheryScraper.employer_name: EfisheryScraper,
    CleverScraper.employer_name: CleverScraper,
    RidgelineScraper.employer_name: RidgelineScraper,
    ViaScraper.employer_name: ViaScraper,
    MomentiveScraper.employer_name: MomentiveScraper,
    GlobalPaymentsScraper.employer_name: GlobalPaymentsScraper,
    BubbleScraper.employer_name: BubbleScraper,
    AccelbyteScraper.employer_name: AccelbyteScraper,
    VedaScraper.employer_name: VedaScraper,
    HomeboundScraper.employer_name: HomeboundScraper,
    AtBayScraper.employer_name: AtBayScraper,
    PayoneerScraper.employer_name: PayoneerScraper,
    AlgoliaScraper.employer_name: AlgoliaScraper,
    HowlScraper.employer_name: HowlScraper,
    PursuitScraper.employer_name: PursuitScraper,
    AirslateScraper.employer_name: AirslateScraper,
    LulaScraper.employer_name: LulaScraper,
    FocalScraper.employer_name: FocalScraper,
    PatreonScraper.employer_name: PatreonScraper,
    NextdoorScraper.employer_name: NextdoorScraper,
    ShipbobScraper.employer_name: ShipbobScraper,
    BuilderAiScraper.employer_name: BuilderAiScraper,
    N26Scraper.employer_name: N26Scraper,
    KnakScraper.employer_name: KnakScraper,
    OriginScraper.employer_name: OriginScraper,
    LandisScraper.employer_name: LandisScraper,
    StellateScraper.employer_name: StellateScraper,
    RocketreachScraper.employer_name: RocketreachScraper,
    ScaleScraper.employer_name: ScaleScraper,
    RedisLabsScraper.employer_name: RedisLabsScraper,
    NarvarScraper.employer_name: NarvarScraper,
    MethodScraper.employer_name: MethodScraper,
    HumaScraper.employer_name: HumaScraper,
    DuolingoScraper.employer_name: DuolingoScraper,
    EvertrueScraper.employer_name: EvertrueScraper,
    LandingaiScraper.employer_name: LandingaiScraper,
    EcoreScraper.employer_name: EcoreScraper,
    PostmanScraper.employer_name: PostmanScraper,
    JobberScraper.employer_name: JobberScraper,
    GleanScraper.employer_name: GleanScraper,
    MozillaScraper.employer_name: MozillaScraper,
    RobloxScraper.employer_name: RobloxScraper,
    EvolutioniqScraper.employer_name: EvolutioniqScraper,
    HologramScraper.employer_name: HologramScraper,
    ClickupScraper.employer_name: ClickupScraper,
    SparrowScraper.employer_name: SparrowScraper,
    WorkivaScraper.employer_name: WorkivaScraper,
    RecoraScraper.employer_name: RecoraScraper,
    MasterclassScraper.employer_name: MasterclassScraper,
    VendrScraper.employer_name: VendrScraper,
    TekionScraper.employer_name: TekionScraper,
    AlchemyScraper.employer_name: AlchemyScraper,
    AxiosScraper.employer_name: AxiosScraper,
    GrailScraper.employer_name: GrailScraper,
    RippleScraper.employer_name: RippleScraper,
    CandidlyScraper.employer_name: CandidlyScraper,
    OzowScraper.employer_name: OzowScraper,
    LatticeScraper.employer_name: LatticeScraper,
    TigeraScraper.employer_name: TigeraScraper,
    MobileyeScraper.employer_name: MobileyeScraper,
    PreplyScraper.employer_name: PreplyScraper,
    ShelfIoScraper.employer_name: ShelfIoScraper,
    PaymongoScraper.employer_name: PaymongoScraper,
    VectraAiScraper.employer_name: VectraAiScraper,
    IncortaScraper.employer_name: IncortaScraper,
    PeakAiScraper.employer_name: PeakAiScraper,
    SinchScraper.employer_name: SinchScraper,
    PitchbookScraper.employer_name: PitchbookScraper,
    QuintoandarScraper.employer_name: QuintoandarScraper,
    DlocalScraper.employer_name: DlocalScraper,
    MeritScraper.employer_name: MeritScraper,
    LaceworkScraper.employer_name: LaceworkScraper,
    ApolloIoScraper.employer_name: ApolloIoScraper,
    ExpediaScraper.employer_name: ExpediaScraper,
    KlookScraper.employer_name: KlookScraper,
    RingcentralScraper.employer_name: RingcentralScraper,
    BoxScraper.employer_name: BoxScraper,
    UpguardScraper.employer_name: UpguardScraper,
    TrendMicroScraper.employer_name: TrendMicroScraper,
    Auto1GroupScraper.employer_name: Auto1GroupScraper,
    PandadocScraper.employer_name: PandadocScraper,
    TruliooScraper.employer_name: TruliooScraper,
    PersonaScraper.employer_name: PersonaScraper,
    NinefinScraper.employer_name: NinefinScraper,
    LumafieldScraper.employer_name: LumafieldScraper,
    FisScraper.employer_name: FisScraper,
    SmartlyScraper.employer_name: SmartlyScraper,
    BrazeScraper.employer_name: BrazeScraper,
    TheHutGroupScraper.employer_name: TheHutGroupScraper,
    SamsaraScraper.employer_name: SamsaraScraper,
    WrapbookScraper.employer_name: WrapbookScraper,
    ZoneAndCoScraper.employer_name: ZoneAndCoScraper,
    GwiScraper.employer_name: GwiScraper,
    QualysScraper.employer_name: QualysScraper,
    Three60learningScraper.employer_name: Three60learningScraper,
    GrouponScraper.employer_name: GrouponScraper,
    FiservScraper.employer_name: FiservScraper,
    AspentechScraper.employer_name: AspentechScraper,
    Cars24Scraper.employer_name: Cars24Scraper,
    HazelHealthScraper.employer_name: HazelHealthScraper,
    QumuloScraper.employer_name: QumuloScraper,
    BlinkistScraper.employer_name: BlinkistScraper,
    JamfScraper.employer_name: JamfScraper,
    LiquibaseScraper.employer_name: LiquibaseScraper,
    GlintsScraper.employer_name: GlintsScraper,
    MudflapScraper.employer_name: MudflapScraper,
    BabylonHealthScraper.employer_name: BabylonHealthScraper,
    KlueScraper.employer_name: KlueScraper,
    AstranisScraper.employer_name: AstranisScraper,
    OmnipresentScraper.employer_name: OmnipresentScraper,
    TemplafyScraper.employer_name: TemplafyScraper,
    OutbrainScraper.employer_name: OutbrainScraper,
    AssembledScraper.employer_name: AssembledScraper,
    NiumScraper.employer_name: NiumScraper,
    AcronisScraper.employer_name: AcronisScraper,
    SamsungScraper.employer_name: SamsungScraper,
    SleeperScraper.employer_name: SleeperScraper,
    SalesforceScraper.employer_name: SalesforceScraper,
    LetsDoThisScraper.employer_name: LetsDoThisScraper,
    VestiaireScraper.employer_name: VestiaireScraper,
    RewindSoftwareScraper.employer_name: RewindSoftwareScraper,
    VannevarLabsScraper.employer_name: VannevarLabsScraper,
    IvaluaScraper.employer_name: IvaluaScraper,
    GeniusSportsScraper.employer_name: GeniusSportsScraper,
    LyraHealthScraper.employer_name: LyraHealthScraper,
    ImmersiveLabsScraper.employer_name: ImmersiveLabsScraper,
    HealthjoyScraper.employer_name: HealthjoyScraper,
    AiseraScraper.employer_name: AiseraScraper,
    SolarwindsScraper.employer_name: SolarwindsScraper,
    FreenowScraper.employer_name: FreenowScraper,
    WebflowScraper.employer_name: WebflowScraper,
    BeyondtrustScraper.employer_name: BeyondtrustScraper,
    TwoUScraper.employer_name: TwoUScraper,
    TaboolaScraper.employer_name: TaboolaScraper,
    FivetranScraper.employer_name: FivetranScraper,
    DruvaScraper.employer_name: DruvaScraper,
    RechargeScraper.employer_name: RechargeScraper,
    ZipScraper.employer_name: ZipScraper,
    AristaNetworksScraper.employer_name: AristaNetworksScraper,
    BeaconScraper.employer_name: BeaconScraper,
    WorkstreamScraper.employer_name: WorkstreamScraper,
    FireblocksScraper.employer_name: FireblocksScraper,
    FubotvScraper.employer_name: FubotvScraper,
    SimilarwebScraper.employer_name: SimilarwebScraper,
    DellScraper.employer_name: DellScraper,
    TideScraper.employer_name: TideScraper,
    KlaScraper.employer_name: KlaScraper,
    LodgifyScraper.employer_name: LodgifyScraper,
    KlaviyoScraper.employer_name: KlaviyoScraper,
    TrivagoScraper.employer_name: TrivagoScraper,
    FreshworksScraper.employer_name: FreshworksScraper,
    CartoScraper.employer_name: CartoScraper,
    HippoScraper.employer_name: HippoScraper,
    ToriiScraper.employer_name: ToriiScraper,
    AtmosphereTvScraper.employer_name: AtmosphereTvScraper,
    StarlingBankScraper.employer_name: StarlingBankScraper,
    CrusoeEnergyScraper.employer_name: CrusoeEnergyScraper,
    NuvemshopScraper.employer_name: NuvemshopScraper,
    HumanInterestScraper.employer_name: HumanInterestScraper,
    CohesityScraper.employer_name: CohesityScraper,
    SevenshiftsScraper.employer_name: SevenshiftsScraper,
    ImpossibleFoodsScraper.employer_name: ImpossibleFoodsScraper,
    AkqaScraper.employer_name: AkqaScraper,
    DiligentRoboticsScraper.employer_name: DiligentRoboticsScraper,
    TealiumScraper.employer_name: TealiumScraper,
    NetskopeScraper.employer_name: NetskopeScraper,
    BackbaseScraper.employer_name: BackbaseScraper,
    AnalogDevicesScraper.employer_name: AnalogDevicesScraper,
    FormaScraper.employer_name: FormaScraper,
    GlorifyScraper.employer_name: GlorifyScraper,
    MytrafficScraper.employer_name: MytrafficScraper,
    CharlesScraper.employer_name: CharlesScraper,
    SpotifyScraper.employer_name: SpotifyScraper,
    ZoominfoScraper.employer_name: ZoominfoScraper,
    BenchlingScraper.employer_name: BenchlingScraper,
    XentralScraper.employer_name: XentralScraper,
    AppliedIntuitionScraper.employer_name: AppliedIntuitionScraper,
    NavanScraper.employer_name: NavanScraper,
    HeyjobsScraper.employer_name: HeyjobsScraper,
    ElevateK12Scraper.employer_name: ElevateK12Scraper,
    HumuScraper.employer_name: HumuScraper,
    PleoScraper.employer_name: PleoScraper,
    WonoloScraper.employer_name: WonoloScraper,
    GitlabScraper.employer_name: GitlabScraper,
    WooScraper.employer_name: WooScraper,
    OpengovScraper.employer_name: OpengovScraper,
    OnesignalScraper.employer_name: OnesignalScraper,
    KeeperSecurityScraper.employer_name: KeeperSecurityScraper,
    HarnessScraper.employer_name: HarnessScraper,
    TaxfyleScraper.employer_name: TaxfyleScraper,
    TiltingPointScraper.employer_name: TiltingPointScraper,
    HivebriteScraper.employer_name: HivebriteScraper,
    GohenryScraper.employer_name: GohenryScraper,
    SmsAssistScraper.employer_name: SmsAssistScraper,
    SkyflowScraper.employer_name: SkyflowScraper,
    CoupangScraper.employer_name: CoupangScraper,
    SuperpedestrianScraper.employer_name: SuperpedestrianScraper,
    DeliverooScraper.employer_name: DeliverooScraper,
    GrafanaScraper.employer_name: GrafanaScraper,
    OrcaSecurityScraper.employer_name: OrcaSecurityScraper,
    TrustlyScraper.employer_name: TrustlyScraper,
    SylveraScraper.employer_name: SylveraScraper,
    DocplannerScraper.employer_name: DocplannerScraper,
    TealbookScraper.employer_name: TealbookScraper,
    TalkdeskScraper.employer_name: TalkdeskScraper,
    MosaicScraper.employer_name: MosaicScraper,
    ForwardNetworksScraper.employer_name: ForwardNetworksScraper,
    YapilyScraper.employer_name: YapilyScraper,
    HubspotScraper.employer_name: HubspotScraper,
    TeyaScraper.employer_name: TeyaScraper,
    AivenScraper.employer_name: AivenScraper,
    CelonisScraper.employer_name: CelonisScraper,
    VoxMediaScraper.employer_name: VoxMediaScraper,
    TrengoScraper.employer_name: TrengoScraper,
    DataikuScraper.employer_name: DataikuScraper,
    CrowdstrikeScraper.employer_name: CrowdstrikeScraper,
    CartaScraper.employer_name: CartaScraper,
    PachamaScraper.employer_name: PachamaScraper,
    ForterScraper.employer_name: ForterScraper,
    WizScraper.employer_name: WizScraper,
    PomeloCareScraper.employer_name: PomeloCareScraper,
    AirwallexScraper.employer_name: AirwallexScraper,
    SoloIoScraper.employer_name: SoloIoScraper,
    CanvaScraper.employer_name: CanvaScraper,
    ParabolaScraper.employer_name: ParabolaScraper,
    BinanceScraper.employer_name: BinanceScraper,
    CompanycamScraper.employer_name: CompanycamScraper,
    PayhawkScraper.employer_name: PayhawkScraper,
    ChocoScraper.employer_name: ChocoScraper,
    ClearbitScraper.employer_name: ClearbitScraper,
    CazooScraper.employer_name: CazooScraper,
    XeroScraper.employer_name: XeroScraper,
    CybereasonScraper.employer_name: CybereasonScraper,
    CarvanaScraper.employer_name: CarvanaScraper,
    AltruistiqScraper.employer_name: AltruistiqScraper,
    UpworkScraper.employer_name: UpworkScraper,
    Dream11Scraper.employer_name: Dream11Scraper,
    PubnubScraper.employer_name: PubnubScraper,
    PaltaScraper.employer_name: PaltaScraper,
    CostarGroupScraper.employer_name: CostarGroupScraper,
    SnykScraper.employer_name: SnykScraper,
    RelativityScraper.employer_name: RelativityScraper,
    BitgetScraper.employer_name: BitgetScraper,
    EngagesmartScraper.employer_name: EngagesmartScraper,
    DoctolibScraper.employer_name: DoctolibScraper,
    RazorGroupScraper.employer_name: RazorGroupScraper,
    ConstellationScraper.employer_name: ConstellationScraper,
    BettermentScraper.employer_name: BettermentScraper,
    IntappScraper.employer_name: IntappScraper,
    VuoriScraper.employer_name: VuoriScraper,
    OcrolusScraper.employer_name: OcrolusScraper,
    TwoKScraper.employer_name: TwoKScraper,
    PaypalScraper.employer_name: PaypalScraper,
    GohealthScraper.employer_name: GohealthScraper,
    HealthverityScraper.employer_name: HealthverityScraper,
    RokuScraper.employer_name: RokuScraper,
    CleoScraper.employer_name: CleoScraper,
    ToastScraper.employer_name: ToastScraper,
    TovalaScraper.employer_name: TovalaScraper,
    FarfetchScraper.employer_name: FarfetchScraper,
    ClearcoverScraper.employer_name: ClearcoverScraper,
    WayfairScraper.employer_name: WayfairScraper,
    AppsflyerScraper.employer_name: AppsflyerScraper,
    PelotonScraper.employer_name: PelotonScraper,
    OscarHealthScraper.employer_name: OscarHealthScraper,
    SeismicScraper.employer_name: SeismicScraper,
    RyeScraper.employer_name: RyeScraper,
    MaxarScraper.employer_name: MaxarScraper,
    ChargepointScraper.employer_name: ChargepointScraper,
    IrobotScraper.employer_name: IrobotScraper,
    PismoScraper.employer_name: PismoScraper,
    RocketLabScraper.employer_name: RocketLabScraper,
    UnitedmastersScraper.employer_name: UnitedmastersScraper,
    JoorScraper.employer_name: JoorScraper,
    TheFarmersDogScraper.employer_name: TheFarmersDogScraper,
    MoonpigScraper.employer_name: MoonpigScraper,
    JeevesScraper.employer_name: JeevesScraper,
    CakeDefiScraper.employer_name: CakeDefiScraper,
    ViantScraper.employer_name: ViantScraper,
    OptimoveScraper.employer_name: OptimoveScraper,
    HikeScraper.employer_name: HikeScraper,
    GlobalfoundriesScraper.employer_name: GlobalfoundriesScraper,
    TenXGenomicsScraper.employer_name: TenXGenomicsScraper,
    FeaturespaceScraper.employer_name: FeaturespaceScraper,
    CompassScraper.employer_name: CompassScraper,
    TrimbleScraper.employer_name: TrimbleScraper,
    LaunchdarklyScraper.employer_name: LaunchdarklyScraper,
    SwordHealthScraper.employer_name: SwordHealthScraper,
    BranchScraper.employer_name: BranchScraper,
    WoltScraper.employer_name: WoltScraper,
    MonzoScraper.employer_name: MonzoScraper,
    EbanxScraper.employer_name: EbanxScraper,
    TrustpilotScraper.employer_name: TrustpilotScraper,
    IntelScraper.employer_name: IntelScraper,
    ImagenScraper.employer_name: ImagenScraper,
    AbcFitnessScraper.employer_name: AbcFitnessScraper,
    ZetaGlobalScraper.employer_name: ZetaGlobalScraper,
    SesoScraper.employer_name: SesoScraper,
    WallapopScraper.employer_name: WallapopScraper,
    OvertimeScraper.employer_name: OvertimeScraper,
    DexcareScraper.employer_name: DexcareScraper,
    SeatgeekScraper.employer_name: SeatgeekScraper,
    FormlabsScraper.employer_name: FormlabsScraper,
    TravelokaScraper.employer_name: TravelokaScraper,
    ElevatebioScraper.employer_name: ElevatebioScraper,
    CambridgeMobileScraper.employer_name: CambridgeMobileScraper,
    FrubanaScraper.employer_name: FrubanaScraper,
    OloScraper.employer_name: OloScraper,
    ThescoreScraper.employer_name: ThescoreScraper,
    DatabricksScraper.employer_name: DatabricksScraper,
    X1Scraper.employer_name: X1Scraper,
    TridgeScraper.employer_name: TridgeScraper,
    AntlerScraper.employer_name: AntlerScraper,
    ElasticScraper.employer_name: ElasticScraper,
    DatadogScraper.employer_name: DatadogScraper,
    IncodeTechnologiesScraper.employer_name: IncodeTechnologiesScraper,
    SprinklrScraper.employer_name: SprinklrScraper,
    XepelinScraper.employer_name: XepelinScraper,
    GympassScraper.employer_name: GympassScraper,
    ArrayScraper.employer_name: ArrayScraper,
    F5Scraper.employer_name: F5Scraper,
    InmobiScraper.employer_name: InmobiScraper,
    QuantstampScraper.employer_name: QuantstampScraper,
    ScalableCapitalScraper.employer_name: ScalableCapitalScraper,
    UnybrandsScraper.employer_name: UnybrandsScraper,
    BerlinBrandsGroupScraper.employer_name: BerlinBrandsGroupScraper,
    PointclickcareScraper.employer_name: PointclickcareScraper,
    FanduelScraper.employer_name: FanduelScraper,
    BlockScraper.employer_name: BlockScraper,
    PaytmScraper.employer_name: PaytmScraper,
    TripadvisorScraper.employer_name: TripadvisorScraper,
    AmadeusScraper.employer_name: AmadeusScraper,
    CrossRiverBankScraper.employer_name: CrossRiverBankScraper,
    DaznScraper.employer_name: DaznScraper,
    LtkScraper.employer_name: LtkScraper,
    AdobeScraper.employer_name: AdobeScraper,
    ReltioScraper.employer_name: ReltioScraper,
    ShopmonkeyScraper.employer_name: ShopmonkeyScraper,
    AccentureScraper.employer_name: AccentureScraper,
    RappiScraper.employer_name: RappiScraper,
    Project44Scraper.employer_name: Project44Scraper,
    PlaytechScraper.employer_name: PlaytechScraper,
    IovLabsScraper.employer_name: IovLabsScraper,
    SumupScraper.employer_name: SumupScraper,
    ZellerScraper.employer_name: ZellerScraper,
    PecanAiScraper.employer_name: PecanAiScraper,
    AllegroScraper.employer_name: AllegroScraper,
    ZyngaScraper.employer_name: ZyngaScraper,
    WorkatoScraper.employer_name: WorkatoScraper,
    IconiqScraper.employer_name: IconiqScraper,
    FlutterEntertainmentScraper.employer_name: FlutterEntertainmentScraper,
    DeelScraper.employer_name: DeelScraper,
    HingeHealthScraper.employer_name: HingeHealthScraper,
    TokenMetricsScraper.employer_name: TokenMetricsScraper,
    AltoScraper.employer_name: AltoScraper,
    SentineloneScraper.employer_name: SentineloneScraper,
    QuantexaScraper.employer_name: QuantexaScraper,
    TetrascienceScraper.employer_name: TetrascienceScraper,
    SportradarScraper.employer_name: SportradarScraper,
    NxpSemiScraper.employer_name: NxpSemiScraper,
    GrabScraper.employer_name: GrabScraper,
    SaviyntScraper.employer_name: SaviyntScraper,
    MarshmallowScraper.employer_name: MarshmallowScraper,
    ArchiproScraper.employer_name: ArchiproScraper,
    OneMedicalScraper.employer_name: OneMedicalScraper,
    DeliveryHeroScraper.employer_name: DeliveryHeroScraper,
    OpenxScraper.employer_name: OpenxScraper,
    CheckoutScraper.employer_name: CheckoutScraper,
    AdyenScraper.employer_name: AdyenScraper,
    PaloAltoNetworksScraper.employer_name: PaloAltoNetworksScraper,
    BackMarketScraper.employer_name: BackMarketScraper,
    BynderScraper.employer_name: BynderScraper,
    PaytrixScraper.employer_name: PaytrixScraper,
    CybercubeScraper.employer_name: CybercubeScraper,
    ArkoseLabsScraper.employer_name: ArkoseLabsScraper,
    GotoScraper.employer_name: GotoScraper,
    NubankScraper.employer_name: NubankScraper,
    GostudentScraper.employer_name: GostudentScraper,
    ExpressvpnScraper.employer_name: ExpressvpnScraper,
    CareemScraper.employer_name: CareemScraper,
    UsertestingScraper.employer_name: UsertestingScraper,
    TsImagineScraper.employer_name: TsImagineScraper,
    BluevineScraper.employer_name: BluevineScraper,
    AgodaScraper.employer_name: AgodaScraper,
    PeekScraper.employer_name: PeekScraper,
    LevadataScraper.employer_name: LevadataScraper,
    MedallionScraper.employer_name: MedallionScraper,
    AvaloqGroupScraper.employer_name: AvaloqGroupScraper,
    OcadoScraper.employer_name: OcadoScraper,
    AdevintaScraper.employer_name: AdevintaScraper,
    TipaltiScraper.employer_name: TipaltiScraper,
    FoodpandaScraper.employer_name: FoodpandaScraper,
    RiotGamesScraper.employer_name: RiotGamesScraper,
    ChewyScraper.employer_name: ChewyScraper,
    ThunesScraper.employer_name: ThunesScraper,
    CompstakScraper.employer_name: CompstakScraper,
    GopuffScraper.employer_name: GopuffScraper,
    CredScraper.employer_name: CredScraper,
    AstSpacemobileScraper.employer_name: AstSpacemobileScraper,
    TakealotScraper.employer_name: TakealotScraper,
    SpacexScraper.employer_name: SpacexScraper,
    JaneStreetScraper.employer_name: JaneStreetScraper,
    GetsafeScraper.employer_name: GetsafeScraper,
    ZscalerScraper.employer_name: ZscalerScraper,
    Point72Scraper.employer_name: Point72Scraper,
    MessariScraper.employer_name: MessariScraper,
    NextInsuranceScraper.employer_name: NextInsuranceScraper,
    ModulrScraper.employer_name: ModulrScraper,
    HudsonRiverTradingScraper.employer_name: HudsonRiverTradingScraper,
    KavakScraper.employer_name: KavakScraper,
    HeadwayScraper.employer_name: HeadwayScraper,
    WilsonSonsiniScraper.employer_name: WilsonSonsiniScraper,
    StripeScraper.employer_name: StripeScraper,
    RoivantScraper.employer_name: RoivantScraper,
    HpScraper.employer_name: HpScraper,
    HpeScraper.employer_name: HpeScraper,
    DoubleverifyScraper.employer_name: DoubleverifyScraper,
    AspireScraper.employer_name: AspireScraper,
    FiscalnoteScraper.employer_name: FiscalnoteScraper,
    AkiliScraper.employer_name: AkiliScraper,
    LastminuteScraper.employer_name: LastminuteScraper,
    NvidiaScraper.employer_name: NvidiaScraper,
    AbnormalSecurityScraper.employer_name: AbnormalSecurityScraper,
    BetterupScraper.employer_name: BetterupScraper,
    GlovoScraper.employer_name: GlovoScraper,
    PayuScraper.employer_name: PayuScraper,
    FlexportScraper.employer_name: FlexportScraper,
    FlatironHealthScraper.employer_name: FlatironHealthScraper,
    DynatraceScraper.employer_name: DynatraceScraper,
    OkxScraper.employer_name: OkxScraper,
    OktaScraper.employer_name: OktaScraper,
    CoalitionScraper.employer_name: CoalitionScraper,
    ParloaScraper.employer_name: ParloaScraper,
    FiskerScraper.employer_name: FiskerScraper,
    CheckrScraper.employer_name: CheckrScraper,
    WorkdayCoScraper.employer_name: WorkdayCoScraper,
    RelativitySpaceScraper.employer_name: RelativitySpaceScraper,
    RemoteScraper.employer_name: RemoteScraper,
    TreasureDataScraper.employer_name: TreasureDataScraper,
    AlphasenseScraper.employer_name: AlphasenseScraper,
    KHealthScraper.employer_name: KHealthScraper,
    OpentableScraper.employer_name: OpentableScraper,
    MongodbScraper.employer_name: MongodbScraper,
    SkimsScraper.employer_name: SkimsScraper,
    TuringScraper.employer_name: TuringScraper,
    VMwareScraper.employer_name: VMwareScraper,
    NuveiScraper.employer_name: NuveiScraper,
    Singularity6Scraper.employer_name: Singularity6Scraper,
    CrestaScraper.employer_name: CrestaScraper,
    ArteraScraper.employer_name: ArteraScraper,
    DeepwatchScraper.employer_name: DeepwatchScraper,
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
