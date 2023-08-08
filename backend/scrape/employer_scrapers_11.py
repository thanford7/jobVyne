from scrape.base_scrapers import AshbyHQScraper, BambooHrScraper, GreenhouseApiScraper, GreenhouseIframeScraper, \
    GreenhouseScraper, LeverScraper, \
    SmartRecruitersScraper, WorkdayScraper


class FlipdishScraper(GreenhouseScraper):
    employer_name = 'Flipdish'
    EMPLOYER_KEY = 'flipdish'


class CoinshiftScraper(LeverScraper):
    employer_name = 'Coinshift'
    EMPLOYER_KEY = 'Coinshift'


class CapchaseScraper(LeverScraper):
    employer_name = 'Capchase'
    EMPLOYER_KEY = 'capchase'


class AgreenaScraper(LeverScraper):
    employer_name = 'Agreena'
    EMPLOYER_KEY = 'agreena'


class EsperScraper(LeverScraper):
    employer_name = 'Esper'
    EMPLOYER_KEY = 'esper-3'


class SingleopsScraper(GreenhouseScraper):
    employer_name = 'SingleOps'
    EMPLOYER_KEY = 'singleops'


class ObserveAiScraper(LeverScraper):
    employer_name = 'Observe.AI'
    EMPLOYER_KEY = 'observeai'


class BitriseScraper(BambooHrScraper):
    employer_name = 'Bitrise'
    EMPLOYER_KEY = 'bitrise'


class PrimarybidScraper(GreenhouseApiScraper):
    employer_name = 'PrimaryBid'
    EMPLOYER_KEY = 'primarybid'


class SwiftNavigationScraper(GreenhouseApiScraper):
    employer_name = 'Swift Navigation'
    EMPLOYER_KEY = 'swiftnavigation'


class AeraTechnologyScraper(LeverScraper):
    employer_name = 'Aera Technology'
    EMPLOYER_KEY = 'aeratechnology'


class HgInsightsScraper(GreenhouseApiScraper):
    employer_name = 'HG Insights'
    EMPLOYER_KEY = 'hginsights'


class UnqorkScraper(GreenhouseScraper):
    employer_name = 'Unqork'
    EMPLOYER_KEY = 'unqork'


class IncidentIoScraper(GreenhouseScraper):
    employer_name = 'incident.io'
    EMPLOYER_KEY = 'incidentio'


class MonteCarloScraper(AshbyHQScraper):
    employer_name = 'Monte Carlo'
    EMPLOYER_KEY = 'montecarlodata'


class TrayIoScraper(GreenhouseScraper):
    employer_name = 'Tray.io'
    EMPLOYER_KEY = 'trayio'


class ClarifyHealthScraper(LeverScraper):
    employer_name = 'Clarify Health'
    EMPLOYER_KEY = 'clarifyhealth'


class MiloScraper(LeverScraper):
    employer_name = 'Milo'
    EMPLOYER_KEY = 'milocredit'


class BoostupAiScraper(GreenhouseScraper):
    employer_name = 'BoostUp.ai'
    EMPLOYER_KEY = 'boostup'


class PrismaScraper(GreenhouseScraper):
    employer_name = 'Prisma'
    EMPLOYER_KEY = 'prisma'


class HeapScraper(GreenhouseScraper):
    employer_name = 'Heap'
    EMPLOYER_KEY = 'heap'


class MazeScraper(AshbyHQScraper):
    employer_name = 'Maze'
    EMPLOYER_KEY = 'mazedesign'


class UberallScraper(LeverScraper):
    employer_name = 'Uberall'
    EMPLOYER_KEY = 'uberall'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class StandardMetricsScraper(GreenhouseScraper):
    employer_name = 'Standard Metrics'
    EMPLOYER_KEY = 'standardmetrics'


class SecureframeScraper(LeverScraper):
    employer_name = 'Secureframe'
    EMPLOYER_KEY = 'secureframe'


class VidmobScraper(GreenhouseApiScraper):
    employer_name = 'VidMob'
    EMPLOYER_KEY = 'vidmob'


