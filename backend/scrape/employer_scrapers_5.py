from scrape.base_scrapers import AshbyHQScraper, \
    GreenhouseApiScraper, \
    GreenhouseScraper, LeverScraper, SmartRecruitersScraper, \
    WorkdayScraper


class WaymoScraper(GreenhouseApiScraper):
    employer_name = 'Waymo'
    EMPLOYER_KEY = 'waymo'


class OptiverScraper(GreenhouseApiScraper):
    employer_name = 'Optiver'
    EMPLOYER_KEY = 'optiverus'


class SamsungResearchScraper(GreenhouseScraper):
    employer_name = 'Samsung Research'
    EMPLOYER_KEY = 'samsungresearchamerica'


class NewlimitScraper(GreenhouseScraper):
    employer_name = 'NewLimit'
    EMPLOYER_KEY = 'newlimit'


class NuanceScraper(WorkdayScraper):
    employer_name = 'Nuance'
    start_url = 'https://nuance.wd1.myworkdayjobs.com/en-US/Nuance/'
    has_job_departments = False


class ChartboostScraper(GreenhouseScraper):
    employer_name = 'Chartboost'
    EMPLOYER_KEY = 'chartboost'


class AltanaScraper(GreenhouseScraper):
    employer_name = 'Altana'
    EMPLOYER_KEY = 'altanaai'


class DrataScraper(GreenhouseApiScraper):
    employer_name = 'Drata'
    EMPLOYER_KEY = 'drata'


class GranicaScraper(GreenhouseScraper):
    employer_name = 'Granica'
    EMPLOYER_KEY = 'granica'


class ArtsyScraper(GreenhouseScraper):
    employer_name = 'Artsy'
    EMPLOYER_KEY = 'artsy'


class TandemaiScraper(GreenhouseScraper):
    employer_name = 'TandemAI'
    EMPLOYER_KEY = 'tandemailimited'


class NetradyneScraper(GreenhouseApiScraper):
    employer_name = 'Netradyne'
    EMPLOYER_KEY = 'netradyne'


class VarjoScraper(GreenhouseApiScraper):
    employer_name = 'Varjo'
    EMPLOYER_KEY = 'varjo'


class StriveHealthScraper(GreenhouseScraper):
    employer_name = 'Strive Health'
    EMPLOYER_KEY = 'strivehealth'


class AirtableScraper(GreenhouseScraper):
    employer_name = 'Airtable'
    EMPLOYER_KEY = 'airtable'


class InscribeScraper(AshbyHQScraper):
    employer_name = 'Inscribe'
    EMPLOYER_KEY = 'InscribeAI'


class UnlearnScraper(LeverScraper):
    employer_name = 'Unlearn'
    EMPLOYER_KEY = 'UnlearnAI'


class SynthesiaScraper(GreenhouseApiScraper):
    employer_name = 'Synthesia'
    EMPLOYER_KEY = 'synthesia'


class CogniteScraper(LeverScraper):
    employer_name = 'Cognite'
    EMPLOYER_KEY = 'cognite'


class EvenupScraper(LeverScraper):
    employer_name = 'EvenUp'
    EMPLOYER_KEY = 'evenuplaw'


class TempusScraper(GreenhouseApiScraper):
    employer_name = 'Tempus'
    EMPLOYER_KEY = 'tempus'


class StyleseatScraper(GreenhouseApiScraper):
    employer_name = 'StyleSeat'
    EMPLOYER_KEY = 'styleseat32'


class LevelAiScraper(LeverScraper):
    employer_name = 'Level AI'
    EMPLOYER_KEY = 'levelai'


class VeranaHealthScraper(GreenhouseScraper):
    employer_name = 'Verana Health'
    EMPLOYER_KEY = 'veranahealth'


class NeuralinkScraper(GreenhouseScraper):
    employer_name = 'Neuralink'
    EMPLOYER_KEY = 'neuralink'


class OdaiaScraper(LeverScraper):
    employer_name = 'ODAIA'
    EMPLOYER_KEY = 'OdaiaIntelligence'


class RecRoomScraper(GreenhouseApiScraper):
    employer_name = 'Rec Room'
    EMPLOYER_KEY = 'recroom'


