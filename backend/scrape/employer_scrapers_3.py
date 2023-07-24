from scrape.base_scrapers import AshbyHQScraper, \
    GreenhouseApiScraper, \
    GreenhouseScraper, LeverScraper, SmartRecruitersScraper, \
    WorkdayScraper


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


class AtmosphereTvScraper(LeverScraper):
    employer_name = 'Atmosphere TV'
    EMPLOYER_KEY = 'atmosphere'


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