class SonarScraper(LeverScraper):
    employer_name = 'Sonar'
    EMPLOYER_KEY = 'sonarsource'


class CoiledScraper(LeverScraper):
    employer_name = 'Coiled'
    EMPLOYER_KEY = 'coiled'


class UptycsScraper(LeverScraper):
    employer_name = 'Uptycs'
    EMPLOYER_KEY = 'uptycs'


class SupraoraclesScraper(GreenhouseScraper):
    employer_name = 'SupraOracles'
    EMPLOYER_KEY = 'supraoracles'


class ZyloScraper(GreenhouseApiScraper):
    employer_name = 'Zylo'
    EMPLOYER_KEY = 'zylo87'


class TerraScraper(LeverScraper):
    employer_name = 'Terra'
    EMPLOYER_KEY = 'terra'


class MagicEdenScraper(GreenhouseScraper):
    employer_name = 'Magic Eden'
    EMPLOYER_KEY = 'magiceden'


class MixpanelScraper(GreenhouseApiScraper):
    employer_name = 'Mixpanel'
    EMPLOYER_KEY = 'mixpanel'


class PatchScraper(LeverScraper):
    employer_name = 'Patch'
    EMPLOYER_KEY = 'patch'


class AcquiaScraper(GreenhouseScraper):
    employer_name = 'Acquia'
    EMPLOYER_KEY = 'acquia'


class RoseRocketScraper(AshbyHQScraper):
    employer_name = 'Rose Rocket'
    EMPLOYER_KEY = 'rose%20rocket'


class SparkcognitionScraper(GreenhouseApiScraper):
    employer_name = 'SparkCognition'
    EMPLOYER_KEY = 'sparkcognition'


class AssemblyaiScraper(GreenhouseScraper):
    employer_name = 'AssemblyAI'
    EMPLOYER_KEY = 'assemblyai'


class UsergemsScraper(GreenhouseApiScraper):
    employer_name = 'UserGems'
    EMPLOYER_KEY = 'usergems'


class OpeninvestScraper(LeverScraper):
    employer_name = 'OpenInvest'
    EMPLOYER_KEY = 'openinvest'


class KaratScraper(GreenhouseApiScraper):
    employer_name = 'Karat'
    EMPLOYER_KEY = 'karat'


class GalaGamesScraper(GreenhouseScraper):
    employer_name = 'Gala Games'
    EMPLOYER_KEY = 'galagames'


class StitchFixScraper(GreenhouseApiScraper):
    employer_name = 'Stitch Fix'
    EMPLOYER_KEY = 'stitchfix'


class OrdergrooveScraper(GreenhouseApiScraper):
    employer_name = 'Ordergroove'
    EMPLOYER_KEY = 'ordergroove'


class CrunchbaseScraper(GreenhouseScraper):
    employer_name = 'Crunchbase'
    EMPLOYER_KEY = 'crunchbase'


class GirlsWhoCodeScraper(LeverScraper):
    employer_name = 'Girls Who Code'
    EMPLOYER_KEY = 'girlswhocode'


class YotpoScraper(GreenhouseApiScraper):
    employer_name = 'Yotpo'
    EMPLOYER_KEY = 'yotpo'


class LeanTaasScraper(LeverScraper):
    employer_name = 'LeanTaas'
    EMPLOYER_KEY = 'leantaas'


class SquireScraper(GreenhouseScraper):
    employer_name = 'Squire'
    EMPLOYER_KEY = 'squire'


class CityblockHealthScraper(GreenhouseApiScraper):
    employer_name = 'Cityblock Health'
    EMPLOYER_KEY = 'cityblockhealth'


class CookunityScraper(GreenhouseScraper):
    employer_name = 'CookUnity'
    EMPLOYER_KEY = 'cookunity'


class ClearmaticsScraper(GreenhouseScraper):
    employer_name = 'Clearmatics'
    EMPLOYER_KEY = 'clearmatics'


class InstabaseScraper(GreenhouseApiScraper):
    employer_name = 'Instabase'
    EMPLOYER_KEY = 'instabase'