class InfermedicaScraper(LeverScraper):
    employer_name = 'Infermedica'
    EMPLOYER_KEY = 'infermedica'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class SambanovaScraper(GreenhouseApiScraper):
    employer_name = 'SambaNova'
    EMPLOYER_KEY = 'sambanovasystems'


class BoostedAiScraper(GreenhouseScraper):
    employer_name = 'Boosted.ai'
    EMPLOYER_KEY = 'boostedai'


class StabilityAiScraper(GreenhouseApiScraper):
    employer_name = 'Stability AI'
    EMPLOYER_KEY = 'stabilityai'


class NotcoScraper(LeverScraper):
    employer_name = 'NotCo'
    EMPLOYER_KEY = 'thenotcompany'


class AvailityScraper(WorkdayScraper):
    employer_name = 'Availity'
    start_url = 'https://availity.wd1.myworkdayjobs.com/en-US/Availity_Careers_US/'
    has_job_departments = False


class ReplitScraper(AshbyHQScraper):
    employer_name = 'Replit'
    EMPLOYER_KEY = 'replit'


class ApplovinScraper(GreenhouseApiScraper):
    employer_name = 'AppLovin'
    EMPLOYER_KEY = 'applovin'


class TurnitinScraper(SmartRecruitersScraper):
    employer_name = 'Turnitin'
    EMPLOYER_KEY = 'TurnitinLLC'


class PodiumScraper(GreenhouseScraper):
    employer_name = 'Podium'
    EMPLOYER_KEY = 'podium81'


class WesternDigitalScraper(SmartRecruitersScraper):
    employer_name = 'Western Digital'
    EMPLOYER_KEY = 'WesternDigital'


class FractalAnalyticsScraper(WorkdayScraper):
    employer_name = 'Fractal Analytics'
    start_url = 'https://fractal.wd1.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class AsanaScraper(GreenhouseApiScraper):
    employer_name = 'Asana'
    EMPLOYER_KEY = 'asana'


class OpenaiScraper(GreenhouseScraper):
    employer_name = 'OpenAI'
    EMPLOYER_KEY = 'openai'


class DropboxScraper(GreenhouseApiScraper):
    employer_name = 'Dropbox'
    EMPLOYER_KEY = 'dropbox'


class IonqScraper(GreenhouseApiScraper):
    employer_name = 'IonQ'
    EMPLOYER_KEY = 'ionq'


class MolocoScraper(GreenhouseScraper):
    employer_name = 'Moloco'
    EMPLOYER_KEY = 'moloco'


class BrainstationScraper(GreenhouseScraper):
    employer_name = 'BrainStation'
    EMPLOYER_KEY = 'brainstation'


class CreditbookScraper(GreenhouseScraper):
    employer_name = 'CreditBook'
    EMPLOYER_KEY = 'creditbook'


class SisuDataScraper(AshbyHQScraper):
    employer_name = 'Sisu Data'
    EMPLOYER_KEY = 'sisudata'


class MindsdbScraper(LeverScraper):
    employer_name = 'MindsDB'
    EMPLOYER_KEY = 'mindsdb'


class AhrefsScraper(GreenhouseScraper):
    employer_name = 'Ahrefs'
    EMPLOYER_KEY = 'ahrefsjobs'


class BillComScraper(GreenhouseApiScraper):
    employer_name = 'Bill.com'
    EMPLOYER_KEY = 'billcom'


class SnorkelAiScraper(GreenhouseScraper):
    employer_name = 'Snorkel AI'
    EMPLOYER_KEY = 'snorkelai'


class HarrisonAiScraper(LeverScraper):
    employer_name = 'Harrison.ai'
    EMPLOYER_KEY = 'harrison'


class FirstdibsScraper(GreenhouseApiScraper):
    employer_name = '1stDibs'
    EMPLOYER_KEY = '1stdibscom'


class LemonadeScraper(GreenhouseApiScraper):
    employer_name = 'Lemonade'
    EMPLOYER_KEY = 'lemonade'


class CelestialAiScraper(GreenhouseScraper):
    employer_name = 'Celestial AI'
    EMPLOYER_KEY = 'celestialai'


