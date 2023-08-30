from scrape.base_scrapers import AshbyHQScraper, \
    GreenhouseApiScraper, \
    GreenhouseScraper, LeverScraper, SmartRecruitersScraper, \
    WorkdayScraper


class WebSummitScraper(LeverScraper):
    employer_name = 'Web Summit'
    EMPLOYER_KEY = 'websummit'


class SpireGlobalScraper(GreenhouseApiScraper):
    employer_name = 'Spire Global'
    EMPLOYER_KEY = 'spire'


class LogicmonitorScraper(GreenhouseApiScraper):
    employer_name = 'LogicMonitor'
    EMPLOYER_KEY = 'logicmonitor'


class PlaidScraper(LeverScraper):
    employer_name = 'Plaid'
    EMPLOYER_KEY = 'plaid'


class CurebaseScraper(GreenhouseScraper):
    employer_name = 'Curebase'
    EMPLOYER_KEY = 'curebase'


class AvaLabsScraper(GreenhouseScraper):
    employer_name = 'Ava Labs'
    EMPLOYER_KEY = 'avalabs'


class HeartflowScraper(GreenhouseScraper):
    employer_name = 'HeartFlow'
    EMPLOYER_KEY = 'heartflowinc'


class BilliontooneScraper(GreenhouseScraper):
    employer_name = 'BillionToOne'
    EMPLOYER_KEY = 'billiontoone'


class PriviaHealthScraper(SmartRecruitersScraper):
    employer_name = 'Privia Health'
    EMPLOYER_KEY = 'PriviaHealth'


class MoxionScraper(LeverScraper):
    employer_name = 'Moxion'
    EMPLOYER_KEY = 'moxionpower'


class ChainlinkLabsScraper(LeverScraper):
    employer_name = 'Chainlink Labs'
    EMPLOYER_KEY = 'chainlink'


class RazorpayScraper(GreenhouseScraper):
    employer_name = 'Razorpay'
    EMPLOYER_KEY = 'razorpaysoftwareprivatelimited'


class MagicLeapScraper(GreenhouseScraper):
    employer_name = 'Magic Leap'
    EMPLOYER_KEY = 'magicleapinc'


class FortoScraper(GreenhouseScraper):
    employer_name = 'Forto'
    EMPLOYER_KEY = 'fortogmbh'


class JdComScraper(GreenhouseScraper):
    employer_name = 'JD.com'
    EMPLOYER_KEY = 'jdcom'


class KucoinScraper(WorkdayScraper):
    employer_name = 'Kucoin'
    start_url = 'https://flashdot.wd3.myworkdayjobs.com/en-US/OfficialWebsite/'
    has_job_departments = False


class MiraklScraper(GreenhouseScraper):
    employer_name = 'Mirakl'
    EMPLOYER_KEY = 'mirakl'


class SpendeskScraper(LeverScraper):
    employer_name = 'Spendesk'
    EMPLOYER_KEY = 'spendesk'


class AmbientAiScraper(GreenhouseScraper):
    employer_name = 'Ambient.ai'
    EMPLOYER_KEY = 'ambientai'


class FernrideScraper(GreenhouseScraper):
    employer_name = 'Fernride'
    EMPLOYER_KEY = 'fernride'


class ClevertapScraper(LeverScraper):
    employer_name = 'Clevertap'
    EMPLOYER_KEY = 'clevertap'


class IsnScraper(GreenhouseApiScraper):
    employer_name = 'ISN'
    EMPLOYER_KEY = 'isn'


class AppsumoScraper(GreenhouseScraper):
    employer_name = 'AppSumo'
    EMPLOYER_KEY = 'appsumocareers'


class FreshbooksScraper(GreenhouseScraper):
    employer_name = 'FreshBooks'
    EMPLOYER_KEY = 'freshbooks'


class MarkerLearningScraper(GreenhouseApiScraper):
    employer_name = 'Marker Learning'
    EMPLOYER_KEY = 'markerlearning'


class CardlyticsScraper(GreenhouseScraper):
    employer_name = 'Cardlytics'
    EMPLOYER_KEY = 'cardlytics'


class OpenwebScraper(GreenhouseApiScraper):
    employer_name = 'OpenWeb'
    EMPLOYER_KEY = 'openweb'