class FolxHealthScraper(GreenhouseScraper):
    employer_name = 'FOLX Health'
    EMPLOYER_KEY = 'folxhealth'


class SalsifyScraper(GreenhouseScraper):
    employer_name = 'Salsify'
    EMPLOYER_KEY = 'salsify'


class HeadspaceScraper(GreenhouseApiScraper):
    employer_name = 'Headspace'
    EMPLOYER_KEY = 'hs'


class NoredinkScraper(GreenhouseApiScraper):
    employer_name = 'NoRedInk'
    EMPLOYER_KEY = 'noredink'


class StackblitzScraper(LeverScraper):
    employer_name = 'StackBlitz'
    EMPLOYER_KEY = 'stackblitz'


class PeppyScraper(LeverScraper):
    employer_name = 'Peppy'
    EMPLOYER_KEY = 'peppy'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class FilecoinFoundationScraper(GreenhouseScraper):
    employer_name = 'Filecoin Foundation'
    EMPLOYER_KEY = 'filecoinfoundation'


class DotmaticsScraper(GreenhouseApiScraper):
    employer_name = 'Dotmatics'
    EMPLOYER_KEY = 'dotmatics'


class NetlifyScraper(GreenhouseScraper):
    employer_name = 'Netlify'
    EMPLOYER_KEY = 'netlify'


class TheInformationScraper(GreenhouseScraper):
    employer_name = 'The Information'
    EMPLOYER_KEY = 'theinformation'


class BandaiNamcoScraper(GreenhouseApiScraper):
    employer_name = 'Bandai Namco'
    EMPLOYER_KEY = 'bandainamco'


class HeirScraper(GreenhouseScraper):
    employer_name = 'HEIR'
    EMPLOYER_KEY = 'heir'


class TurntideScraper(GreenhouseApiScraper):
    employer_name = 'Turntide'
    EMPLOYER_KEY = 'turntide'


class SeekoutScraper(GreenhouseApiScraper):
    employer_name = 'SeekOut'
    EMPLOYER_KEY = 'seekout'


class ThriveGlobalScraper(GreenhouseScraper):
    employer_name = 'Thrive Global'
    EMPLOYER_KEY = 'thriveglobal'


class UniteUsScraper(GreenhouseScraper):
    employer_name = 'Unite Us'
    EMPLOYER_KEY = 'uniteus'


class HypebeastScraper(LeverScraper):
    employer_name = 'HYPEBEAST'
    EMPLOYER_KEY = 'hypebeast'


class GraphiteSoftwareScraper(AshbyHQScraper):
    employer_name = 'Graphite Software'
    EMPLOYER_KEY = 'Graphite'


class SettleScraper(GreenhouseScraper):
    employer_name = 'Settle'
    EMPLOYER_KEY = 'settle'


class GlowforgeScraper(LeverScraper):
    employer_name = 'Glowforge'
    EMPLOYER_KEY = 'glowforge'


class SecurlyScraper(GreenhouseApiScraper):
    employer_name = 'Securly'
    EMPLOYER_KEY = 'securly13'


class UdemyScraper(GreenhouseApiScraper):
    employer_name = 'Udemy'
    EMPLOYER_KEY = 'udemy'


class BigeyeScraper(AshbyHQScraper):
    employer_name = 'Bigeye'
    EMPLOYER_KEY = 'bigeye'


class Mark43Scraper(GreenhouseApiScraper):
    employer_name = 'Mark43'
    EMPLOYER_KEY = 'mark43'


class WriterScraper(AshbyHQScraper):
    employer_name = 'Writer'
    EMPLOYER_KEY = 'writer'


class M1FinanceScraper(GreenhouseScraper):
    employer_name = 'M1 Finance'
    EMPLOYER_KEY = 'm1finance'


class AlluxioScraper(LeverScraper):
    employer_name = 'Alluxio'
    EMPLOYER_KEY = 'alluxio'


class LightricksScraper(GreenhouseApiScraper):
    employer_name = 'Lightricks'
    EMPLOYER_KEY = 'lightricks'