class ShopifyScraper(SmartRecruitersScraper):
    employer_name = 'Shopify'
    EMPLOYER_KEY = 'Shopify'


class CourseHeroScraper(GreenhouseApiScraper):
    employer_name = 'Course Hero'
    EMPLOYER_KEY = 'coursehero'


class ZapierScraper(GreenhouseApiScraper):
    employer_name = 'Zapier'
    EMPLOYER_KEY = 'zapier'


class GumgumScraper(GreenhouseScraper):
    employer_name = 'GumGum'
    EMPLOYER_KEY = 'gumgum'


class IntercomScraper(GreenhouseScraper):
    employer_name = 'Intercom'
    EMPLOYER_KEY = 'intercom'


class BaiduScraper(GreenhouseApiScraper):
    employer_name = 'Baidu'
    EMPLOYER_KEY = 'baidu'


class FathomScraper(GreenhouseScraper):
    employer_name = 'Fathom'
    EMPLOYER_KEY = 'fathom'


class TruebillScraper(GreenhouseScraper):
    employer_name = 'Truebill'
    EMPLOYER_KEY = 'truebill'


class EcovadisScraper(SmartRecruitersScraper):
    employer_name = 'EcoVadis'
    EMPLOYER_KEY = 'ecovadis'


class PocusScraper(AshbyHQScraper):
    employer_name = 'Pocus'
    EMPLOYER_KEY = 'pocus'


class BluecoreScraper(GreenhouseApiScraper):
    employer_name = 'Bluecore'
    EMPLOYER_KEY = 'bluecoreinc'


class ApeelSciencesScraper(GreenhouseScraper):
    employer_name = 'Apeel Sciences'
    EMPLOYER_KEY = 'apeel'


class MotiveScraper(GreenhouseScraper):
    employer_name = 'Motive'
    EMPLOYER_KEY = 'gomotive'


class VouchScraper(GreenhouseScraper):
    employer_name = 'Vouch'
    EMPLOYER_KEY = 'vouchinsurance'


class GoldbellyScraper(GreenhouseScraper):
    employer_name = 'Goldbelly'
    EMPLOYER_KEY = 'goldbelly'


class SpeakScraper(AshbyHQScraper):
    employer_name = 'Speak'
    EMPLOYER_KEY = 'Speak'


class TenstorrentScraper(LeverScraper):
    employer_name = 'Tenstorrent'
    EMPLOYER_KEY = 'tenstorrent'


class Forty2dotScraper(LeverScraper):
    employer_name = '42dot'
    EMPLOYER_KEY = '42dot'


class BlackCrowAiScraper(LeverScraper):
    employer_name = 'Black Crow AI'
    EMPLOYER_KEY = 'blackcrow'


class OntraScraper(GreenhouseApiScraper):
    employer_name = 'Ontra'
    EMPLOYER_KEY = 'ontracareers'


class PicsartScraper(GreenhouseApiScraper):
    employer_name = 'Picsart'
    EMPLOYER_KEY = 'picsart'


class Five9Scraper(GreenhouseApiScraper):
    employer_name = 'Five9'
    EMPLOYER_KEY = 'five9'


class MovableInkScraper(GreenhouseApiScraper):
    employer_name = 'Movable Ink'
    EMPLOYER_KEY = 'movableink'


class IntegralAdScienceScraper(WorkdayScraper):
    employer_name = 'Integral Ad Science'
    start_url = 'https://integralads.wd1.myworkdayjobs.com/en-US/IAScareers/'
    has_job_departments = False


class OwkinScraper(GreenhouseApiScraper):
    employer_name = 'Owkin'
    EMPLOYER_KEY = 'owkin'


class TomtomScraper(LeverScraper):
    employer_name = 'TomTom'
    EMPLOYER_KEY = 'tomtom'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class SpotterScraper(GreenhouseScraper):
    employer_name = 'Spotter'
    EMPLOYER_KEY = 'spotter'


class MystenLabsScraper(AshbyHQScraper):
    employer_name = 'Mysten Labs'
    EMPLOYER_KEY = 'mystenlabs'


class VetcoveScraper(AshbyHQScraper):
    employer_name = 'Vetcove'
    EMPLOYER_KEY = 'Vetcove'


