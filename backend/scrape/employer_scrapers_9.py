from scrape.base_scrapers import AshbyHQScraper, GreenhouseApiScraper, GreenhouseScraper, JobviteScraper, LeverScraper, \
    RipplingAtsScraper, SmartRecruitersScraper, \
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


class FlexeraScraper(WorkdayScraper):
    employer_name = 'Flexera'
    start_url = 'https://flexerasoftware.wd1.myworkdayjobs.com/en-US/FlexeraSoftware/'
    has_job_departments = False


class YahooScraper(WorkdayScraper):
    employer_name = 'Yahoo'
    start_url = 'https://ouryahoo.wd5.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class ActivisionScraper(WorkdayScraper):
    employer_name = 'Activision Blizzard'
    start_url = 'https://activision.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class StockxScraper(GreenhouseScraper):
    employer_name = 'StockX'
    EMPLOYER_KEY = 'stockx'


class WefoxScraper(GreenhouseApiScraper):
    employer_name = 'wefox'
    EMPLOYER_KEY = 'wefoxgroup'


class CitizenScraper(GreenhouseScraper):
    employer_name = 'Citizen'
    EMPLOYER_KEY = 'citizen'


class EspressoSystemsScraper(LeverScraper):
    employer_name = 'Espresso Systems'
    EMPLOYER_KEY = 'Espresso'


class VaynermediaScraper(GreenhouseScraper):
    employer_name = 'VaynerMedia'
    EMPLOYER_KEY = 'vaynermedia'


class VergesenseScraper(LeverScraper):
    employer_name = 'VergeSense'
    EMPLOYER_KEY = 'vergesense'


class DnanexusScraper(SmartRecruitersScraper):
    employer_name = 'DNAnexus'
    EMPLOYER_KEY = 'DNAnexus'


class AnkrScraper(GreenhouseScraper):
    employer_name = 'Ankr'
    EMPLOYER_KEY = 'ankrnetwork'


class AtaccamaScraper(LeverScraper):
    employer_name = 'Ataccama'
    EMPLOYER_KEY = 'ataccama'


class InceptioScraper(GreenhouseScraper):
    employer_name = 'Inceptio'
    EMPLOYER_KEY = 'inceptiotechnology'


class FlippScraper(GreenhouseApiScraper):
    employer_name = 'Flipp'
    EMPLOYER_KEY = 'flipp'


class JobgetScraper(GreenhouseScraper):
    employer_name = 'JobGet'
    EMPLOYER_KEY = 'jobget'


class LatchbioScraper(LeverScraper):
    employer_name = 'LatchBio'
    EMPLOYER_KEY = 'latch'


class ForethoughtScraper(GreenhouseScraper):
    employer_name = 'Forethought'
    EMPLOYER_KEY = 'forethought'


class ZenjobScraper(GreenhouseScraper):
    employer_name = 'Zenjob'
    EMPLOYER_KEY = 'zenjob'


class CrossbeamScraper(GreenhouseScraper):
    employer_name = 'Crossbeam'
    EMPLOYER_KEY = 'crossbeam'


class PathaiScraper(GreenhouseApiScraper):
    employer_name = 'PathAI'
    EMPLOYER_KEY = 'pathai'


class ZerocaterScraper(GreenhouseApiScraper):
    employer_name = 'Zerocater'
    EMPLOYER_KEY = 'zerocater'


class LeanTechnologiesScraper(LeverScraper):
    employer_name = 'Lean Technologies'
    EMPLOYER_KEY = 'LeanTech'


class AiRudderScraper(GreenhouseApiScraper):
    employer_name = 'AI Rudder'
    EMPLOYER_KEY = 'airudder'


class AlloyScraper(GreenhouseApiScraper):
    employer_name = 'Alloy'
    EMPLOYER_KEY = 'alloy'


class ContentfulScraper(GreenhouseScraper):
    employer_name = 'Contentful'
    EMPLOYER_KEY = 'contentful'


class SplitScraper(GreenhouseScraper):
    employer_name = 'Split'
    EMPLOYER_KEY = 'split'


class DigitalAssetScraper(GreenhouseScraper):
    employer_name = 'Digital Asset'
    EMPLOYER_KEY = 'digitalasset'


class BigidScraper(GreenhouseScraper):
    employer_name = 'BigID'
    EMPLOYER_KEY = 'bigid'


class LumaHealthScraper(GreenhouseScraper):
    employer_name = 'Luma Health'
    EMPLOYER_KEY = 'lumahealth'