class CreativeFabricaScraper(GreenhouseScraper):
    employer_name = 'Creative Fabrica'
    EMPLOYER_KEY = 'creativefabrica'


class ChiefScraper(GreenhouseScraper):
    employer_name = 'Chief'
    EMPLOYER_KEY = 'chief'


class QuiddScraper(LeverScraper):
    employer_name = 'Quidd'
    EMPLOYER_KEY = 'quidd'


class CensusScraper(AshbyHQScraper):
    employer_name = 'Census'
    EMPLOYER_KEY = 'Census'


class InjectiveProtocolScraper(LeverScraper):
    employer_name = 'Injective Protocol'
    EMPLOYER_KEY = 'injectivelabs'


class ColumnSoftwareScraper(GreenhouseScraper):
    employer_name = 'Column'
    EMPLOYER_KEY = 'columnsoftware'


class SpotheroScraper(GreenhouseApiScraper):
    employer_name = 'SpotHero'
    EMPLOYER_KEY = 'spothero'


class OmniCreatorProductsScraper(AshbyHQScraper):
    employer_name = 'Omni Creator Products'
    EMPLOYER_KEY = 'ocp'


class ViviScraper(GreenhouseApiScraper):
    employer_name = 'Vivi'
    EMPLOYER_KEY = 'vivi'


class Knowbe4Scraper(GreenhouseScraper):
    employer_name = 'KnowBe4'
    EMPLOYER_KEY = 'knowbe4'


class FlowcarbonScraper(GreenhouseScraper):
    employer_name = 'Flowcarbon'
    EMPLOYER_KEY = 'flowcarbon'


class ZoeScraper(LeverScraper):
    employer_name = 'Zoe'
    EMPLOYER_KEY = 'joinzoe'


class AnaplanScraper(GreenhouseScraper):
    employer_name = 'Anaplan'
    EMPLOYER_KEY = 'anaplan'


class SfoxScraper(GreenhouseApiScraper):
    employer_name = 'SFOX'
    EMPLOYER_KEY = 'sfox'


class HivemqScraper(GreenhouseScraper):
    employer_name = 'HiveMQ'
    EMPLOYER_KEY = 'hivemq'


class HometapScraper(LeverScraper):
    employer_name = 'Hometap'
    EMPLOYER_KEY = 'hometap'


class BitlyScraper(GreenhouseScraper):
    employer_name = 'Bitly'
    EMPLOYER_KEY = 'bitly46'


class VowScraper(GreenhouseScraper):
    employer_name = 'Vow'
    EMPLOYER_KEY = 'vowgroup'


class BuiltScraper(GreenhouseScraper):
    employer_name = 'Built'
    EMPLOYER_KEY = 'getbuilt'


class PacasoScraper(GreenhouseScraper):
    employer_name = 'Pacaso'
    EMPLOYER_KEY = 'pacaso'


class CertikScraper(LeverScraper):
    employer_name = 'CertiK'
    EMPLOYER_KEY = 'certik'


class MediumScraper(LeverScraper):
    employer_name = 'Medium'
    EMPLOYER_KEY = 'medium'


class MerlinLabsScraper(LeverScraper):
    employer_name = 'Merlin Labs'
    EMPLOYER_KEY = 'merlinlabs'


class SyncteraScraper(GreenhouseIframeScraper):
    employer_name = 'Synctera'
    EMPLOYER_KEY = 'synctera'


class AirCompanyScraper(GreenhouseScraper):
    employer_name = 'Air Company'
    EMPLOYER_KEY = 'aircompany'


class MagicScraper(GreenhouseScraper):
    employer_name = 'Magic'
    EMPLOYER_KEY = 'magic'


class KyvernaTherapeuticsScraper(LeverScraper):
    employer_name = 'Kyverna Therapeutics'
    EMPLOYER_KEY = 'Kyverna'


class XwingScraper(GreenhouseScraper):
    employer_name = 'Xwing'
    EMPLOYER_KEY = 'xwing'


class GroveCollaborativeScraper(LeverScraper):
    employer_name = 'Grove Collaborative'
    EMPLOYER_KEY = 'grove'