class SoundhoundScraper(GreenhouseScraper):
    employer_name = 'Soundhound'
    EMPLOYER_KEY = 'soundhoundinc'


class CoveraHealthScraper(GreenhouseScraper):
    employer_name = 'Covera Health'
    EMPLOYER_KEY = 'coverahealth'


class PureStorageScraper(GreenhouseScraper):
    employer_name = 'Pure Storage'
    EMPLOYER_KEY = 'purestorage'


class SciencelogicScraper(GreenhouseScraper):
    employer_name = 'ScienceLogic'
    EMPLOYER_KEY = 'sciencelogic'


class PhonepeScraper(GreenhouseScraper):
    employer_name = 'PhonePe'
    EMPLOYER_KEY = 'phonepe'


class AlationScraper(LeverScraper):
    employer_name = 'Alation'
    EMPLOYER_KEY = 'alation'


class MarklogicScraper(GreenhouseApiScraper):
    employer_name = 'MarkLogic'
    EMPLOYER_KEY = 'marklogic'


class EppoScraper(AshbyHQScraper):
    employer_name = 'Eppo'
    EMPLOYER_KEY = 'eppo'


class NarmiScraper(LeverScraper):
    employer_name = 'Narmi'
    EMPLOYER_KEY = 'narmi'


class ChainalysisScraper(GreenhouseScraper):
    employer_name = 'Chainalysis'
    EMPLOYER_KEY = 'chainalysis'


class AxoniusScraper(GreenhouseApiScraper):
    employer_name = 'Axonius'
    EMPLOYER_KEY = 'axonius'


class CodeForAmericaScraper(GreenhouseApiScraper):
    employer_name = 'Code for America'
    EMPLOYER_KEY = 'codeforamerica'


class KomodoHealthScraper(GreenhouseApiScraper):
    employer_name = 'Komodo Health'
    EMPLOYER_KEY = 'komodohealth'


class BotifyScraper(LeverScraper):
    employer_name = 'Botify'
    EMPLOYER_KEY = 'botify'


class AviatrixScraper(GreenhouseApiScraper):
    employer_name = 'Aviatrix'
    EMPLOYER_KEY = 'aviatrix'


class MarigoldScraper(WorkdayScraper):
    employer_name = 'Marigold'
    start_url = 'https://campaignmonitor.wd5.myworkdayjobs.com/en-US/marigold/'
    has_job_departments = False


class AstronomerScraper(AshbyHQScraper):
    employer_name = 'Astronomer'
    EMPLOYER_KEY = 'astronomer'


class TranscarentScraper(GreenhouseScraper):
    employer_name = 'Transcarent'
    EMPLOYER_KEY = 'transcarent'


class VercelScraper(GreenhouseScraper):
    employer_name = 'Vercel'
    EMPLOYER_KEY = 'vercel'


class VerilyScraper(GreenhouseApiScraper):
    employer_name = 'Verily'
    EMPLOYER_KEY = 'verily'


class DatagrailScraper(GreenhouseScraper):
    employer_name = 'DataGrail'
    EMPLOYER_KEY = 'datagrail'


class AppianScraper(GreenhouseScraper):
    employer_name = 'Appian'
    EMPLOYER_KEY = 'appian'


class TailscaleScraper(GreenhouseScraper):
    employer_name = 'Tailscale'
    EMPLOYER_KEY = 'tailscale'


class Eightx8Scraper(LeverScraper):
    employer_name = '8x8'
    EMPLOYER_KEY = '8x8'


class RelexSolutionsScraper(GreenhouseApiScraper):
    employer_name = 'Relex Solutions'
    EMPLOYER_KEY = 'relex'


class RaiseScraper(GreenhouseApiScraper):
    employer_name = 'Raise'
    EMPLOYER_KEY = 'raise'


class RubrikScraper(GreenhouseApiScraper):
    employer_name = 'Rubrik'
    EMPLOYER_KEY = 'rubrik'


class FlockSafetyScraper(GreenhouseScraper):
    employer_name = 'Flock Safety'
    EMPLOYER_KEY = 'flocksafety'


