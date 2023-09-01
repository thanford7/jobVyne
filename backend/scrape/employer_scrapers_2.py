from scrape.base_scrapers import AshbyHQScraper, \
    EightfoldScraper, GreenhouseApiScraper, GreenhouseIframeScraper, \
    GreenhouseScraper, LeverScraper, SmartRecruitersApiScraper, SmartRecruitersScraper, \
    WorkdayScraper


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


class QualcommScraper(EightfoldScraper):
    employer_name = 'Qualcomm'
    EMPLOYER_KEY = 'qualcomm'


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


class RobinhoodScraper(GreenhouseApiScraper):
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


class AdevintaScraper(SmartRecruitersApiScraper):
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