class ZilliqaScraper(GreenhouseScraper):
    employer_name = 'Zilliqa'
    EMPLOYER_KEY = 'zilliqa'


class StonecoScraper(GreenhouseScraper):
    employer_name = 'StoneCo'
    EMPLOYER_KEY = 'stone'


class BrincScraper(LeverScraper):
    employer_name = 'Brinc'
    EMPLOYER_KEY = 'brinc'


class RaribleScraper(LeverScraper):
    employer_name = 'Rarible'
    EMPLOYER_KEY = 'Rarible'


class CdProjektScraper(SmartRecruitersScraper):
    employer_name = 'CD Projekt'
    EMPLOYER_KEY = 'CDPROJEKTRED'


class AlltrailsScraper(LeverScraper):
    employer_name = 'AllTrails'
    EMPLOYER_KEY = 'alltrails'


class RaniTherapeuticsScraper(LeverScraper):
    employer_name = 'Rani Therapeutics'
    EMPLOYER_KEY = 'RaniTherapeutics'


class TruvScraper(LeverScraper):
    employer_name = 'Truv'
    EMPLOYER_KEY = 'truv'


class MailchainScraper(GreenhouseApiScraper):
    employer_name = 'Mailchain'
    EMPLOYER_KEY = 'mailchain'


class GardenScraper(GreenhouseScraper):
    employer_name = 'Garden'
    EMPLOYER_KEY = 'gardenio'


class FuelScraper(LeverScraper):
    employer_name = 'Fuel'
    EMPLOYER_KEY = 'fuellabs'


class SourcegraphScraper(GreenhouseScraper):
    employer_name = 'Sourcegraph'
    EMPLOYER_KEY = 'sourcegraph91'


class RoverScraper(LeverScraper):
    employer_name = 'Rover'
    EMPLOYER_KEY = 'rover'


class UnionAiScraper(AshbyHQScraper):
    employer_name = 'Union AI'
    EMPLOYER_KEY = 'Union'


class SentryScraper(GreenhouseScraper):
    employer_name = 'Sentry'
    EMPLOYER_KEY = 'sentry'


class PragmaPlatformScraper(AshbyHQScraper):
    employer_name = 'Pragma Platform'
    EMPLOYER_KEY = 'pragmaplatform'


class EthereumFoundationScraper(LeverScraper):
    employer_name = 'Ethereum Foundation'
    EMPLOYER_KEY = 'ethereumfoundation'


class InworldScraper(LeverScraper):
    employer_name = 'Inworld'
    EMPLOYER_KEY = 'inworld'


class EigenlabsScraper(GreenhouseScraper):
    employer_name = 'EigenLabs'
    EMPLOYER_KEY = 'eigenlabs'


class RelationalaiScraper(GreenhouseScraper):
    employer_name = 'RelationalAI'
    EMPLOYER_KEY = 'relationalai'


class DfinityScraper(GreenhouseScraper):
    employer_name = 'DFINITY'
    EMPLOYER_KEY = 'dfinity'


class SeiLabsScraper(LeverScraper):
    employer_name = 'Sei Labs'
    EMPLOYER_KEY = 'SeiLabs'


class ShardeumScraper(GreenhouseScraper):
    employer_name = 'Shardeum'
    EMPLOYER_KEY = 'shardeumfoundation'


class ChiaScraper(GreenhouseApiScraper):
    employer_name = 'Chia'
    EMPLOYER_KEY = 'chianetworkinc'


class DittoScraper(AshbyHQScraper):
    employer_name = 'Ditto'
    EMPLOYER_KEY = 'ditto'


class CodeseeScraper(LeverScraper):
    employer_name = 'CodeSee'
    EMPLOYER_KEY = 'codesee'


class StellarfiScraper(LeverScraper):
    employer_name = 'StellarFi'
    EMPLOYER_KEY = 'stellarfinance'


class AgentsyncScraper(GreenhouseScraper):
    employer_name = 'AgentSync'
    EMPLOYER_KEY = 'agentsync'


