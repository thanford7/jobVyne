from scrape.base_scrapers import AshbyHQScraper, GreenhouseApiScraper, GreenhouseScraper, JobviteScraper, LeverScraper, \
    SmartRecruitersScraper, \
    WorkdayScraper


class CohereScraper(LeverScraper):
    employer_name = 'Cohere'
    EMPLOYER_KEY = 'cohere'


class WealthfrontScraper(LeverScraper):
    employer_name = 'Wealthfront'
    EMPLOYER_KEY = 'wealthfront'


class YassirScraper(LeverScraper):
    employer_name = 'Yassir'
    EMPLOYER_KEY = 'Yassir'


class ArgentScraper(GreenhouseScraper):
    employer_name = 'Argent'
    EMPLOYER_KEY = 'argent'


class DunamuScraper(GreenhouseScraper):
    employer_name = 'Dunamu'
    EMPLOYER_KEY = 'dunamu'


class PayitScraper(GreenhouseApiScraper):
    employer_name = 'PayIt'
    EMPLOYER_KEY = 'payit'


class KraftonGameUnionScraper(GreenhouseScraper):
    employer_name = 'Krafton Game Union'
    EMPLOYER_KEY = 'pubgcorporation'


class TruecallerScraper(GreenhouseScraper):
    employer_name = 'Truecaller'
    EMPLOYER_KEY = 'truecaller'


class YummyScraper(LeverScraper):
    employer_name = 'Yummy'
    EMPLOYER_KEY = 'yummysuperapp'


class HqoScraper(AshbyHQScraper):
    employer_name = 'HqO'
    EMPLOYER_KEY = 'hqo'


class DataAiScraper(GreenhouseApiScraper):
    employer_name = 'Data.ai'
    EMPLOYER_KEY = 'dataai'


class GlanceScraper(GreenhouseScraper):
    employer_name = 'Glance'
    EMPLOYER_KEY = 'glance'


class VaroScraper(LeverScraper):
    employer_name = 'Varo'
    EMPLOYER_KEY = 'varomoney'


class PetCircleScraper(LeverScraper):
    employer_name = 'Pet Circle'
    EMPLOYER_KEY = 'petcircle'


class VoodooScraper(LeverScraper):
    employer_name = 'Voodoo'
    EMPLOYER_KEY = 'voodoo'


class UpstoxScraper(LeverScraper):
    employer_name = 'Upstox'
    EMPLOYER_KEY = 'upstox'


class IbottaScraper(WorkdayScraper):
    employer_name = 'Ibotta'
    start_url = 'https://ibotta.wd1.myworkdayjobs.com/en-US/Ibotta/'
    has_job_departments = False


class OnboardScraper(GreenhouseScraper):
    employer_name = 'OnBoard'
    EMPLOYER_KEY = 'onboardmeetings'


class JarScraper(LeverScraper):
    employer_name = 'Jar'
    EMPLOYER_KEY = 'jar-app'


class SaturnScraper(GreenhouseScraper):
    employer_name = 'Saturn'
    EMPLOYER_KEY = 'saturn'


class NoomScraper(GreenhouseApiScraper):
    employer_name = 'Noom'
    EMPLOYER_KEY = 'noomgrowth'


class TempoScraper(GreenhouseScraper):
    employer_name = 'Tempo'
    EMPLOYER_KEY = 'tempo'


class ScribdScraper(LeverScraper):
    employer_name = 'Scribd'
    EMPLOYER_KEY = 'scribd'


class LevelScraper(GreenhouseScraper):
    employer_name = 'Level'
    EMPLOYER_KEY = 'level'


class CarsBidsScraper(GreenhouseScraper):
    employer_name = 'Cars & Bids'
    EMPLOYER_KEY = 'carsandbids'


class ChownowScraper(LeverScraper):
    employer_name = 'ChowNow'
    EMPLOYER_KEY = 'chownow'


class TixrScraper(LeverScraper):
    employer_name = 'TIXR'
    EMPLOYER_KEY = 'Tixr'