class LogicgateScraper(GreenhouseScraper):
    employer_name = 'LogicGate'
    EMPLOYER_KEY = 'logicgate'


class ZoomScraper(WorkdayScraper):
    employer_name = 'Zoom'
    start_url = 'https://zoom.wd5.myworkdayjobs.com/en-US/Zoom/'
    has_job_departments = False


class RobinScraper(LeverScraper):
    employer_name = 'Robin'
    EMPLOYER_KEY = 'robinpowered'


class AirbaseScraper(GreenhouseScraper):
    employer_name = 'Airbase'
    EMPLOYER_KEY = 'airbase'


class MemfaultScraper(LeverScraper):
    employer_name = 'Memfault'
    EMPLOYER_KEY = 'memfault'


class SitetrackerScraper(LeverScraper):
    employer_name = 'Sitetracker'
    EMPLOYER_KEY = 'sitetracker'


class PlanetscaleScraper(GreenhouseScraper):
    employer_name = 'PlanetScale'
    EMPLOYER_KEY = 'planetscale'


class VezaScraper(GreenhouseScraper):
    employer_name = 'Veza'
    EMPLOYER_KEY = 'veza'


class PrimerScraper(GreenhouseScraper):
    employer_name = 'Primer'
    EMPLOYER_KEY = 'primerai'


class OwnbackupScraper(GreenhouseApiScraper):
    employer_name = 'OwnBackup'
    EMPLOYER_KEY = 'ownbackup'


class CovermymedsScraper(WorkdayScraper):
    employer_name = 'CoverMyMeds'
    start_url = 'https://mckesson.wd3.myworkdayjobs.com/en-US/CoverMyMeds_External_Careers/'
    has_job_departments = False


class SysdigScraper(GreenhouseScraper):
    employer_name = 'Sysdig'
    EMPLOYER_KEY = 'sysdig'


class AssentComplianceScraper(SmartRecruitersScraper):
    employer_name = 'Assent Compliance'
    EMPLOYER_KEY = 'Assent'


class SendcloudScraper(GreenhouseApiScraper):
    employer_name = 'Sendcloud'
    EMPLOYER_KEY = 'sendcloud'


class SiftScraper(GreenhouseScraper):
    employer_name = 'Sift'
    EMPLOYER_KEY = 'siftscience'


class RepriseScraper(GreenhouseApiScraper):
    employer_name = 'Reprise'
    EMPLOYER_KEY = 'reprise'


class ProcoreScraper(SmartRecruitersScraper):
    employer_name = 'Procore'
    EMPLOYER_KEY = 'ProcoreTechnologies'


class VtexScraper(GreenhouseApiScraper):
    employer_name = 'VTEX'
    EMPLOYER_KEY = 'vtex'


class MediamathScraper(GreenhouseApiScraper):
    employer_name = 'MediaMath'
    EMPLOYER_KEY = 'mediamath'


class PigmentScraper(LeverScraper):
    employer_name = 'Pigment'
    EMPLOYER_KEY = 'pigment'


class CadenceScraper(WorkdayScraper):
    employer_name = 'Cadence'
    start_url = 'https://cadence.wd1.myworkdayjobs.com/en-US/External_Careers/'
    has_job_departments = False


class FactsetScraper(WorkdayScraper):
    employer_name = 'Factset'
    start_url = 'https://factset.wd1.myworkdayjobs.com/en-US/FactSetCareers/'
    has_job_departments = False


class AgoraScraper(GreenhouseApiScraper):
    employer_name = 'Agora'
    EMPLOYER_KEY = 'agoralabinc'


class Neo4jScraper(GreenhouseApiScraper):
    employer_name = 'Neo4j'
    EMPLOYER_KEY = 'neo4j'


class Rapid7Scraper(WorkdayScraper):
    employer_name = 'Rapid7'
    start_url = 'https://mymoose.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class RossumScraper(GreenhouseApiScraper):
    employer_name = 'Rossum'
    EMPLOYER_KEY = 'rossum'


class MessagebirdScraper(AshbyHQScraper):
    employer_name = 'MessageBird'
    EMPLOYER_KEY = 'messagebird'


class BufScraper(GreenhouseApiScraper):
    employer_name = 'Buf'
    EMPLOYER_KEY = 'buftechnologies'