class MergeScraper(GreenhouseScraper):
    employer_name = 'Merge'
    EMPLOYER_KEY = 'merge'


class ProviScraper(LeverScraper):
    employer_name = 'Provi'
    EMPLOYER_KEY = 'provi'


class HalbornScraper(AshbyHQScraper):
    employer_name = 'Halborn'
    EMPLOYER_KEY = 'halborn'


class C6BankScraper(GreenhouseScraper):
    employer_name = 'C6 Bank'
    EMPLOYER_KEY = 'c6bank'


class AutographScraper(GreenhouseScraper):
    employer_name = 'Autograph'
    EMPLOYER_KEY = 'autograph'


class NeonBankScraper(LeverScraper):
    employer_name = 'Neon Bank'
    EMPLOYER_KEY = 'neon'


class DscoutScraper(LeverScraper):
    employer_name = 'dscout'
    EMPLOYER_KEY = 'dscout'


class IfoodScraper(GreenhouseScraper):
    employer_name = 'iFood'
    EMPLOYER_KEY = 'ifoodcarreiras'


class PerchwellScraper(GreenhouseScraper):
    employer_name = 'Perchwell'
    EMPLOYER_KEY = 'pw'


class MicroFocusScraper(WorkdayScraper):
    employer_name = 'Micro Focus'
    start_url = 'https://microfocus.wd5.myworkdayjobs.com/en-US/Jobsatmicrofocus/'
    has_job_departments = False


class FirstModeScraper(GreenhouseApiScraper):
    employer_name = 'First Mode'
    EMPLOYER_KEY = 'firstmode'


class WasabiScraper(LeverScraper):
    employer_name = 'Wasabi'
    EMPLOYER_KEY = 'wasabi'


class HelloHeartScraper(GreenhouseScraper):
    employer_name = 'Hello Heart'
    EMPLOYER_KEY = 'helloheart'


class CommonRoomScraper(GreenhouseApiScraper):
    employer_name = 'Common Room'
    EMPLOYER_KEY = 'joincommonroom'


class UnicoScraper(LeverScraper):
    employer_name = 'Unico'
    EMPLOYER_KEY = 'unico'


class ZippinScraper(AshbyHQScraper):
    employer_name = 'Zippin'
    EMPLOYER_KEY = 'zippin'


class WingtraScraper(LeverScraper):
    employer_name = 'Wingtra'
    EMPLOYER_KEY = 'wingtra-2'


class FampayScraper(LeverScraper):
    employer_name = 'FamPay'
    EMPLOYER_KEY = 'fampay'


class GoustoScraper(SmartRecruitersScraper):
    employer_name = 'Gousto'
    EMPLOYER_KEY = 'Gousto1'


class RidecellScraper(GreenhouseScraper):
    employer_name = 'Ridecell'
    EMPLOYER_KEY = 'ridecell'


class InsurifyScraper(GreenhouseScraper):
    employer_name = 'Insurify'
    EMPLOYER_KEY = 'insurify'


class EdgeNodeScraper(GreenhouseScraper):
    employer_name = 'Edge & Node'
    EMPLOYER_KEY = 'edgeandnode'


class TharsisLabsScraper(GreenhouseScraper):
    employer_name = 'Tharsis Labs'
    EMPLOYER_KEY = 'evmos'


class OutschoolScraper(GreenhouseScraper):
    employer_name = 'Outschool'
    EMPLOYER_KEY = 'outschool'


class BallertvScraper(LeverScraper):
    employer_name = 'BallerTV'
    EMPLOYER_KEY = 'baller'


class HangScraper(AshbyHQScraper):
    employer_name = 'Hang'
    EMPLOYER_KEY = 'Hang'


class SupersideScraper(LeverScraper):
    employer_name = 'Superside'
    EMPLOYER_KEY = 'superside'


class MultiverseScraper(AshbyHQScraper):
    employer_name = 'Multiverse'
    EMPLOYER_KEY = 'multiverse'


class ReifyHealthScraper(GreenhouseApiScraper):
    employer_name = 'Reify Health'
    EMPLOYER_KEY = 'reifyhealth'