class AndurilScraper(LeverScraper):
    employer_name = 'Anduril'
    EMPLOYER_KEY = 'anduril'


class DronedeployScraper(LeverScraper):
    employer_name = 'DroneDeploy'
    EMPLOYER_KEY = 'dronedeploy'


class MedableScraper(SmartRecruitersScraper):
    employer_name = 'Medable'
    EMPLOYER_KEY = 'Medable'


class LoopReturnsScraper(LeverScraper):
    employer_name = 'Loop Returns'
    EMPLOYER_KEY = 'loopreturns'


class ZolaScraper(GreenhouseApiScraper):
    employer_name = 'Zola'
    EMPLOYER_KEY = 'zola'


class BinanceUsScraper(GreenhouseScraper):
    employer_name = 'Binance.US'
    EMPLOYER_KEY = 'binanceus'


class LookoutScraper(GreenhouseApiScraper):
    employer_name = 'Lookout'
    EMPLOYER_KEY = 'lookout'


class PlacerAiScraper(GreenhouseApiScraper):
    employer_name = 'Placer.ai'
    EMPLOYER_KEY = 'placerlabs'


class LeagueappsScraper(GreenhouseApiScraper):
    employer_name = 'LeagueApps'
    EMPLOYER_KEY = 'leagueapps'


class AptosScraper(GreenhouseScraper):
    employer_name = 'Aptos'
    EMPLOYER_KEY = 'aptoslabs'


class StocktwitsScraper(GreenhouseApiScraper):
    employer_name = 'Stocktwits'
    EMPLOYER_KEY = 'stocktwits'


class AlayacareScraper(GreenhouseApiScraper):
    employer_name = 'AlayaCare'
    EMPLOYER_KEY = 'alayacare'


class LucidworksScraper(LeverScraper):
    employer_name = 'Lucidworks'
    EMPLOYER_KEY = 'lucidworks'


class GamblingComScraper(GreenhouseApiScraper):
    employer_name = 'Gambling.com'
    EMPLOYER_KEY = 'corporatecareers'


class DelphixScraper(LeverScraper):
    employer_name = 'Delphix'
    EMPLOYER_KEY = 'delphix'


class JustwatchScraper(LeverScraper):
    employer_name = 'JustWatch'
    EMPLOYER_KEY = 'justwatch'


class ArenaScraper(GreenhouseScraper):
    employer_name = 'Arena'
    EMPLOYER_KEY = 'arenaai'


class HealthCatalystScraper(WorkdayScraper):
    employer_name = 'Health Catalyst'
    start_url = 'https://healthcatalyst.wd5.myworkdayjobs.com/en-US/healthcatalystcareers/'
    has_job_departments = False


class HexScraper(GreenhouseApiScraper):
    employer_name = 'Hex'
    EMPLOYER_KEY = 'hextechnologies'


class DiscoScraper(GreenhouseApiScraper):
    employer_name = 'DISCO'
    EMPLOYER_KEY = 'disco'


class MantaScraper(GreenhouseScraper):
    employer_name = 'Manta'
    EMPLOYER_KEY = 'manta'


class RackspaceScraper(LeverScraper):
    employer_name = 'Rackspace'
    EMPLOYER_KEY = 'rackspace'


class GrinScraper(GreenhouseApiScraper):
    employer_name = 'Grin'
    EMPLOYER_KEY = 'grin'


class SignifydScraper(GreenhouseScraper):
    employer_name = 'Signifyd'
    EMPLOYER_KEY = 'signifyd95'


class OpnScraper(GreenhouseScraper):
    employer_name = 'Opn'
    EMPLOYER_KEY = 'opn'


class RightwayScraper(GreenhouseApiScraper):
    employer_name = 'Rightway'
    EMPLOYER_KEY = 'rightwayhealthcare'


class VectaraScraper(LeverScraper):
    employer_name = 'Vectara'
    EMPLOYER_KEY = 'vectara'