class HootsuiteScraper(GreenhouseApiScraper):
    employer_name = 'Hootsuite'
    EMPLOYER_KEY = 'hootsuite'


class ArmisScraper(GreenhouseScraper):
    employer_name = 'Armis'
    EMPLOYER_KEY = 'armissecurity'


class IcertisScraper(LeverScraper):
    employer_name = 'Icertis'
    EMPLOYER_KEY = 'icertis'


class NexthinkScraper(SmartRecruitersScraper):
    employer_name = 'Nexthink'
    EMPLOYER_KEY = 'Nexthink'


class RakutenScraper(WorkdayScraper):
    employer_name = 'Rakuten'
    start_url = 'https://rakuten.wd1.myworkdayjobs.com/en-US/RakutenAmericas/'
    has_job_departments = False


class JfrogScraper(GreenhouseApiScraper):
    employer_name = 'JFrog'
    EMPLOYER_KEY = 'jfrog'


class SkydioScraper(GreenhouseScraper):
    employer_name = 'Skydio'
    EMPLOYER_KEY = 'skydio'


class HudlScraper(GreenhouseScraper):
    employer_name = 'Hudl'
    EMPLOYER_KEY = 'hudl'


class ImpactComScraper(GreenhouseScraper):
    employer_name = 'Impact.com'
    EMPLOYER_KEY = 'impact'


class AlteryxScraper(WorkdayScraper):
    employer_name = 'Alteryx'
    start_url = 'https://alteryx.wd5.myworkdayjobs.com/en-US/AlteryxCareers/'
    has_job_departments = False


class BroadcomScraper(WorkdayScraper):
    employer_name = 'Broadcom'
    start_url = 'https://broadcom.wd1.myworkdayjobs.com/en-US/External_Career/'
    has_job_departments = False


class ContentstackScraper(GreenhouseApiScraper):
    employer_name = 'Contentstack'
    EMPLOYER_KEY = 'contentstack'


class LambdaScraper(GreenhouseScraper):
    employer_name = 'Lambda'
    EMPLOYER_KEY = 'lambda'


class XometryScraper(GreenhouseApiScraper):
    employer_name = 'Xometry'
    EMPLOYER_KEY = 'xometry'


class UniphoreScraper(LeverScraper):
    employer_name = 'Uniphore'
    EMPLOYER_KEY = 'uniphore'


class DialpadScraper(GreenhouseScraper):
    employer_name = 'Dialpad'
    EMPLOYER_KEY = 'dialpad'


class NorthspyreScraper(GreenhouseScraper):
    employer_name = 'Northspyre'
    EMPLOYER_KEY = 'northspyre'


class VendiaScraper(GreenhouseScraper):
    employer_name = 'Vendia'
    EMPLOYER_KEY = 'vendia'


class PingcapScraper(LeverScraper):
    employer_name = 'PingCAP'
    EMPLOYER_KEY = 'pingcap'


class ClearScraper(GreenhouseScraper):
    employer_name = 'Clear'
    EMPLOYER_KEY = 'clear'


class InnovaccerScraper(GreenhouseScraper):
    employer_name = 'Innovaccer'
    EMPLOYER_KEY = 'innovaccer'


class TheTradeDeskScraper(WorkdayScraper):
    employer_name = 'The Trade Desk'
    start_url = 'https://thetradedesk.wd5.myworkdayjobs.com/en-US/TTDExternalSite/'
    has_job_departments = False


class NovoScraper(GreenhouseScraper):
    employer_name = 'Novo'
    EMPLOYER_KEY = 'novo'


class MewsScraper(GreenhouseApiScraper):
    employer_name = 'Mews'
    EMPLOYER_KEY = 'mewssystems'


class CommvaultScraper(WorkdayScraper):
    employer_name = 'Commvault'
    start_url = 'https://commvault.wd1.myworkdayjobs.com/en-US/commvault/'
    has_job_departments = False


class AtlasTechnologyScraper(GreenhouseApiScraper):
    employer_name = 'Atlas Technology'
    EMPLOYER_KEY = 'atlasxhm'


