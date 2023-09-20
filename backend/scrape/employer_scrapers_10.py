from scrape.base_scrapers import AshbyHQApiV2Scraper, AshbyHQScraper, GreenhouseApiScraper, GreenhouseScraper, \
    LeverScraper, \
    SmartRecruitersApiScraper, SmartRecruitersScraper, WorkdayScraper


class AlpacaScraper(GreenhouseScraper):
    employer_name = 'Alpaca'
    EMPLOYER_KEY = 'alpaca'


class SimpplrScraper(GreenhouseScraper):
    employer_name = 'Simpplr'
    EMPLOYER_KEY = 'simpplr'


class GeneralCatalystScraper(GreenhouseScraper):
    employer_name = 'General Catalyst'
    EMPLOYER_KEY = 'generalcatalyst'


class ArcadiaScraper(GreenhouseScraper):
    employer_name = 'Arcadia'
    EMPLOYER_KEY = 'arcadiacareers'


class CodeAndTheoryScraper(GreenhouseApiScraper):
    employer_name = 'Code and Theory'
    EMPLOYER_KEY = 'codeandtheory'


class SofiScraper(GreenhouseApiScraper):
    employer_name = 'SoFi'
    EMPLOYER_KEY = 'sofi'


class FilmhubScraper(AshbyHQApiV2Scraper):
    employer_name = 'Filmhub'
    EMPLOYER_KEY = 'filmhub'


class TrabaScraper(LeverScraper):
    employer_name = 'Traba'
    EMPLOYER_KEY = 'Traba'


class WorldcoinScraper(GreenhouseScraper):
    employer_name = 'Worldcoin'
    EMPLOYER_KEY = 'worldcoinorg'


class OrumScraper(GreenhouseApiScraper):
    employer_name = 'Orum'
    EMPLOYER_KEY = 'orum'


class AnrokScraper(AshbyHQApiV2Scraper):
    employer_name = 'Anrok'
    EMPLOYER_KEY = 'anrok'


class MonduScraper(GreenhouseScraper):
    employer_name = 'Mondu'
    EMPLOYER_KEY = 'monduai'


class TruelayerScraper(GreenhouseApiScraper):
    employer_name = 'TrueLayer'
    EMPLOYER_KEY = 'truelayer'


class TulScraper(LeverScraper):
    employer_name = 'Tul'
    EMPLOYER_KEY = 'Tul'


class AboduScraper(GreenhouseScraper):
    employer_name = 'Abodu'
    EMPLOYER_KEY = 'abodu'


class NymbusScraper(GreenhouseApiScraper):
    employer_name = 'Nymbus'
    EMPLOYER_KEY = 'nymbusinc'


class BetaTechScraper(LeverScraper):
    employer_name = 'Beta Tech'
    EMPLOYER_KEY = 'beta'


class NexiiScraper(LeverScraper):
    employer_name = 'Nexii'
    EMPLOYER_KEY = 'nexii'


class SaltSecurityScraper(GreenhouseApiScraper):
    employer_name = 'Salt Security'
    EMPLOYER_KEY = 'saltsecurity'


class SeldonScraper(GreenhouseScraper):
    employer_name = 'Seldon'
    EMPLOYER_KEY = 'seldon'


class SubmittableScraper(GreenhouseScraper):
    employer_name = 'Submittable'
    EMPLOYER_KEY = 'submittable'


class ZenotiScraper(GreenhouseScraper):
    employer_name = 'Zenoti'
    EMPLOYER_KEY = 'zenoti'


class ClassdojoScraper(GreenhouseScraper):
    employer_name = 'ClassDojo'
    EMPLOYER_KEY = 'classdojo'


class ClearwaterAnalyticsScraper(WorkdayScraper):
    employer_name = 'Clearwater Analytics'
    start_url = 'https://clearwateranalytics.wd1.myworkdayjobs.com/en-US/Clearwater_Analytics_Careers/'
    has_job_departments = False


class RoofstockScraper(LeverScraper):
    employer_name = 'Roofstock'
    EMPLOYER_KEY = 'roofstock'


class AuroraSolarScraper(AshbyHQApiV2Scraper):
    employer_name = 'Aurora Solar'
    EMPLOYER_KEY = 'aurorasolar'