class FigmentScraper(GreenhouseScraper):
    employer_name = 'Figment'
    EMPLOYER_KEY = 'figment'


class AuvikNetworksScraper(GreenhouseApiScraper):
    employer_name = 'Auvik Networks'
    EMPLOYER_KEY = 'auviknetworks'


class OnehouseScraper(LeverScraper):
    employer_name = 'Onehouse'
    EMPLOYER_KEY = 'Onehouse'


class SpheraScraper(WorkdayScraper):
    employer_name = 'Sphera'
    start_url = 'https://sphera.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class TrueAnomalyScraper(GreenhouseScraper):
    employer_name = 'True Anomaly'
    EMPLOYER_KEY = 'trueanomalyinc'


class EverphoneScraper(GreenhouseScraper):
    employer_name = 'Everphone'
    EMPLOYER_KEY = 'everphone'


class ButterPaymentsScraper(LeverScraper):
    employer_name = 'Butter Payments'
    EMPLOYER_KEY = 'ButterPayments'


class WaymarkScraper(GreenhouseScraper):
    employer_name = 'Waymark'
    EMPLOYER_KEY = 'waymark'


class CoastScraper(GreenhouseScraper):
    employer_name = 'Coast'
    EMPLOYER_KEY = 'coast'


class CopperScraper(GreenhouseScraper):
    employer_name = 'Copper'
    EMPLOYER_KEY = 'copperco'


class VacasaScraper(GreenhouseApiScraper):
    employer_name = 'Vacasa'
    EMPLOYER_KEY = 'vacasa'


class QventusScraper(AshbyHQScraper):
    employer_name = 'Qventus'
    EMPLOYER_KEY = 'qventus'


class SynackScraper(GreenhouseScraper):
    employer_name = 'Synack'
    EMPLOYER_KEY = 'synack'


class BottomlineTechnologiesScraper(GreenhouseScraper):
    employer_name = 'Bottomline Technologies'
    EMPLOYER_KEY = 'bottomlinetechnologies'


class VoltronDataScraper(GreenhouseScraper):
    employer_name = 'Voltron Data'
    EMPLOYER_KEY = 'voltrondata'


class SelectStarScraper(AshbyHQScraper):
    employer_name = 'Select Star'
    EMPLOYER_KEY = 'selectstar'


class ImprobableScraper(LeverScraper):
    employer_name = 'Improbable'
    EMPLOYER_KEY = 'improbable'


class ZeroOneLabsScraper(GreenhouseScraper):
    employer_name = 'O(1) Labs'
    EMPLOYER_KEY = 'o1labs'


class TruenorthScraper(LeverScraper):
    employer_name = 'TrueNorth'
    EMPLOYER_KEY = 'truenorth'


class FarmwiseScraper(LeverScraper):
    employer_name = 'FarmWise'
    EMPLOYER_KEY = 'farmwise'


class BigpandaScraper(GreenhouseApiScraper):
    employer_name = 'BigPanda'
    EMPLOYER_KEY = 'bigpanda'


class TulipScraper(GreenhouseApiScraper):
    employer_name = 'Tulip'
    EMPLOYER_KEY = 'tulip'


class AuguryScraper(GreenhouseApiScraper):
    employer_name = 'Augury'
    EMPLOYER_KEY = 'augury'


class SimcorpScraper(WorkdayScraper):
    employer_name = 'SimCorp'
    start_url = 'https://simcorp.wd3.myworkdayjobs.com/en-US/SimCorp_Private/'
    has_job_departments = False


class OpenspaceScraper(GreenhouseApiScraper):
    employer_name = 'OpenSpace'
    EMPLOYER_KEY = 'openspace'


class LunoScraper(GreenhouseScraper):
    employer_name = 'Luno'
    EMPLOYER_KEY = 'luno'


class ConsensysScraper(GreenhouseApiScraper):
    employer_name = 'Consensys'
    EMPLOYER_KEY = 'consensys'