class CodaPaymentsScraper(LeverScraper):
    employer_name = 'Coda Payments'
    EMPLOYER_KEY = 'codapayments'


class LastEnergyScraper(LeverScraper):
    employer_name = 'Last Energy'
    EMPLOYER_KEY = 'last-energy'


class HumaansScraper(AshbyHQScraper):
    employer_name = 'Humaans'
    EMPLOYER_KEY = 'humaans'


class PinwheelScraper(GreenhouseScraper):
    employer_name = 'Pinwheel'
    EMPLOYER_KEY = 'pinwheelapi'


class FoxitScraper(LeverScraper):
    employer_name = 'Foxit'
    EMPLOYER_KEY = 'foxitsoftware'


class DremioScraper(GreenhouseApiScraper):
    employer_name = 'Dremio'
    EMPLOYER_KEY = 'dremio'


class EventbriteScraper(LeverScraper):
    employer_name = 'Eventbrite'
    EMPLOYER_KEY = 'eventbrite'


class IroncladScraper(AshbyHQScraper):
    employer_name = 'Ironclad'
    EMPLOYER_KEY = 'ironcladhq'


class GroverScraper(GreenhouseScraper):
    employer_name = 'Grover'
    EMPLOYER_KEY = 'grover'


class WerideScraper(LeverScraper):
    employer_name = 'WeRide'
    EMPLOYER_KEY = 'weride'


class PagayaScraper(GreenhouseScraper):
    employer_name = 'Pagaya'
    EMPLOYER_KEY = 'pagaya'


class AnimocaBrandsScraper(LeverScraper):
    employer_name = 'Animoca Brands'
    EMPLOYER_KEY = 'animocabrands'


class FetchRewardsScraper(GreenhouseScraper):
    employer_name = 'Fetch Rewards'
    EMPLOYER_KEY = 'fetchrewards'


class LayerzeroScraper(GreenhouseScraper):
    employer_name = 'LayerZero'
    EMPLOYER_KEY = 'layerzerolabs'


class WeeeScraper(GreenhouseApiScraper):
    employer_name = 'Weee!'
    EMPLOYER_KEY = 'weee'


class EvidationHealthScraper(GreenhouseApiScraper):
    employer_name = 'Evidation Health'
    EMPLOYER_KEY = 'evidation'


class CharthopScraper(GreenhouseApiScraper):
    employer_name = 'ChartHop'
    EMPLOYER_KEY = 'charthop'


class VisierScraper(GreenhouseScraper):
    employer_name = 'Visier'
    EMPLOYER_KEY = 'visiersolutionsinc'


class SmartlingScraper(GreenhouseScraper):
    employer_name = 'Smartling'
    EMPLOYER_KEY = 'smartling'


class AwardcoScraper(GreenhouseApiScraper):
    employer_name = 'Awardco'
    EMPLOYER_KEY = 'awardco'


class TouchbistroScraper(GreenhouseApiScraper):
    employer_name = 'TouchBistro'
    EMPLOYER_KEY = 'touchbistro'


class CreatoriqScraper(GreenhouseApiScraper):
    employer_name = 'CreatorIQ'
    EMPLOYER_KEY = 'creatoriq'


class SuseScraper(WorkdayScraper):
    employer_name = 'SUSE'
    start_url = 'https://suse.wd3.myworkdayjobs.com/en-US/Jobsatsuse/'
    has_job_departments = False


class LendingClubScraper(WorkdayScraper):
    employer_name = 'Lending Club'
    start_url = 'https://lendingclub.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class FingerprintjsScraper(GreenhouseApiScraper):
    employer_name = 'FingerprintJS'
    EMPLOYER_KEY = 'fingerprint'


class HighradiusScraper(GreenhouseApiScraper):
    employer_name = 'HighRadius'
    EMPLOYER_KEY = 'highradius'


class BirdRidesScraper(GreenhouseApiScraper):
    employer_name = 'Bird Rides'
    EMPLOYER_KEY = 'bird'


class ProductsupScraper(GreenhouseApiScraper):
    employer_name = 'Productsup'
    EMPLOYER_KEY = 'productsup'