class CheggScraper(WorkdayScraper):
    employer_name = 'Chegg'
    start_url = 'https://osv-chegg.wd5.myworkdayjobs.com/en-US/Chegg/'
    has_job_departments = False


class AirbyteScraper(GreenhouseScraper):
    employer_name = 'Airbyte'
    EMPLOYER_KEY = 'airbyte'


class JumpcloudScraper(LeverScraper):
    employer_name = 'JumpCloud'
    EMPLOYER_KEY = 'jumpcloud'


class NcinoScraper(WorkdayScraper):
    employer_name = 'nCino'
    start_url = 'https://ncino.wd5.myworkdayjobs.com/en-US/nCinoCareers/'
    has_job_departments = False


class GenerallyIntelligentScraper(LeverScraper):
    employer_name = 'Generally Intelligent'
    EMPLOYER_KEY = 'generallyintelligent'


class AuraScraper(GreenhouseApiScraper):
    employer_name = 'Aura'
    EMPLOYER_KEY = 'aura'


class ApolloAgricultureScraper(LeverScraper):
    employer_name = 'Apollo Agriculture'
    EMPLOYER_KEY = 'apolloagriculture'


class ContrastSecurityScraper(LeverScraper):
    employer_name = 'Contrast Security'
    EMPLOYER_KEY = 'contrastsecurity'


class TheskimmScraper(GreenhouseApiScraper):
    employer_name = 'theSkimm'
    EMPLOYER_KEY = 'theskimm'


class ParallelLearningScraper(GreenhouseScraper):
    employer_name = 'Parallel Learning'
    EMPLOYER_KEY = 'parallellearning'


class DatadomeScraper(GreenhouseApiScraper):
    employer_name = 'DataDome'
    EMPLOYER_KEY = 'ddome'


class PolygonScraper(LeverScraper):
    employer_name = 'Polygon'
    EMPLOYER_KEY = 'Polygon'


class McafeeScraper(WorkdayScraper):
    employer_name = 'McAfee'
    start_url = 'https://mcafee.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class WaveMobileScraper(GreenhouseApiScraper):
    employer_name = 'Wave Mobile'
    EMPLOYER_KEY = 'wavemm1'


class SmallDoorScraper(GreenhouseScraper):
    employer_name = 'Small Door'
    EMPLOYER_KEY = 'smalldoor'


class SolarisbankScraper(GreenhouseScraper):
    employer_name = 'Solarisbank'
    EMPLOYER_KEY = 'solarisbank'


class RstudioScraper(GreenhouseApiScraper):
    employer_name = 'RStudio'
    EMPLOYER_KEY = 'rstudio'


class CollectiveScraper(GreenhouseApiScraper):
    employer_name = 'Collective'
    EMPLOYER_KEY = 'collectiveinc'


class MrbeastScraper(GreenhouseScraper):
    employer_name = 'MrBeast'
    EMPLOYER_KEY = 'mrbeastyoutube'


class SixSenseScraper(GreenhouseApiScraper):
    employer_name = '6Sense'
    EMPLOYER_KEY = '6sense'


class TierScraper(GreenhouseScraper):
    employer_name = 'Tier'
    EMPLOYER_KEY = 'tiermobility'


class PicnichealthScraper(GreenhouseApiScraper):
    employer_name = 'PicnicHealth'
    EMPLOYER_KEY = 'picnichealth'


class PactumScraper(GreenhouseScraper):
    employer_name = 'Pactum'
    EMPLOYER_KEY = 'pactum'


class GeneralAtlanticScraper(GreenhouseScraper):
    employer_name = 'General Atlantic'
    EMPLOYER_KEY = 'generalatlantic'


class SellerxScraper(GreenhouseApiScraper):
    employer_name = 'SellerX'
    EMPLOYER_KEY = 'sellerx'


class IdeoScraper(GreenhouseApiScraper):
    employer_name = 'IDEO'
    EMPLOYER_KEY = 'ideo'


class MavenSecuritiesScraper(GreenhouseScraper):
    employer_name = 'Maven Securities'
    EMPLOYER_KEY = 'mavensecuritiesholdingltd'


class BillieScraper(GreenhouseApiScraper):
    employer_name = 'Billie'
    EMPLOYER_KEY = 'billie'