class SuperScraper(GreenhouseScraper):
    employer_name = 'Super'
    EMPLOYER_KEY = 'superpayments'


class TractableScraper(GreenhouseApiScraper):
    employer_name = 'Tractable'
    EMPLOYER_KEY = 'tractable'


class BumbleScraper(WorkdayScraper):
    employer_name = 'Bumble'
    start_url = 'https://bumble.wd3.myworkdayjobs.com/en-US/Bumble_Careers/'
    has_job_departments = False


class GantryScraper(LeverScraper):
    employer_name = 'Gantry'
    EMPLOYER_KEY = 'gantry'


class WayflyerScraper(AshbyHQScraper):
    employer_name = 'Wayflyer'
    EMPLOYER_KEY = 'wayflyer'


class MollieScraper(AshbyHQScraper):
    employer_name = 'Mollie'
    EMPLOYER_KEY = 'mollie'


class DiceScraper(GreenhouseScraper):
    employer_name = 'Dice'
    EMPLOYER_KEY = 'dice'


class LendingtreeScraper(GreenhouseScraper):
    employer_name = 'LendingTree'
    EMPLOYER_KEY = 'lendingtree'


class KitmanLabsScraper(LeverScraper):
    employer_name = 'Kitman Labs'
    EMPLOYER_KEY = 'kitmanlabs'


class HoneybookScraper(GreenhouseApiScraper):
    employer_name = 'HoneyBook'
    EMPLOYER_KEY = 'honeybook'


class AxeleraAiScraper(LeverScraper):
    employer_name = 'Axelera AI'
    EMPLOYER_KEY = 'axelera'


class PelaScraper(GreenhouseApiScraper):
    employer_name = 'Pela'
    EMPLOYER_KEY = 'pelacase'


class Ten47GamesScraper(GreenhouseScraper):
    employer_name = '1047 Games'
    EMPLOYER_KEY = '1047games'


class MmhmmScraper(GreenhouseScraper):
    employer_name = 'mmhmm'
    EMPLOYER_KEY = 'allturtles'


class BelieverScraper(AshbyHQScraper):
    employer_name = 'Believer'
    EMPLOYER_KEY = 'believer'


class DevrevScraper(GreenhouseScraper):
    employer_name = 'DevRev'
    EMPLOYER_KEY = 'devrev'


class SpykeScraper(LeverScraper):
    employer_name = 'Spyke'
    EMPLOYER_KEY = 'spyke-games'


class BlockworksScraper(AshbyHQScraper):
    employer_name = 'Blockworks'
    EMPLOYER_KEY = 'Blockworks'


class SandboxVrScraper(LeverScraper):
    employer_name = 'Sandbox VR'
    EMPLOYER_KEY = 'sandboxvr'


class BonfireStudiosScraper(LeverScraper):
    employer_name = 'Bonfire Studios'
    EMPLOYER_KEY = 'bonfirestudios'


class ReadyPlayerMeScraper(GreenhouseScraper):
    employer_name = 'Ready Player Me'
    EMPLOYER_KEY = 'readyplayerme'


class OdysseyInteractiveScraper(SmartRecruitersScraper):
    employer_name = 'Odyssey Interactive'
    EMPLOYER_KEY = 'OdysseyInteractive'


class KueskiScraper(LeverScraper):
    employer_name = 'Kueski'
    EMPLOYER_KEY = 'kueski'


class AirtmScraper(LeverScraper):
    employer_name = 'Airtm'
    EMPLOYER_KEY = 'airtm'


class StepScraper(GreenhouseApiScraper):
    employer_name = 'Step'
    EMPLOYER_KEY = 'stepmobile'


class CopyAiScraper(LeverScraper):
    employer_name = 'Copy.ai'
    EMPLOYER_KEY = 'CopyAI'


class MindbodyScraper(GreenhouseApiScraper):
    employer_name = 'Mindbody'
    EMPLOYER_KEY = 'mindbody'


class QualifiedScraper(LeverScraper):
    employer_name = 'Qualified'
    EMPLOYER_KEY = 'qualified'