class SliceScraper(GreenhouseApiScraper):
    employer_name = 'Slice'
    EMPLOYER_KEY = 'slice'


class HarmonyScraper(LeverScraper):
    employer_name = 'Harmony'
    EMPLOYER_KEY = 'harmony'


class OneScraper(AshbyHQScraper):
    employer_name = 'One'
    EMPLOYER_KEY = 'oneapp'


class PantherLabsScraper(GreenhouseScraper):
    employer_name = 'Panther Labs'
    EMPLOYER_KEY = 'pantherlabs'


class SymphonyScraper(GreenhouseApiScraper):
    employer_name = 'Symphony'
    EMPLOYER_KEY = 'symphony'


class Captiv8Scraper(LeverScraper):
    employer_name = 'Captiv8'
    EMPLOYER_KEY = 'captiv8'


class CloudncScraper(LeverScraper):
    employer_name = 'CloudNC'
    EMPLOYER_KEY = 'cloudnc'


class FenwickScraper(WorkdayScraper):
    employer_name = 'Fenwick'
    start_url = 'https://fenwick.wd1.myworkdayjobs.com/en-US/Fenwick_External_Careers/'
    has_job_departments = False


class NinjaVanScraper(LeverScraper):
    employer_name = 'Ninja Van'
    EMPLOYER_KEY = 'ninjavan'


class AffinidiScraper(GreenhouseScraper):
    employer_name = 'Affinidi'
    EMPLOYER_KEY = 'affinidi'


class IressScraper(WorkdayScraper):
    employer_name = 'Iress'
    start_url = 'https://iress.wd3.myworkdayjobs.com/en-US/IRESS_EXTERNAL/'
    has_job_departments = False


class TricentisScraper(WorkdayScraper):
    employer_name = 'Tricentis'
    start_url = 'https://tricentis.wd1.myworkdayjobs.com/en-US/Tricentis_Careers/'
    has_job_departments = False


class ThoughtworksScraper(GreenhouseApiScraper):
    employer_name = 'Thoughtworks'
    EMPLOYER_KEY = 'thoughtworks'


class NextrackerScraper(WorkdayScraper):
    employer_name = 'Nextracker'
    start_url = 'https://flextronics.wd1.myworkdayjobs.com/en-US/Nextracker_Careers/'
    has_job_departments = False


class EmplifiScraper(GreenhouseApiScraper):
    employer_name = 'Emplifi'
    EMPLOYER_KEY = 'emplifi'


class ExtendScraper(GreenhouseScraper):
    employer_name = 'Extend'
    EMPLOYER_KEY = 'extend'


class ImmutableScraper(LeverScraper):
    employer_name = 'Immutable'
    EMPLOYER_KEY = 'immutable'


class PrimeMedicineScraper(GreenhouseScraper):
    employer_name = 'Prime Medicine'
    EMPLOYER_KEY = 'primemedicine'


class DespegarComScraper(LeverScraper):
    employer_name = 'Despegar.com'
    EMPLOYER_KEY = 'despegar'


class PineParkHealthScraper(GreenhouseScraper):
    employer_name = 'Pine Park Health'
    EMPLOYER_KEY = 'pineparkhealth'


class BabylistScraper(GreenhouseScraper):
    employer_name = 'Babylist'
    EMPLOYER_KEY = 'babylist'


class JobandtalentScraper(LeverScraper):
    employer_name = 'Jobandtalent'
    EMPLOYER_KEY = 'jobandtalent'


class HermeusScraper(LeverScraper):
    employer_name = 'Hermeus'
    EMPLOYER_KEY = 'hermeus'


class MeeshoScraper(LeverScraper):
    employer_name = 'Meesho'
    EMPLOYER_KEY = 'meesho'


class PandionScraper(GreenhouseApiScraper):
    employer_name = 'Pandion'
    EMPLOYER_KEY = 'pandion'


class MoonpayScraper(GreenhouseScraper):
    employer_name = 'MoonPay'
    EMPLOYER_KEY = 'moonpay'


class WestMonroeScraper(GreenhouseApiScraper):
    employer_name = 'West Monroe'
    EMPLOYER_KEY = 'westmonroe1'


class JustosScraper(LeverScraper):
    employer_name = 'Justos'
    EMPLOYER_KEY = 'justos'