class PricelineScraper(WorkdayScraper):
    employer_name = 'Priceline'
    start_url = 'https://priceline.wd1.myworkdayjobs.com/en-US/Priceline/'
    has_job_departments = False


class SisenseScraper(GreenhouseApiScraper):
    employer_name = 'Sisense'
    EMPLOYER_KEY = 'sisense'


class SynapseScraper(LeverScraper):
    employer_name = 'Synapse'
    EMPLOYER_KEY = 'synapsefi'


class XenditScraper(GreenhouseScraper):
    employer_name = 'Xendit'
    EMPLOYER_KEY = 'xendit'


class BuildopsScraper(GreenhouseApiScraper):
    employer_name = 'BuildOps'
    EMPLOYER_KEY = 'buildops'


class OvoEnergyScraper(GreenhouseApiScraper):
    employer_name = 'Ovo Energy'
    EMPLOYER_KEY = 'ovoenergy'


class OpendoorScraper(GreenhouseScraper):
    employer_name = 'OpenDoor'
    EMPLOYER_KEY = 'opendoor'


class CargurusScraper(GreenhouseScraper):
    employer_name = 'CarGurus'
    EMPLOYER_KEY = 'cargurus'


class AcornsScraper(GreenhouseApiScraper):
    employer_name = 'Acorns'
    EMPLOYER_KEY = 'acorns'


class LinearbScraper(LeverScraper):
    employer_name = 'LinearB'
    EMPLOYER_KEY = 'LinearB'


class EpisodeSixScraper(GreenhouseScraper):
    employer_name = 'Episode Six'
    EMPLOYER_KEY = 'episodesixlinkedin'


class InnovusionScraper(GreenhouseScraper):
    employer_name = 'Innovusion'
    EMPLOYER_KEY = 'innovusion'


class BrightHealthScraper(GreenhouseScraper):
    employer_name = 'Bright Health'
    EMPLOYER_KEY = 'brighthealthgroup'


class MetalScraper(LeverScraper):
    employer_name = 'Metal'
    EMPLOYER_KEY = 'metallicus'


class JuniperSquareScraper(AshbyHQApiV2Scraper):
    employer_name = 'Juniper Square'
    EMPLOYER_KEY = 'junipersquare'


class SnowplowScraper(LeverScraper):
    employer_name = 'Snowplow'
    EMPLOYER_KEY = 'snowplow'


class LogzScraper(LeverScraper):
    employer_name = 'Logz'
    EMPLOYER_KEY = 'logz'


class GoodrxScraper(LeverScraper):
    employer_name = 'GoodRx'
    EMPLOYER_KEY = 'goodrx'


class MeramaScraper(GreenhouseScraper):
    employer_name = 'Merama'
    EMPLOYER_KEY = 'merama'


class KaratFinancialScraper(GreenhouseScraper):
    employer_name = 'Karat Financial'
    EMPLOYER_KEY = 'trykarat'


class NowstaScraper(GreenhouseScraper):
    employer_name = 'Nowsta'
    EMPLOYER_KEY = 'nowsta'


class HouseRxScraper(GreenhouseApiScraper):
    employer_name = 'House Rx'
    EMPLOYER_KEY = 'houserx'


class CandyScraper(GreenhouseScraper):
    employer_name = 'Candy'
    EMPLOYER_KEY = 'candy'


class NextrollScraper(GreenhouseScraper):
    employer_name = 'Nextroll'
    EMPLOYER_KEY = 'nextroll'


class LiltScraper(AshbyHQApiV2Scraper):
    employer_name = 'Lilt'
    EMPLOYER_KEY = 'lilt'


class ParadigmScraper(AshbyHQApiV2Scraper):
    employer_name = 'Paradigm'
    EMPLOYER_KEY = 'Paradigm'


class TwentyOneCoScraper(GreenhouseApiScraper):
    employer_name = '21.co'
    EMPLOYER_KEY = '21co'


class ExoScraper(GreenhouseScraper):
    employer_name = 'Exo'
    EMPLOYER_KEY = 'exo'


class WrikeScraper(GreenhouseScraper):
    employer_name = 'Wrike'
    EMPLOYER_KEY = 'wrike'


class UserInterviewsScraper(GreenhouseScraper):
    employer_name = 'User Interviews'
    EMPLOYER_KEY = 'userinterviews'