class CoindeskScraper(GreenhouseScraper):
    employer_name = 'CoinDesk'
    EMPLOYER_KEY = 'coindesk'


class VeriffScraper(GreenhouseApiScraper):
    employer_name = 'Veriff'
    EMPLOYER_KEY = 'veriff'


class SequenceScraper(AshbyHQScraper):
    employer_name = 'Sequence'
    EMPLOYER_KEY = 'sequence'


class SigmaComputingScraper(GreenhouseScraper):
    employer_name = 'Sigma Computing'
    EMPLOYER_KEY = 'sigmacomputing'


class ZoraScraper(GreenhouseScraper):
    employer_name = 'Zora'
    EMPLOYER_KEY = 'zora'


class ParafinScraper(AshbyHQScraper):
    employer_name = 'Parafin'
    EMPLOYER_KEY = 'parafin'


class TextileScraper(GreenhouseScraper):
    employer_name = 'Textile'
    EMPLOYER_KEY = 'textileio'


class PennylaneScraper(LeverScraper):
    employer_name = 'Pennylane'
    EMPLOYER_KEY = 'pennylane'


class WindfallScraper(LeverScraper):
    employer_name = 'Windfall'
    EMPLOYER_KEY = 'windfalldata'


class JoyScraper(GreenhouseApiScraper):
    employer_name = 'Joy'
    EMPLOYER_KEY = 'joy'


class KohoScraper(LeverScraper):
    employer_name = 'Koho'
    EMPLOYER_KEY = 'koho'


class MossScraper(GreenhouseScraper):
    employer_name = 'Moss'
    EMPLOYER_KEY = 'moss'


class QBioScraper(LeverScraper):
    employer_name = 'Q Bio'
    EMPLOYER_KEY = 'qbio'


class FintualScraper(LeverScraper):
    employer_name = 'Fintual'
    EMPLOYER_KEY = 'fintual'


class SweepScraper(GreenhouseScraper):
    employer_name = 'Sweep'
    EMPLOYER_KEY = 'sweep'


class NextMatterScraper(AshbyHQScraper):
    employer_name = 'Next Matter'
    EMPLOYER_KEY = 'nextmatter'


class CalmScraper(GreenhouseScraper):
    employer_name = 'Calm'
    EMPLOYER_KEY = 'calm'


class TomeScraper(AshbyHQScraper):
    employer_name = 'Tome'
    EMPLOYER_KEY = 'Tome'


class EkoScraper(LeverScraper):
    employer_name = 'Eko'
    EMPLOYER_KEY = 'ekohealth'


class QuantumMetricScraper(LeverScraper):
    employer_name = 'Quantum Metric'
    EMPLOYER_KEY = 'quantummetric'


class TruecarScraper(GreenhouseApiScraper):
    employer_name = 'TrueCar'
    EMPLOYER_KEY = 'truecar'


class FlockFreightScraper(GreenhouseApiScraper):
    employer_name = 'Flock Freight'
    EMPLOYER_KEY = 'flockfreight'


class CloudtrucksScraper(AshbyHQScraper):
    employer_name = 'CloudTrucks'
    EMPLOYER_KEY = 'cloudtrucks'


class CultureAmpScraper(GreenhouseScraper):
    employer_name = 'Culture Amp'
    EMPLOYER_KEY = 'cultureamp'


class TextnowScraper(LeverScraper):
    employer_name = 'TextNow'
    EMPLOYER_KEY = 'textnow'


class BalbixScraper(LeverScraper):
    employer_name = 'Balbix'
    EMPLOYER_KEY = 'balbix'


class ThirtyMadisonScraper(GreenhouseScraper):
    employer_name = 'Thirty Madison'
    EMPLOYER_KEY = 'thirtymadison'


class BuildkiteScraper(LeverScraper):
    employer_name = 'Buildkite'
    EMPLOYER_KEY = 'Buildkite'


class ApprenticeScraper(GreenhouseScraper):
    employer_name = 'Apprentice'
    EMPLOYER_KEY = 'apprentice'