class PaytientScraper(LeverScraper):
    employer_name = 'Paytient'
    EMPLOYER_KEY = 'paytient'


class GithubScraper(GreenhouseScraper):
    employer_name = 'GitHub'
    EMPLOYER_KEY = 'github'


class CmrSurgicalScraper(GreenhouseApiScraper):
    employer_name = 'CMR Surgical'
    EMPLOYER_KEY = 'cmrsurgical'


class WaterplanScraper(AshbyHQScraper):
    employer_name = 'Waterplan'
    EMPLOYER_KEY = 'Waterplan'


class MetalabScraper(GreenhouseScraper):
    employer_name = 'MetaLab'
    EMPLOYER_KEY = 'metalab'


class YellowAiScraper(LeverScraper):
    employer_name = 'Yellow.ai'
    EMPLOYER_KEY = 'yellowai'


class BrightflowAiScraper(GreenhouseScraper):
    employer_name = 'Brightflow AI'
    EMPLOYER_KEY = 'brightflowai'


class JuniScraper(AshbyHQScraper):
    employer_name = 'Juni'
    EMPLOYER_KEY = 'juni'


class AwayScraper(AshbyHQScraper):
    employer_name = 'Away'
    EMPLOYER_KEY = 'away'


class SanityScraper(GreenhouseScraper):
    employer_name = 'Sanity'
    EMPLOYER_KEY = 'sanityio'


class TrmScraper(GreenhouseApiScraper):
    employer_name = 'TRM'
    EMPLOYER_KEY = 'trm'


class KnowdeScraper(GreenhouseScraper):
    employer_name = 'Knowde'
    EMPLOYER_KEY = 'knowde'


class WarbyParkerScraper(GreenhouseScraper):
    employer_name = 'Warby Parker'
    EMPLOYER_KEY = 'warbyparker'


class VestaScraper(GreenhouseApiScraper):
    employer_name = 'Vesta Healthcare'
    EMPLOYER_KEY = 'vestahealthcare'


class ReibusScraper(LeverScraper):
    employer_name = 'Reibus'
    EMPLOYER_KEY = 'reibus'


class AmperityScraper(GreenhouseScraper):
    employer_name = 'Amperity'
    EMPLOYER_KEY = 'amperity'


class SpaceAndTimeScraper(RipplingAtsScraper):
    employer_name = 'Space and Time'
    EMPLOYER_KEY = 'sxt'


class DailypayScraper(GreenhouseApiScraper):
    employer_name = 'DailyPay'
    EMPLOYER_KEY = 'dailypay'


class AngleHealthScraper(LeverScraper):
    employer_name = 'Angle Health'
    EMPLOYER_KEY = 'AngleHealth'


class WunderkindScraper(GreenhouseApiScraper):
    employer_name = 'Wunderkind'
    EMPLOYER_KEY = 'wunderkind'


class RattleScraper(AshbyHQScraper):
    employer_name = 'Rattle'
    EMPLOYER_KEY = 'Rattle'


class CloudkitchensScraper(GreenhouseScraper):
    employer_name = 'CloudKitchens'
    EMPLOYER_KEY = 'css'


class ModernTreasuryScraper(AshbyHQScraper):
    employer_name = 'Modern Treasury'
    EMPLOYER_KEY = 'moderntreasury'


class InfluxdataScraper(GreenhouseApiScraper):
    employer_name = 'InfluxData'
    EMPLOYER_KEY = 'influxdb'


class HighspotScraper(LeverScraper):
    employer_name = 'Highspot'
    EMPLOYER_KEY = 'highspot'


class JungleScoutScraper(GreenhouseScraper):
    employer_name = 'Jungle Scout'
    EMPLOYER_KEY = 'junglescout'


class MercuryScraper(GreenhouseScraper):
    employer_name = 'Mercury'
    EMPLOYER_KEY = 'mercury'


class BitfuryScraper(GreenhouseScraper):
    employer_name = 'Bitfury'
    EMPLOYER_KEY = 'bitfury'


class PaxScraper(GreenhouseScraper):
    employer_name = 'Pax'
    EMPLOYER_KEY = 'paxlabs'


class CatalantScraper(LeverScraper):
    employer_name = 'Catalant'
    EMPLOYER_KEY = 'gocatalant'


class ElementlScraper(GreenhouseScraper):
    employer_name = 'Elementl'
    EMPLOYER_KEY = 'elementl'


class InvocaScraper(GreenhouseApiScraper):
    employer_name = 'Invoca'
    EMPLOYER_KEY = 'invoca'