class BiorenderScraper(LeverScraper):
    employer_name = 'BioRender'
    EMPLOYER_KEY = 'biorender'


class AbacumScraper(GreenhouseApiScraper):
    employer_name = 'Abacum'
    EMPLOYER_KEY = 'abacum'


class ChordScraper(LeverScraper):
    employer_name = 'Chord'
    EMPLOYER_KEY = 'Chord'


class GalaxyDigitalScraper(GreenhouseScraper):
    employer_name = 'Galaxy Digital'
    EMPLOYER_KEY = 'galaxydigitalservices'


class RezoScraper(LeverScraper):
    employer_name = 'Rezo'
    EMPLOYER_KEY = 'rezotx'


class RothysScraper(GreenhouseScraper):
    employer_name = 'Rothy\'s'
    EMPLOYER_KEY = 'rothys'


class PproScraper(LeverScraper):
    employer_name = 'PPRO'
    EMPLOYER_KEY = 'ppro'


class WahedScraper(LeverScraper):
    employer_name = 'Wahed'
    EMPLOYER_KEY = 'wahed.com'


class MuralScraper(GreenhouseScraper):
    employer_name = 'Mural'
    EMPLOYER_KEY = 'mural'


class StacklineScraper(GreenhouseScraper):
    employer_name = 'Stackline'
    EMPLOYER_KEY = 'stackline'


class JustanswerScraper(GreenhouseScraper):
    employer_name = 'JustAnswer'
    EMPLOYER_KEY = 'justanswer'


class KindbodyScraper(GreenhouseScraper):
    employer_name = 'Kindbody'
    EMPLOYER_KEY = 'kindbody'


class MaltScraper(LeverScraper):
    employer_name = 'Malt'
    EMPLOYER_KEY = 'malt'


class ParcellabScraper(LeverScraper):
    employer_name = 'parcelLab'
    EMPLOYER_KEY = 'parcellab'


class GreenhouseAtsScraper(GreenhouseScraper):
    employer_name = 'Greenhouse'
    EMPLOYER_KEY = 'greenhouse'


class WorldremitScraper(WorkdayScraper):
    employer_name = 'WorldRemit'
    start_url = 'https://worldremit.wd3.myworkdayjobs.com/en-US/WRCareers/'
    has_job_departments = False


class GodaddyScraper(GreenhouseApiScraper):
    employer_name = 'Godaddy'
    EMPLOYER_KEY = 'godaddy'


class TokuScraper(LeverScraper):
    employer_name = 'Toku'
    EMPLOYER_KEY = 'toku'


class OysterScraper(GreenhouseApiScraper):
    employer_name = 'Oyster'
    EMPLOYER_KEY = 'oyster'


class ThredupScraper(WorkdayScraper):
    employer_name = 'ThredUp'
    start_url = 'https://thredup.wd1.myworkdayjobs.com/en-US/thredup_Careers/'
    has_job_departments = False


class JupiterScraper(LeverScraper):
    employer_name = 'Jupiter'
    EMPLOYER_KEY = 'jupiter'


class ZopaScraper(LeverScraper):
    employer_name = 'Zopa'
    EMPLOYER_KEY = 'zopa'


class ZumScraper(LeverScraper):
    employer_name = 'Zum'
    EMPLOYER_KEY = 'ridezum'


class BrowserstackScraper(WorkdayScraper):
    employer_name = 'BrowserStack'
    start_url = 'https://browserstack.wd3.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class MarqetaScraper(GreenhouseScraper):
    employer_name = 'Marqeta'
    EMPLOYER_KEY = 'marqeta'


class VerisignScraper(GreenhouseScraper):
    employer_name = 'Verisign'
    EMPLOYER_KEY = 'verisign'


class PayfitScraper(LeverScraper):
    employer_name = 'PayFit'
    EMPLOYER_KEY = 'payfit'


class UniversalHydrogenScraper(GreenhouseApiScraper):
    employer_name = 'Universal Hydrogen'
    EMPLOYER_KEY = 'universalhydrogen'


class WalkmeScraper(LeverScraper):
    employer_name = 'WalkMe'
    EMPLOYER_KEY = 'walkme'


class YextScraper(GreenhouseScraper):
    employer_name = 'Yext'
    EMPLOYER_KEY = 'yext'