class LucidMotorsScraper(LeverScraper):
    employer_name = 'Lucid Motors'
    EMPLOYER_KEY = 'lucidmotors'


class WayveScraper(GreenhouseScraper):
    employer_name = 'Wayve'
    EMPLOYER_KEY = 'wayve'


class UbisoftScraper(SmartRecruitersScraper):
    employer_name = 'Ubisoft'
    EMPLOYER_KEY = 'Ubisoft2'


class SanctuaryScraper(LeverScraper):
    employer_name = 'Sanctuary'
    EMPLOYER_KEY = 'sanctuary'


class SymboticScraper(WorkdayScraper):
    employer_name = 'Symbotic'
    start_url = 'https://symbotic.wd1.myworkdayjobs.com/en-US/Symbotic/'
    has_job_departments = False


class GraphiteScraper(AshbyHQScraper):
    employer_name = 'Graphite'
    EMPLOYER_KEY = 'Graphitehq'


class ZiplineScraper(GreenhouseApiScraper):
    employer_name = 'Zipline'
    EMPLOYER_KEY = 'flyzipline'


class SonosScraper(WorkdayScraper):
    employer_name = 'Sonos'
    start_url = 'https://sonos.wd1.myworkdayjobs.com/en-US/Sonos/'
    has_job_departments = False


class BoringCompanyScraper(LeverScraper):
    employer_name = 'Boring Company'
    EMPLOYER_KEY = 'boringcompany'


class EbayScraper(WorkdayScraper):
    employer_name = 'eBay'
    start_url = 'https://ebay.wd5.myworkdayjobs.com/en-US/apply/'
    has_job_departments = False


class GymsharkScraper(GreenhouseScraper):
    employer_name = 'Gymshark'
    EMPLOYER_KEY = 'gymshark'


class UltimaGenomicsScraper(GreenhouseScraper):
    employer_name = 'Ultima Genomics'
    EMPLOYER_KEY = 'ultimagenomics'


class ShieldAiScraper(LeverScraper):
    employer_name = 'Shield AI'
    EMPLOYER_KEY = 'shieldai'


class NeteaseScraper(WorkdayScraper):
    employer_name = 'NetEase'
    start_url = 'https://netease.wd3.myworkdayjobs.com/en-US/NetEasegroup/'
    has_job_departments = False


class AboutYouScraper(SmartRecruitersScraper):
    employer_name = 'About You'
    EMPLOYER_KEY = 'ABOUTYOUGmbH'


class BrightMachinesScraper(LeverScraper):
    employer_name = 'Bright Machines'
    EMPLOYER_KEY = 'brightmachines'


class HowdenGroupScraper(WorkdayScraper):
    employer_name = 'Howden Group'
    start_url = 'https://howden.wd3.myworkdayjobs.com/en-US/external/'
    has_job_departments = False


class ArcherScraper(GreenhouseScraper):
    employer_name = 'Archer'
    EMPLOYER_KEY = 'archer56'


class BeyondMeatScraper(LeverScraper):
    employer_name = 'Beyond Meat'
    EMPLOYER_KEY = 'beyondmeat'


class QuinceScraper(LeverScraper):
    employer_name = 'Quince'
    EMPLOYER_KEY = 'quince'


class MayMobilityScraper(GreenhouseScraper):
    employer_name = 'May Mobility'
    EMPLOYER_KEY = 'maymobility'


class LivescoreScraper(GreenhouseApiScraper):
    employer_name = 'LiveScore'
    EMPLOYER_KEY = 'livescore9'


class LightspeedScraper(GreenhouseScraper):
    employer_name = 'Lightspeed'
    EMPLOYER_KEY = 'lightspeedhq'


class SweetgreenScraper(GreenhouseApiScraper):
    employer_name = 'Sweetgreen'
    EMPLOYER_KEY = 'sweetgreen'


class CommonwealthFusionScraper(LeverScraper):
    employer_name = 'Commonwealth Fusion'
    EMPLOYER_KEY = 'cfsenergy'


class TheRealrealScraper(GreenhouseScraper):
    employer_name = 'The RealReal'
    EMPLOYER_KEY = 'therealreal'