class PermutiveScraper(GreenhouseScraper):
    employer_name = 'Permutive'
    EMPLOYER_KEY = 'permutive'


class SlopeScraper(AshbyHQScraper):
    employer_name = 'Slope'
    EMPLOYER_KEY = 'slope'


class CarbonDirectScraper(LeverScraper):
    employer_name = 'Carbon Direct'
    EMPLOYER_KEY = 'CarbonDirect'


class FinleyScraper(LeverScraper):
    employer_name = 'Finley'
    EMPLOYER_KEY = 'FinleyTechnologies'


class VtsScraper(GreenhouseScraper):
    employer_name = 'VTS'
    EMPLOYER_KEY = 'vts'


class MorseMicroScraper(GreenhouseApiScraper):
    employer_name = 'Morse Micro'
    EMPLOYER_KEY = 'morsemicro'


class MicronScraper(WorkdayScraper):
    employer_name = 'Micron'
    start_url = 'https://micron.wd1.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class PrintfulScraper(WorkdayScraper):
    employer_name = 'Printful'
    start_url = 'https://printful.wd1.myworkdayjobs.com/en-US/Printful/'
    has_job_departments = False


class AmwellScraper(GreenhouseScraper):
    employer_name = 'Amwell'
    EMPLOYER_KEY = 'amwell'


class BoomiScraper(GreenhouseApiScraper):
    employer_name = 'Boomi'
    EMPLOYER_KEY = 'boomilp'


class CarbonRoboticsScraper(GreenhouseApiScraper):
    employer_name = 'Carbon Robotics'
    EMPLOYER_KEY = 'carbonrobotics'


class DoximityScraper(GreenhouseApiScraper):
    employer_name = 'Doximity'
    EMPLOYER_KEY = 'doximity'


class NtwrkScraper(LeverScraper):
    employer_name = 'NTWRK'
    EMPLOYER_KEY = 'thentwrk'


class AdvancedNavScraper(LeverScraper):
    employer_name = 'Advanced Nav'
    EMPLOYER_KEY = 'advancednavigation'


class InstructureScraper(LeverScraper):
    employer_name = 'Instructure'
    EMPLOYER_KEY = 'instructure'


class AppenScraper(LeverScraper):
    employer_name = 'Appen'
    EMPLOYER_KEY = 'appen-2'


class VeritasScraper(WorkdayScraper):
    employer_name = 'Veritas'
    start_url = 'https://veritas.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class CloudbedsScraper(GreenhouseScraper):
    employer_name = 'Cloudbeds'
    EMPLOYER_KEY = 'cloudbeds'


class IterableScraper(GreenhouseApiScraper):
    employer_name = 'Iterable'
    EMPLOYER_KEY = 'iterable'


class VicAiScraper(GreenhouseApiScraper):
    employer_name = 'Vic.ai'
    EMPLOYER_KEY = 'vicai'


class VartanaScraper(LeverScraper):
    employer_name = 'Vartana'
    EMPLOYER_KEY = 'Vartana'


class ZendeskScraper(WorkdayScraper):
    employer_name = 'Zendesk'
    start_url = 'https://zendesk.wd1.myworkdayjobs.com/en-US/zendesk/'
    has_job_departments = False


class SumoLogicScraper(GreenhouseScraper):
    employer_name = 'Sumo Logic'
    EMPLOYER_KEY = 'sumologic'


class HotelEngineScraper(GreenhouseScraper):
    employer_name = 'Hotel Engine'
    EMPLOYER_KEY = 'hotelengine'


class HiveScraper(LeverScraper):
    employer_name = 'Hive'
    EMPLOYER_KEY = 'hive'


class KaseyaScraper(SmartRecruitersScraper):
    employer_name = 'Kaseya'
    EMPLOYER_KEY = 'Kaseya'


class TropicScraper(GreenhouseScraper):
    employer_name = 'Tropic'
    EMPLOYER_KEY = 'tropic'


class VialScraper(LeverScraper):
    employer_name = 'Vial'
    EMPLOYER_KEY = 'Vial'


class AlmaScraper(GreenhouseScraper):
    employer_name = 'Alma'
    EMPLOYER_KEY = 'alma'


class MaterialBankScraper(GreenhouseScraper):
    employer_name = 'Material Bank'
    EMPLOYER_KEY = 'materialbank'


class EverlaneScraper(GreenhouseScraper):
    employer_name = 'Everlane'
    EMPLOYER_KEY = 'everlane'


class PagerScraper(GreenhouseApiScraper):
    employer_name = 'Pager'
    EMPLOYER_KEY = 'pager'