class PaystackScraper(GreenhouseScraper):
    employer_name = 'Paystack'
    EMPLOYER_KEY = 'paystack'


class UpsideFoodsScraper(GreenhouseScraper):
    employer_name = 'Upside Foods'
    EMPLOYER_KEY = 'memphismeats'


class ZwiftScraper(GreenhouseApiScraper):
    employer_name = 'Zwift'
    EMPLOYER_KEY = 'zwift'


class BitsoScraper(GreenhouseApiScraper):
    employer_name = 'Bitso'
    EMPLOYER_KEY = 'bitso'


class EquipScraper(LeverScraper):
    employer_name = 'Equip'
    EMPLOYER_KEY = 'equiphealth'


class Unit4Scraper(SmartRecruitersScraper):
    employer_name = 'Unit4'
    EMPLOYER_KEY = 'Unit44'


class ConductorScraper(GreenhouseScraper):
    employer_name = 'Conductor'
    EMPLOYER_KEY = 'conductor'


class FoundationScraper(LeverScraper):
    employer_name = 'Foundation'
    EMPLOYER_KEY = 'with-foundation'


class MetamapScraper(GreenhouseScraper):
    employer_name = 'MetaMap'
    EMPLOYER_KEY = 'metamap'


class HeroesScraper(GreenhouseScraper):
    employer_name = 'Heroes'
    EMPLOYER_KEY = 'heroes'


class ZampFinanceScraper(AshbyHQApiV2Scraper):
    employer_name = 'Zamp Finance'
    EMPLOYER_KEY = 'zamp'


class PublicScraper(GreenhouseScraper):
    employer_name = 'Public'
    EMPLOYER_KEY = 'public'


class TeadsScraper(GreenhouseApiScraper):
    employer_name = 'Teads'
    EMPLOYER_KEY = 'teads'


class SearchlightScraper(AshbyHQApiV2Scraper):
    employer_name = 'Searchlight'
    EMPLOYER_KEY = 'searchlight'


class BonuslyScraper(LeverScraper):
    employer_name = 'Bonusly'
    EMPLOYER_KEY = 'bonusly'


class HuntressScraper(GreenhouseScraper):
    employer_name = 'Huntress'
    EMPLOYER_KEY = 'huntress'


class ATeamScraper(LeverScraper):
    employer_name = 'A.Team'
    EMPLOYER_KEY = 'a'


class KinexonScraper(GreenhouseApiScraper):
    employer_name = 'Kinexon'
    EMPLOYER_KEY = 'kinexon'


class CarrotScraper(GreenhouseScraper):
    employer_name = 'Carrot'
    EMPLOYER_KEY = 'carrotfertility'


class VueStorefrontScraper(GreenhouseApiScraper):
    employer_name = 'Vue Storefront'
    EMPLOYER_KEY = 'vuestorefront'


class WorkhumanScraper(WorkdayScraper):
    employer_name = 'Workhuman'
    start_url = 'https://workhuman.wd1.myworkdayjobs.com/en-US/WorkhumanCareers/'
    has_job_departments = False


class ObieScraper(LeverScraper):
    employer_name = 'Obie'
    EMPLOYER_KEY = 'Obie'


class BraveScraper(GreenhouseScraper):
    employer_name = 'Brave'
    EMPLOYER_KEY = 'brave'


class LessenScraper(LeverScraper):
    employer_name = 'Lessen'
    EMPLOYER_KEY = 'lessen'


class MathpressoScraper(LeverScraper):
    employer_name = 'Mathpresso'
    EMPLOYER_KEY = 'mathpresso'


class DoceboScraper(LeverScraper):
    employer_name = 'Docebo'
    EMPLOYER_KEY = 'docebo'


class CamblyScraper(LeverScraper):
    employer_name = 'Cambly'
    EMPLOYER_KEY = 'cambly'


class MicrostrategyScraper(SmartRecruitersScraper):
    employer_name = 'MicroStrategy'
    EMPLOYER_KEY = 'MicroStrategy1'


class EnvoyScraper(GreenhouseScraper):
    employer_name = 'Envoy'
    EMPLOYER_KEY = 'envoy'


class NgrokScraper(GreenhouseScraper):
    employer_name = 'Ngrok'
    EMPLOYER_KEY = 'ngrokinc'