class MiroScraper(GreenhouseApiScraper):
    employer_name = 'Miro'
    EMPLOYER_KEY = 'realtimeboardglobal'


class MatterportScraper(LeverScraper):
    employer_name = 'Matterport'
    EMPLOYER_KEY = 'matterport'


class CloudinaryScraper(LeverScraper):
    employer_name = 'Cloudinary'
    EMPLOYER_KEY = 'cloudinary'


class EnfusionScraper(GreenhouseApiScraper):
    employer_name = 'Enfusion'
    EMPLOYER_KEY = 'enfusion'


class IlluviumScraper(GreenhouseApiScraper):
    employer_name = 'Illuvium'
    EMPLOYER_KEY = 'illuvium'


class YubicoScraper(LeverScraper):
    employer_name = 'Yubico'
    EMPLOYER_KEY = 'yubico'


class SpaceAndTimeScraper(LeverScraper):
    employer_name = 'Space and Time'
    EMPLOYER_KEY = 'space-time'


class DarktraceScraper(GreenhouseScraper):
    employer_name = 'Darktrace'
    EMPLOYER_KEY = 'darktracelimited'


class VizAiScraper(GreenhouseApiScraper):
    employer_name = 'Viz.ai'
    EMPLOYER_KEY = 'vizai'


class HometogoScraper(GreenhouseScraper):
    employer_name = 'HomeToGo'
    EMPLOYER_KEY = 'hometogo'


class ShowpadScraper(GreenhouseScraper):
    employer_name = 'Showpad'
    EMPLOYER_KEY = 'showpad'


class KoboldMetalsScraper(GreenhouseScraper):
    employer_name = 'KoBold Metals'
    EMPLOYER_KEY = 'koboldmetals'


class KevinScraper(GreenhouseScraper):
    employer_name = 'kevin.'
    EMPLOYER_KEY = 'kevin'


class LocalKitchensScraper(LeverScraper):
    employer_name = 'Local Kitchens'
    EMPLOYER_KEY = 'localfoodgroup'


class KhanAcademyScraper(GreenhouseScraper):
    employer_name = 'Khan Academy'
    EMPLOYER_KEY = 'khanacademy'


class GroundtruthScraper(GreenhouseScraper):
    employer_name = 'GroundTruth'
    EMPLOYER_KEY = 'groundtruth'


class DatarobotScraper(WorkdayScraper):
    employer_name = 'DataRobot'
    start_url = 'https://datarobot.wd1.myworkdayjobs.com/en-US/DataRobot_External_Careers/'
    has_job_departments = False


class CialfoScraper(GreenhouseApiScraper):
    employer_name = 'Cialfo'
    EMPLOYER_KEY = 'cialfo'


class OrbitFabScraper(GreenhouseScraper):
    employer_name = 'Orbit Fab'
    EMPLOYER_KEY = 'orbitfab'


class TinesScraper(GreenhouseScraper):
    employer_name = 'Tines'
    EMPLOYER_KEY = 'tines'


class RadiantScraper(GreenhouseScraper):
    employer_name = 'Radiant'
    EMPLOYER_KEY = 'radiant'


class SosafeScraper(GreenhouseScraper):
    employer_name = 'SoSafe'
    EMPLOYER_KEY = 'sosafe'


class PlayplayScraper(LeverScraper):
    employer_name = 'PlayPlay'
    EMPLOYER_KEY = 'playplay'


class OrbitalTherapeuticsScraper(GreenhouseScraper):
    employer_name = 'Orbital Therapeutics'
    EMPLOYER_KEY = 'orbitaltherapeutics'


class ResilienceScraper(WorkdayScraper):
    employer_name = 'Resilience'
    start_url = 'https://resilience.wd1.myworkdayjobs.com/en-US/Resilience_Careers/'
    has_job_departments = False


class ShopbackScraper(LeverScraper):
    employer_name = 'ShopBack'
    EMPLOYER_KEY = 'shopback-2'


class SkyscannerScraper(GreenhouseApiScraper):
    employer_name = 'Skyscanner'
    EMPLOYER_KEY = 'skyscanner'


class GetirScraper(GreenhouseApiScraper):
    employer_name = 'Getir'
    EMPLOYER_KEY = 'getir'