class AgilityRoboticsScraper(GreenhouseApiScraper):
    employer_name = 'Agility Robotics'
    EMPLOYER_KEY = 'agilityrobotics'


class ChimeScraper(GreenhouseApiScraper):
    employer_name = 'Chime'
    EMPLOYER_KEY = 'chime'


class AndelaScraper(GreenhouseScraper):
    employer_name = 'Andela'
    EMPLOYER_KEY = 'andela'


class RemoraScraper(GreenhouseScraper):
    employer_name = 'Remora'
    EMPLOYER_KEY = 'remoracarbon'


class LimeScraper(LeverScraper):
    employer_name = 'Lime'
    EMPLOYER_KEY = 'lime'


class VentionScraper(SmartRecruitersScraper):
    employer_name = 'Vention'
    EMPLOYER_KEY = 'Vention'


class MightyBuildingsScraper(GreenhouseApiScraper):
    employer_name = 'Mighty Buildings'
    EMPLOYER_KEY = 'mightybuildings'


class TaeScraper(GreenhouseScraper):
    employer_name = 'TAE'
    EMPLOYER_KEY = 'taepwm'


class MisfitsMarketScraper(GreenhouseScraper):
    employer_name = 'Misfits Market'
    EMPLOYER_KEY = 'misfitsmarket'


class ThrasioScraper(LeverScraper):
    employer_name = 'Thrasio'
    EMPLOYER_KEY = 'thrasio'


class PlumeScraper(GreenhouseApiScraper):
    employer_name = 'Plume'
    EMPLOYER_KEY = 'plume'


class FormEnergyScraper(LeverScraper):
    employer_name = 'Form Energy'
    EMPLOYER_KEY = 'formenergy'


class SsenseScraper(SmartRecruitersScraper):
    employer_name = 'SSENSE'
    EMPLOYER_KEY = 'SSENSE1'


class XosScraper(GreenhouseApiScraper):
    employer_name = 'Xos'
    EMPLOYER_KEY = 'xosinc'


class GenesysScraper(WorkdayScraper):
    employer_name = 'Genesys'
    start_url = 'https://genesys.wd1.myworkdayjobs.com/en-US/Genesys/'
    has_job_departments = False


class IspaceScraper(LeverScraper):
    employer_name = 'ispace'
    EMPLOYER_KEY = 'ispace-inc'


class MindgeekScraper(GreenhouseScraper):
    employer_name = 'MindGeek'
    EMPLOYER_KEY = 'mindgeek'


class PagerdutyScraper(GreenhouseScraper):
    employer_name = 'Pagerduty'
    EMPLOYER_KEY = 'pagerduty'


class ViceMediaScraper(WorkdayScraper):
    employer_name = 'Vice Media'
    start_url = 'https://vice.wd1.myworkdayjobs.com/en-US/Vice_External_Career_Site/'
    has_job_departments = False


class ContentsquareScraper(LeverScraper):
    employer_name = 'Contentsquare'
    EMPLOYER_KEY = 'contentsquare'


class ButcherboxScraper(LeverScraper):
    employer_name = 'ButcherBox'
    EMPLOYER_KEY = 'butcherbox'


class CoreScientificScraper(GreenhouseScraper):
    employer_name = 'Core Scientific'
    EMPLOYER_KEY = 'corescientific'


class FloqastScraper(LeverScraper):
    employer_name = 'FloQast'
    EMPLOYER_KEY = 'floqast'


class TiveScraper(LeverScraper):
    employer_name = 'Tive'
    EMPLOYER_KEY = 'Tive'


class LiliumAviationScraper(GreenhouseApiScraper):
    employer_name = 'Lilium Aviation'
    EMPLOYER_KEY = 'lilium'


class AiFundScraper(LeverScraper):
    employer_name = 'AI Fund'
    EMPLOYER_KEY = 'landing'


class BitgoScraper(GreenhouseScraper):
    employer_name = 'BitGo'
    EMPLOYER_KEY = 'bitgo'


class Divergent3dScraper(LeverScraper):
    employer_name = 'Divergent 3D'
    EMPLOYER_KEY = 'divergent3d'


class StennScraper(GreenhouseScraper):
    employer_name = 'Stenn'
    EMPLOYER_KEY = 'stenn'