class OdaScraper(LeverScraper):
    employer_name = 'Oda'
    EMPLOYER_KEY = 'oda'


class DWaveScraper(LeverScraper):
    employer_name = 'D-Wave'
    EMPLOYER_KEY = 'dwavesys'


class YokoyScraper(LeverScraper):
    employer_name = 'Yokoy'
    EMPLOYER_KEY = 'yokoy'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class UdacityScraper(GreenhouseScraper):
    employer_name = 'Udacity'
    EMPLOYER_KEY = 'udacity'


class KinInsuranceScraper(GreenhouseScraper):
    employer_name = 'Kin Insurance'
    EMPLOYER_KEY = 'kininsurance'


class MeridianlinkScraper(LeverScraper):
    employer_name = 'MeridianLink'
    EMPLOYER_KEY = 'meridianlink'


class HivemapperScraper(LeverScraper):
    employer_name = 'Hivemapper'
    EMPLOYER_KEY = 'Hivemapper'


class InfobipScraper(WorkdayScraper):
    employer_name = 'Infobip'
    start_url = 'https://infobip.wd3.myworkdayjobs.com/en-US/InfobipCareers/'
    has_job_departments = False


class BamboohrScraper(GreenhouseScraper):
    employer_name = 'BambooHR'
    EMPLOYER_KEY = 'bamboohr17'


class PraxisScraper(AshbyHQApiV2Scraper):
    employer_name = 'Praxis'
    EMPLOYER_KEY = 'Praxis'


class KyteScraper(LeverScraper):
    employer_name = 'Kyte'
    EMPLOYER_KEY = 'kyte'


class MintHouseScraper(GreenhouseScraper):
    employer_name = 'Mint House'
    EMPLOYER_KEY = 'minthouse'


class LightningAiScraper(GreenhouseScraper):
    employer_name = 'Lightning AI'
    EMPLOYER_KEY = 'lightningai'


class ColumnScraper(AshbyHQApiV2Scraper):
    employer_name = 'Column'
    EMPLOYER_KEY = 'column'


class SkilljarScraper(GreenhouseScraper):
    employer_name = 'Skilljar'
    EMPLOYER_KEY = 'skilljar'


class PetraScraper(GreenhouseScraper):
    employer_name = 'Petra'
    EMPLOYER_KEY = 'petra'


class VimeoScraper(GreenhouseScraper):
    employer_name = 'Vimeo'
    EMPLOYER_KEY = 'vimeo'


class HomebaseScraper(GreenhouseScraper):
    employer_name = 'Homebase'
    EMPLOYER_KEY = 'homebase'


class SociScraper(GreenhouseApiScraper):
    employer_name = 'Soci'
    EMPLOYER_KEY = 'soci'


class WorkosScraper(LeverScraper):
    employer_name = 'WorkOS'
    EMPLOYER_KEY = 'workos'


class DovetailScraper(GreenhouseScraper):
    employer_name = 'Dovetail'
    EMPLOYER_KEY = 'dovetail'


class CircleCoScraper(LeverScraper):
    employer_name = 'Circle'
    EMPLOYER_KEY = 'circleco'


class SubstackScraper(GreenhouseScraper):
    employer_name = 'Substack'
    EMPLOYER_KEY = 'substack'


class LeapsomeScraper(AshbyHQApiV2Scraper):
    employer_name = 'Leapsome'
    EMPLOYER_KEY = 'Leapsome'


class ItalicScraper(AshbyHQApiV2Scraper):
    employer_name = 'Italic'
    EMPLOYER_KEY = 'italic'


class SecurityscorecardScraper(GreenhouseApiScraper):
    employer_name = 'SecurityScorecard'
    EMPLOYER_KEY = 'securityscorecard'


class HouzzScraper(WorkdayScraper):
    employer_name = 'Houzz'
    start_url = 'https://houzz.wd5.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class Op3nScraper(GreenhouseScraper):
    employer_name = 'OP3N'
    EMPLOYER_KEY = 'op3n'


class SorareScraper(AshbyHQApiV2Scraper):
    employer_name = 'Sorare'
    EMPLOYER_KEY = 'sorare'


class SofarScraper(GreenhouseScraper):
    employer_name = 'Sofar'
    EMPLOYER_KEY = 'sofarocean'