class KongScraper(LeverScraper):
    employer_name = 'Kong'
    EMPLOYER_KEY = 'kong'


class EthosScraper(GreenhouseScraper):
    employer_name = 'Ethos'
    EMPLOYER_KEY = 'ethoslife'


class SpruceScraper(LeverScraper):
    employer_name = 'Spruce'
    EMPLOYER_KEY = 'sprucesystems'


class SwiftlyScraper(LeverScraper):
    employer_name = 'Swiftly'
    EMPLOYER_KEY = 'SwiftlySystems'


class ClickhouseScraper(GreenhouseScraper):
    employer_name = 'ClickHouse'
    EMPLOYER_KEY = 'clickhouse'


class AcxiomScraper(WorkdayScraper):
    employer_name = 'Acxiom'
    start_url = 'https://acxiomllc.wd5.myworkdayjobs.com/en-US/AcxiomUSA/'
    has_job_departments = False


class ForgerockScraper(GreenhouseScraper):
    employer_name = 'ForgeRock'
    EMPLOYER_KEY = 'forgerock'


class GraylogScraper(LeverScraper):
    employer_name = 'Graylog'
    EMPLOYER_KEY = 'graylog'


class CoreweaveScraper(GreenhouseScraper):
    employer_name = 'CoreWeave'
    EMPLOYER_KEY = 'coreweave'


class WeedmapsScraper(GreenhouseScraper):
    employer_name = 'Weedmaps'
    EMPLOYER_KEY = 'weedmaps77'


class WildlifeStudiosScraper(GreenhouseScraper):
    employer_name = 'Wildlife Studios'
    EMPLOYER_KEY = 'wildlifestudios'


class ZeroXScraper(GreenhouseScraper):
    employer_name = '0x'
    EMPLOYER_KEY = '0x'


class CaptivateiqScraper(LeverScraper):
    employer_name = 'CaptivateIQ'
    EMPLOYER_KEY = 'captivateiq'


class DutchieScraper(GreenhouseScraper):
    employer_name = 'Dutchie'
    EMPLOYER_KEY = 'thedutchie'


class BiltRewardsScraper(GreenhouseScraper):
    employer_name = 'Bilt Rewards'
    EMPLOYER_KEY = 'biltrewards'


class SinglestoreScraper(GreenhouseScraper):
    employer_name = 'SingleStore'
    EMPLOYER_KEY = 'singlestore'


class MyntraScraper(GreenhouseScraper):
    employer_name = 'Myntra'
    EMPLOYER_KEY = 'myntra'


class MemzoScraper(GreenhouseScraper):
    employer_name = 'Memzo'
    EMPLOYER_KEY = 'mezmo'


class ForgeScraper(GreenhouseScraper):
    employer_name = 'Forge'
    EMPLOYER_KEY = 'forgeglobal'


class EnvestnetScraper(WorkdayScraper):
    employer_name = 'Envestnet'
    start_url = 'https://envestnet.wd5.myworkdayjobs.com/en-US/ENV/'
    has_job_departments = False


class AppomniScraper(GreenhouseApiScraper):
    employer_name = 'AppOmni'
    EMPLOYER_KEY = 'appomni'


class QlikScraper(JobviteScraper):
    employer_name = 'Qlik'
    EMPLOYER_KEY = 'qlik'


class TrumidScraper(GreenhouseApiScraper):
    employer_name = 'Trumid'
    EMPLOYER_KEY = 'trumid'


class ThreatlockerScraper(GreenhouseScraper):
    employer_name = 'ThreatLocker'
    EMPLOYER_KEY = 'threatlocker'


class XsollaScraper(LeverScraper):
    employer_name = 'Xsolla'
    EMPLOYER_KEY = 'xsolla'


class KrakenScraper(LeverScraper):
    employer_name = 'Kraken'
    EMPLOYER_KEY = 'kraken'


class WeworkScraper(GreenhouseScraper):
    employer_name = 'WeWork'
    EMPLOYER_KEY = 'wework'