class ScribeTherapeuticsScraper(GreenhouseScraper):
    employer_name = 'Scribe Therapeutics'
    EMPLOYER_KEY = 'scribetherapeutics'


class ParityScraper(GreenhouseScraper):
    employer_name = 'Parity'
    EMPLOYER_KEY = 'parity'


class FreenomeScraper(GreenhouseScraper):
    employer_name = 'Freenome'
    EMPLOYER_KEY = 'freenome'


class IcapitalNetworkScraper(GreenhouseScraper):
    employer_name = 'iCapital Network'
    EMPLOYER_KEY = 'icapitalnetwork'


class AltosLabsScraper(GreenhouseScraper):
    employer_name = 'Altos Labs'
    EMPLOYER_KEY = 'altoslabs'


class SaliogenScraper(GreenhouseScraper):
    employer_name = 'SalioGen'
    EMPLOYER_KEY = 'saliogen'


class TerrayTherapeuticsScraper(GreenhouseScraper):
    employer_name = 'Terray Therapeutics'
    EMPLOYER_KEY = 'terraytherapeutics'


class MosaicmlScraper(GreenhouseScraper):
    employer_name = 'MosaicML'
    EMPLOYER_KEY = 'mosaicml'


class InariScraper(GreenhouseApiScraper):
    employer_name = 'Inari'
    EMPLOYER_KEY = 'inariagriculture'


class ConvoyScraper(GreenhouseScraper):
    employer_name = 'Convoy'
    EMPLOYER_KEY = 'convoy'


class BravadoScraper(GreenhouseScraper):
    employer_name = 'Bravado'
    EMPLOYER_KEY = 'bravado'


class JinaAiScraper(LeverScraper):
    employer_name = 'Jina AI'
    EMPLOYER_KEY = 'jina-ai'


class DynoTherapeuticsScraper(GreenhouseApiScraper):
    employer_name = 'Dyno Therapeutics'
    EMPLOYER_KEY = 'dynotherapeutics'


class CircleciScraper(GreenhouseApiScraper):
    employer_name = 'CircleCI'
    EMPLOYER_KEY = 'circleci'


class AllenInstituteScraper(GreenhouseScraper):
    employer_name = 'Allen Institute'
    EMPLOYER_KEY = 'thealleninstitute'


class ColossalScraper(GreenhouseApiScraper):
    employer_name = 'Colossal'
    EMPLOYER_KEY = 'colossalbiosciences'


class StaffbaseScraper(GreenhouseApiScraper):
    employer_name = 'Staffbase'
    EMPLOYER_KEY = 'staffbase'


class AkunaCapitalScraper(GreenhouseApiScraper):
    employer_name = 'Akuna Capital'
    EMPLOYER_KEY = 'akunacapital'


class NianticScraper(GreenhouseScraper):
    employer_name = 'Niantic'
    EMPLOYER_KEY = 'niantic'


class MonadLabsScraper(GreenhouseScraper):
    employer_name = 'Monad Labs'
    EMPLOYER_KEY = 'monad'


class CbInsightsScraper(GreenhouseScraper):
    employer_name = 'CB Insights'
    EMPLOYER_KEY = 'cbinsights'


class TopographyHealthScraper(LeverScraper):
    employer_name = 'Topography Health'
    EMPLOYER_KEY = 'jointopo'


class SafeSecurityScraper(LeverScraper):
    employer_name = 'Safe Security'
    EMPLOYER_KEY = 'safe'


class MammothBiosciencesScraper(LeverScraper):
    employer_name = 'Mammoth Biosciences'
    EMPLOYER_KEY = 'mammothbiosci'


class BostonDynamicsScraper(WorkdayScraper):
    employer_name = 'Boston Dynamics'
    start_url = 'https://bostondynamics.wd1.myworkdayjobs.com/en-US/Boston_Dynamics/'
    has_job_departments = False


class AdeptScraper(GreenhouseScraper):
    employer_name = 'Adept'
    EMPLOYER_KEY = 'adept'


class EpicGamesScraper(GreenhouseScraper):
    employer_name = 'Epic Games'
    EMPLOYER_KEY = 'epicgames'