class TradelinkScraper(LeverScraper):
    employer_name = 'TradeLink'
    EMPLOYER_KEY = 'tradelink'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class KalshiScraper(GreenhouseApiScraper):
    employer_name = 'Kalshi'
    EMPLOYER_KEY = 'kalshi'


class StrapiScraper(LeverScraper):
    employer_name = 'Strapi'
    EMPLOYER_KEY = 'strapi'


class CorvusInsuranceScraper(AshbyHQApiV2Scraper):
    employer_name = 'Corvus Insurance'
    EMPLOYER_KEY = 'corvus'


class BraintrustScraper(GreenhouseApiScraper):
    employer_name = 'Braintrust'
    EMPLOYER_KEY = 'braintrustcore'


class BounceScraper(LeverScraper):
    employer_name = 'Bounce'
    EMPLOYER_KEY = 'use-bounce'


class GeneralAssemblyScraper(GreenhouseScraper):
    employer_name = 'General Assembly'
    EMPLOYER_KEY = 'generalassembly'


class StravaScraper(GreenhouseScraper):
    employer_name = 'Strava'
    EMPLOYER_KEY = 'strava'


class AcademiaScraper(LeverScraper):
    employer_name = 'Academia'
    EMPLOYER_KEY = 'academia'


class FinixScraper(LeverScraper):
    employer_name = 'Finix'
    EMPLOYER_KEY = 'finix'


class AxioScraper(GreenhouseApiScraper):
    employer_name = 'Axio'
    EMPLOYER_KEY = 'axio'


class CalderaScraper(AshbyHQApiV2Scraper):
    employer_name = 'Caldera'
    EMPLOYER_KEY = 'Caldera'


class LobScraper(GreenhouseApiScraper):
    employer_name = 'Lob'
    EMPLOYER_KEY = 'lob'


class HavenlyScraper(GreenhouseScraper):
    employer_name = 'Havenly'
    EMPLOYER_KEY = 'havenly'


class LeagueScraper(GreenhouseScraper):
    employer_name = 'League'
    EMPLOYER_KEY = 'leagueinc'


class NaturesFyndScraper(LeverScraper):
    employer_name = 'Nature\'s Fynd'
    EMPLOYER_KEY = 'naturesfynd'


class SubspaceLabsScraper(LeverScraper):
    employer_name = 'Subspace Labs'
    EMPLOYER_KEY = 'subspacelabs'


class KikoffScraper(LeverScraper):
    employer_name = 'Kikoff'
    EMPLOYER_KEY = 'kikoff'


class ObservableScraper(LeverScraper):
    employer_name = 'Observable'
    EMPLOYER_KEY = 'observablehq'


class KeyfactorScraper(GreenhouseScraper):
    employer_name = 'Keyfactor'
    EMPLOYER_KEY = 'keyfactorinc'


class MuckRackScraper(GreenhouseScraper):
    employer_name = 'Muck Rack'
    EMPLOYER_KEY = 'muckrack'


class AbTastyScraper(LeverScraper):
    employer_name = 'AB Tasty'
    EMPLOYER_KEY = 'abtasty'


class JerryScraper(AshbyHQApiV2Scraper):
    employer_name = 'Jerry'
    EMPLOYER_KEY = 'Jerry'


class CollectorsScraper(GreenhouseScraper):
    employer_name = 'Collectors'
    EMPLOYER_KEY = 'collectorsuniverse'


class SylndrScraper(LeverScraper):
    employer_name = 'Sylndr'
    EMPLOYER_KEY = 'sylndr'


class GudangadaScraper(SmartRecruitersScraper):
    employer_name = 'GudangAda'
    EMPLOYER_KEY = 'GudangAda'


class OmioScraper(SmartRecruitersApiScraper):
    employer_name = 'Omio'
    EMPLOYER_KEY = 'Omio1'


class JellysmackScraper(LeverScraper):
    employer_name = 'Jellysmack'
    EMPLOYER_KEY = 'jellysmack'


class BluesWirelessScraper(LeverScraper):
    employer_name = 'Blues Wireless'
    EMPLOYER_KEY = 'BluesInc'


class AllRaiseScraper(LeverScraper):
    employer_name = 'All Raise'
    EMPLOYER_KEY = 'allraise'