class QuantinuumScraper(LeverScraper):
    employer_name = 'Quantinuum'
    EMPLOYER_KEY = 'quantinuum'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class PlentyScraper(GreenhouseApiScraper):
    employer_name = 'Plenty'
    EMPLOYER_KEY = 'plenty'


class LumaAiScraper(LeverScraper):
    employer_name = 'Luma AI'
    EMPLOYER_KEY = 'LumaAi'


class SandboxaqScraper(GreenhouseApiScraper):
    employer_name = 'SandboxAQ'
    EMPLOYER_KEY = 'sandboxaq'


class StatusScraper(GreenhouseApiScraper):
    employer_name = 'Status'
    EMPLOYER_KEY = 'status72'


class ImcScraper(WorkdayScraper):
    employer_name = 'IMC'
    start_url = 'https://imc.wd5.myworkdayjobs.com/en-US/IMC_USA/'
    has_job_departments = False


class GinkgoBioworksScraper(GreenhouseApiScraper):
    employer_name = 'Ginkgo BioWorks'
    EMPLOYER_KEY = 'ginkgobioworks'


class GreenlightScraper(LeverScraper):
    employer_name = 'Greenlight'
    EMPLOYER_KEY = 'greenlight'


class PaperspaceScraper(GreenhouseScraper):
    employer_name = 'Paperspace'
    EMPLOYER_KEY = 'paperspace'


class DeepmindScraper(GreenhouseScraper):
    employer_name = 'Deepmind'
    EMPLOYER_KEY = 'deepmind'


class LoomScraper(GreenhouseScraper):
    employer_name = 'Loom'
    EMPLOYER_KEY = 'loominc'


class ToyotaResearchScraper(LeverScraper):
    employer_name = 'Toyota Research'
    EMPLOYER_KEY = 'tri'


class PipeScraper(GreenhouseApiScraper):
    employer_name = 'Pipe'
    EMPLOYER_KEY = 'pipetechnologies'


class DiligentScraper(GreenhouseScraper):
    employer_name = 'Diligent'
    EMPLOYER_KEY = 'diligentcorporation'


class TowerResearchScraper(GreenhouseApiScraper):
    employer_name = 'Tower Research'
    EMPLOYER_KEY = 'towerresearchcapital'


class GlobalizationPartnersScraper(GreenhouseScraper):
    employer_name = 'Globalization Partners'
    EMPLOYER_KEY = 'globalizationpartners'


class PivotBioScraper(GreenhouseApiScraper):
    employer_name = 'Pivot Bio'
    EMPLOYER_KEY = 'pivotbio'


class IexScraper(GreenhouseApiScraper):
    employer_name = 'IEX'
    EMPLOYER_KEY = 'iex'


class RunwayScraper(GreenhouseScraper):
    employer_name = 'Runway'
    EMPLOYER_KEY = 'runwayml'


class DrwScraper(GreenhouseScraper):
    employer_name = 'DRW'
    EMPLOYER_KEY = 'drweng'


class EsusuScraper(GreenhouseApiScraper):
    employer_name = 'Esusu'
    EMPLOYER_KEY = 'esusu'


class QualtricsScraper(GreenhouseApiScraper):
    employer_name = 'Qualtrics'
    EMPLOYER_KEY = 'qualtrics'


class DescriptScraper(GreenhouseApiScraper):
    employer_name = 'Descript'
    EMPLOYER_KEY = 'descript'


class TheBlockScraper(LeverScraper):
    employer_name = 'The Block'
    EMPLOYER_KEY = 'theblockcrypto'


class QCtrlScraper(LeverScraper):
    employer_name = 'Q-CTRL'
    EMPLOYER_KEY = 'q-ctrl'


class PqshieldScraper(GreenhouseApiScraper):
    employer_name = 'PQShield'
    EMPLOYER_KEY = 'pqshield'


class RetroBioScraper(LeverScraper):
    employer_name = 'Retro Bio'
    EMPLOYER_KEY = 'retro'


class CalicoScraper(GreenhouseApiScraper):
    employer_name = 'Calico'
    EMPLOYER_KEY = 'calicolabs'


class OffchainLabsScraper(LeverScraper):
    employer_name = 'Offchain Labs'
    EMPLOYER_KEY = 'offchainlabs'