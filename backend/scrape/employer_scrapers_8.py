from scrape.base_scrapers import AshbyHQScraper, \
    GreenhouseApiScraper, \
    GreenhouseScraper, LeverScraper, SmartRecruitersScraper, \
    WorkdayScraper


class SolanaLabsScraper(GreenhouseScraper):
    employer_name = 'Solana Labs'
    EMPLOYER_KEY = 'solana'


class CooleyScraper(WorkdayScraper):
    employer_name = 'Cooley'
    start_url = 'https://cooley.wd1.myworkdayjobs.com/en-US/Cooley_US_LLP/'
    has_job_departments = False


class OverairScraper(GreenhouseApiScraper):
    employer_name = 'Overair'
    EMPLOYER_KEY = 'overair'


class GrammarlyScraper(GreenhouseScraper):
    employer_name = 'Grammarly'
    EMPLOYER_KEY = 'grammarly'


class StartreeScraper(GreenhouseScraper):
    employer_name = 'StarTree'
    EMPLOYER_KEY = 'startree'


class PonteraScraper(GreenhouseScraper):
    employer_name = 'Pontera'
    EMPLOYER_KEY = 'pontera'


class NautilusScraper(GreenhouseApiScraper):
    employer_name = 'Nautilus'
    EMPLOYER_KEY = 'nautiluslabs'


class BlockdaemonScraper(GreenhouseScraper):
    employer_name = 'Blockdaemon'
    EMPLOYER_KEY = 'blockdaemon'


class LalamoveScraper(LeverScraper):
    employer_name = 'Lalamove'
    EMPLOYER_KEY = 'lalamove'


class HaydenAiScraper(GreenhouseScraper):
    employer_name = 'Hayden AI'
    EMPLOYER_KEY = 'haydenai'


class PathRoboticsScraper(GreenhouseApiScraper):
    employer_name = 'Path Robotics'
    EMPLOYER_KEY = 'pathrobotics'


class ThoughtspotScraper(GreenhouseApiScraper):
    employer_name = 'ThoughtSpot'
    EMPLOYER_KEY = 'thoughtspot'


class QredoScraper(LeverScraper):
    employer_name = 'Qredo'
    EMPLOYER_KEY = 'qredo'


class PrestoScraper(LeverScraper):
    employer_name = 'Presto'
    EMPLOYER_KEY = 'Presto'


class InvitaeScraper(GreenhouseApiScraper):
    employer_name = 'Invitae'
    EMPLOYER_KEY = 'invitae'


class LoftOrbitalScraper(LeverScraper):
    employer_name = 'Loft Orbital'
    EMPLOYER_KEY = 'loftorbital'


class VoltaScraper(GreenhouseScraper):
    employer_name = 'Volta'
    EMPLOYER_KEY = 'voltacharging'


class SpanScraper(GreenhouseScraper):
    employer_name = 'Span'
    EMPLOYER_KEY = 'spanio'


class VardaScraper(GreenhouseScraper):
    employer_name = 'Varda'
    EMPLOYER_KEY = 'vardaspace'


class PagosScraper(AshbyHQScraper):
    employer_name = 'Pagos'
    EMPLOYER_KEY = 'pagos'


class TalaScraper(LeverScraper):
    employer_name = 'Tala'
    EMPLOYER_KEY = 'tala'


class RedpandaScraper(GreenhouseScraper):
    employer_name = 'Redpanda'
    EMPLOYER_KEY = 'redpandadata'


class HypergiantScraper(GreenhouseApiScraper):
    employer_name = 'Hypergiant'
    EMPLOYER_KEY = 'hypergiant'


class DapperLabsScraper(LeverScraper):
    employer_name = 'Dapper Labs'
    EMPLOYER_KEY = 'axiomzen'


class BitcoinDepotScraper(GreenhouseScraper):
    employer_name = 'Bitcoin Depot'
    EMPLOYER_KEY = 'bitcoindepot'


class HashicorpScraper(GreenhouseApiScraper):
    employer_name = 'HashiCorp'
    EMPLOYER_KEY = 'hashicorp'


class KhaznaScraper(SmartRecruitersScraper):
    employer_name = 'Khazna'
    EMPLOYER_KEY = 'KhaznaTech'


class SvtRoboticsScraper(GreenhouseScraper):
    employer_name = 'SVT Robotics'
    EMPLOYER_KEY = 'svtrobotics'


class JuulScraper(GreenhouseScraper):
    employer_name = 'JUUL'
    EMPLOYER_KEY = 'juullabs'


class HelionEnergyScraper(GreenhouseScraper):
    employer_name = 'Helion Energy'
    EMPLOYER_KEY = 'helionenergy'


class OrderlyNetworkScraper(GreenhouseScraper):
    employer_name = 'Orderly Network'
    EMPLOYER_KEY = 'orderlynetwork'


class GoproScraper(GreenhouseApiScraper):
    employer_name = 'GoPro'
    EMPLOYER_KEY = 'goprocareers'


class MediaoceanScraper(LeverScraper):
    employer_name = 'Mediaocean'
    EMPLOYER_KEY = 'mediaocean'


class SpycloudScraper(GreenhouseScraper):
    employer_name = 'SpyCloud'
    EMPLOYER_KEY = 'spycloud'


class SierraSpaceScraper(WorkdayScraper):
    employer_name = 'Sierra Space'
    start_url = 'https://snc.wd1.myworkdayjobs.com/en-US/Sierra_Space_External_Career_Site/'
    has_job_departments = False


class YugabyteScraper(GreenhouseScraper):
    employer_name = 'Yugabyte'
    EMPLOYER_KEY = 'yugabyte'


class CarisLifeSciencesScraper(WorkdayScraper):
    employer_name = 'Caris Life Sciences'
    start_url = 'https://carislifesciences.wd1.myworkdayjobs.com/en-US/cls/'
    has_job_departments = False


class SkyryseScraper(GreenhouseScraper):
    employer_name = 'Skyryse'
    EMPLOYER_KEY = 'skyryse'


class ReplicantScraper(LeverScraper):
    employer_name = 'Replicant'
    EMPLOYER_KEY = 'replicant'


class DigitalAIScraper(GreenhouseApiScraper):
    employer_name = 'Digital.ai'
    EMPLOYER_KEY = 'digitalai'


class BritiveScraper(GreenhouseScraper):
    employer_name = 'Britive'
    EMPLOYER_KEY = 'britive'


class AuroraScraper(GreenhouseScraper):
    employer_name = 'Aurora'
    EMPLOYER_KEY = 'aurorainnovation'


class SlicePayScraper(SmartRecruitersScraper):
    employer_name = 'Slice Pay'
    EMPLOYER_KEY = 'slice1'


class AllbirdsScraper(GreenhouseApiScraper):
    employer_name = 'Allbirds'
    EMPLOYER_KEY = 'allbirds'


class SednaScraper(AshbyHQScraper):
    employer_name = 'Sedna'
    EMPLOYER_KEY = 'sedna'


class LuminarScraper(GreenhouseScraper):
    employer_name = 'Luminar'
    EMPLOYER_KEY = 'luminar'


class ReliableRoboticsScraper(LeverScraper):
    employer_name = 'Reliable Robotics'
    EMPLOYER_KEY = 'reliable'


class NzxtScraper(GreenhouseScraper):
    employer_name = 'NZXT'
    EMPLOYER_KEY = 'nzxt'


class FleetcorScraper(WorkdayScraper):
    employer_name = 'Fleetcor'
    start_url = 'https://fleetcor.wd3.myworkdayjobs.com/en-US/Ext_001/'
    has_job_departments = False


class BigcommerceScraper(GreenhouseApiScraper):
    employer_name = 'BigCommerce'
    EMPLOYER_KEY = 'bigcommerce'


class LinksquaresScraper(GreenhouseApiScraper):
    employer_name = 'LinkSquares'
    EMPLOYER_KEY = 'linksquaresinc'


class KairosPowerScraper(GreenhouseApiScraper):
    employer_name = 'Kairos Power'
    EMPLOYER_KEY = 'kairospower'


class TeamviewerScraper(SmartRecruitersScraper):
    employer_name = 'TeamViewer'
    EMPLOYER_KEY = 'TeamViewer1'


class EmbrokerScraper(GreenhouseScraper):
    employer_name = 'Embroker'
    EMPLOYER_KEY = 'embroker'


class Life360Scraper(GreenhouseScraper):
    employer_name = 'Life360'
    EMPLOYER_KEY = 'life360'


class StonlyScraper(GreenhouseApiScraper):
    employer_name = 'Stonly'
    EMPLOYER_KEY = 'stonly'


class LogikcullScraper(GreenhouseScraper):
    employer_name = 'Logikcull'
    EMPLOYER_KEY = 'logikcull'


class AviMedicalScraper(GreenhouseApiScraper):
    employer_name = 'Avi Medical'
    EMPLOYER_KEY = 'avimedical'


class FirstResonanceScraper(GreenhouseScraper):
    employer_name = 'First Resonance'
    EMPLOYER_KEY = 'firstresonance'


class AdvanceAiScraper(GreenhouseScraper):
    employer_name = 'ADVANCE.AI'
    EMPLOYER_KEY = 'advanceai'


class WikimediaScraper(GreenhouseScraper):
    employer_name = 'Wikimedia'
    EMPLOYER_KEY = 'wikimedia'


class ExodusScraper(GreenhouseScraper):
    employer_name = 'Exodus'
    EMPLOYER_KEY = 'exodus54'


class KyruusScraper(LeverScraper):
    employer_name = 'Kyruus'
    EMPLOYER_KEY = 'kyruus'


class HimsScraper(GreenhouseScraper):
    employer_name = 'Hims'
    EMPLOYER_KEY = 'himshers'


class RibbonHealthScraper(GreenhouseApiScraper):
    employer_name = 'Ribbon Health'
    EMPLOYER_KEY = 'ribbonhealth'


class VantageScraper(AshbyHQScraper):
    employer_name = 'Vantage'
    EMPLOYER_KEY = 'vantage'


class ExpelScraper(GreenhouseApiScraper):
    employer_name = 'Expel'
    EMPLOYER_KEY = 'expel'


class LocusRoboticsScraper(SmartRecruitersScraper):
    employer_name = 'Locus Robotics'
    EMPLOYER_KEY = 'LocusRobotics'


class BoosterScraper(GreenhouseApiScraper):
    employer_name = 'Booster'
    EMPLOYER_KEY = 'boostercareers'


class RedVenturesScraper(GreenhouseApiScraper):
    employer_name = 'Red Ventures'
    EMPLOYER_KEY = 'redventures'


class ShipwellScraper(GreenhouseApiScraper):
    employer_name = 'Shipwell'
    EMPLOYER_KEY = 'shipwell'


class ZiprecruiterScraper(GreenhouseScraper):
    employer_name = 'ZipRecruiter'
    EMPLOYER_KEY = 'ziprecruiter'


class CarousellScraper(SmartRecruitersScraper):
    employer_name = 'Carousell'
    EMPLOYER_KEY = 'CarousellGroup'


class EverstreamAnalyticsScraper(GreenhouseScraper):
    employer_name = 'Everstream Analytics'
    EMPLOYER_KEY = 'everstreamanalytics'


class PlanetScraper(GreenhouseScraper):
    employer_name = 'Planet'
    EMPLOYER_KEY = 'planetlabs'


class KariusScraper(LeverScraper):
    employer_name = 'Karius'
    EMPLOYER_KEY = 'kariusdx'


class MoveworksScraper(GreenhouseApiScraper):
    employer_name = 'Moveworks'
    EMPLOYER_KEY = 'moveworks'


class CoverGeniusScraper(LeverScraper):
    employer_name = 'Cover Genius'
    EMPLOYER_KEY = 'covergenius'


class SpotnanaScraper(GreenhouseApiScraper):
    employer_name = 'Spotnana'
    EMPLOYER_KEY = 'spotnanatechnology'


class ClariScraper(LeverScraper):
    employer_name = 'Clari'
    EMPLOYER_KEY = 'clari'


class GraviticsScraper(LeverScraper):
    employer_name = 'Gravitics'
    EMPLOYER_KEY = 'graviticsspace'


class StoryblokScraper(SmartRecruitersScraper):
    employer_name = 'Storyblok'
    EMPLOYER_KEY = 'Storyblok'


class GliaScraper(GreenhouseApiScraper):
    employer_name = 'Glia'
    EMPLOYER_KEY = 'glia'


class ThatgamecompanyScraper(GreenhouseApiScraper):
    employer_name = 'Thatgamecompany'
    EMPLOYER_KEY = 'thatgamecompany'


class GeminiScraper(GreenhouseApiScraper):
    employer_name = 'Gemini'
    EMPLOYER_KEY = 'gemini'


class AfreshScraper(GreenhouseScraper):
    employer_name = 'Afresh'
    EMPLOYER_KEY = 'afresh'


class ExabeamScraper(GreenhouseScraper):
    employer_name = 'Exabeam'
    EMPLOYER_KEY = 'exabeam'


class FaradayFutureScraper(GreenhouseScraper):
    employer_name = 'Faraday Future'
    EMPLOYER_KEY = 'faradayfuture'


class ProtocolLabsScraper(GreenhouseScraper):
    employer_name = 'Protocol Labs'
    EMPLOYER_KEY = 'protocollabs'


class DraftkingsScraper(WorkdayScraper):
    employer_name = 'DraftKings'
    start_url = 'https://draftkings.wd1.myworkdayjobs.com/en-US/DraftKings/'
    has_job_departments = False


class AircallScraper(LeverScraper):
    employer_name = 'Aircall'
    EMPLOYER_KEY = 'aircall'


class AidashScraper(LeverScraper):
    employer_name = 'AiDash'
    EMPLOYER_KEY = 'aidash'


class TypeformScraper(GreenhouseScraper):
    employer_name = 'Typeform'
    EMPLOYER_KEY = 'typeform'


class MagicalScraper(AshbyHQScraper):
    employer_name = 'Magical'
    EMPLOYER_KEY = 'Magical'


class MastercontrolScraper(GreenhouseApiScraper):
    employer_name = 'MasterControl'
    EMPLOYER_KEY = 'mastercontrol'


class OpenstoreScraper(GreenhouseScraper):
    employer_name = 'OpenStore'
    EMPLOYER_KEY = 'openstore'


class SpekitScraper(LeverScraper):
    employer_name = 'Spekit'
    EMPLOYER_KEY = 'spekit'


class FaireScraper(GreenhouseApiScraper):
    employer_name = 'Faire'
    EMPLOYER_KEY = 'faire'


class HipcampScraper(LeverScraper):
    employer_name = 'Hipcamp'
    EMPLOYER_KEY = 'hipcamp'


class PlaceScraper(GreenhouseScraper):
    employer_name = 'Place'
    EMPLOYER_KEY = 'place'


class NorthoneScraper(GreenhouseScraper):
    employer_name = 'NorthOne'
    EMPLOYER_KEY = 'northone'


class DriftScraper(GreenhouseApiScraper):
    employer_name = 'Drift'
    EMPLOYER_KEY = 'drift'


class HiroScraper(LeverScraper):
    employer_name = 'Hiro'
    EMPLOYER_KEY = 'hiro'


class ZenefitsScraper(GreenhouseScraper):
    employer_name = 'Zenefits'
    EMPLOYER_KEY = 'zenefits'


class UniswapScraper(GreenhouseScraper):
    employer_name = 'Uniswap'
    EMPLOYER_KEY = 'uniswaplabs'


class VeepeeScraper(LeverScraper):
    employer_name = 'Veepee'
    EMPLOYER_KEY = 'veepee'


class ShipiumScraper(GreenhouseApiScraper):
    employer_name = 'Shipium'
    EMPLOYER_KEY = 'shipium'


class SigfigScraper(LeverScraper):
    employer_name = 'SigFig'
    EMPLOYER_KEY = 'sigfig-2'


class HorizenLabsScraper(GreenhouseScraper):
    employer_name = 'Horizen Labs'
    EMPLOYER_KEY = 'horizenlabs'


class FictivScraper(GreenhouseScraper):
    employer_name = 'Fictiv'
    EMPLOYER_KEY = 'fictiv'


class CreatordaoScraper(GreenhouseScraper):
    employer_name = 'CreatorDAO'
    EMPLOYER_KEY = 'creatordao'


class InstrumentalScraper(LeverScraper):
    employer_name = 'Instrumental'
    EMPLOYER_KEY = 'instrumental'


class FourkitesScraper(GreenhouseScraper):
    employer_name = 'FourKites'
    EMPLOYER_KEY = 'fourkites'


class VrchatScraper(LeverScraper):
    employer_name = 'VRChat'
    EMPLOYER_KEY = 'vrchat'


class LinearScraper(AshbyHQScraper):
    employer_name = 'Linear'
    EMPLOYER_KEY = 'Linear'


class TaxfixScraper(GreenhouseApiScraper):
    employer_name = 'Taxfix'
    EMPLOYER_KEY = 'taxfix'


class PerchScraper(GreenhouseApiScraper):
    employer_name = 'Perch'
    EMPLOYER_KEY = 'perchhq'


class RampNetworkScraper(LeverScraper):
    employer_name = 'Ramp Network'
    EMPLOYER_KEY = 'careers.ramp.network'


class FireworkScraper(GreenhouseScraper):
    employer_name = 'Firework'
    EMPLOYER_KEY = 'fireworkcareers'


class KayakScraper(GreenhouseScraper):
    employer_name = 'Kayak'
    EMPLOYER_KEY = 'kayak'


class StytchScraper(AshbyHQScraper):
    employer_name = 'Stytch'
    EMPLOYER_KEY = 'stytch'


class TalonScraper(GreenhouseScraper):
    employer_name = 'Talon'
    EMPLOYER_KEY = 'taloncybersecurity'


class DominoScraper(GreenhouseApiScraper):
    employer_name = 'Domino'
    EMPLOYER_KEY = 'dominodatalab'


class StokeScraper(GreenhouseApiScraper):
    employer_name = 'STOKE'
    EMPLOYER_KEY = 'stoke'


class BloomreachScraper(GreenhouseScraper):
    employer_name = 'Bloomreach'
    EMPLOYER_KEY = 'bloomreach'


class VintedScraper(GreenhouseApiScraper):
    employer_name = 'Vinted'
    EMPLOYER_KEY = 'vinteduab'


class TravelperkScraper(GreenhouseApiScraper):
    employer_name = 'TravelPerk'
    EMPLOYER_KEY = 'travelperk'


class OaknorthScraper(LeverScraper):
    employer_name = 'OakNorth'
    EMPLOYER_KEY = 'oaknorth.ai'


class TrustMachinesScraper(GreenhouseScraper):
    employer_name = 'Trust Machines'
    EMPLOYER_KEY = 'trustmachines'


class HelpshiftScraper(LeverScraper):
    employer_name = 'Helpshift'
    EMPLOYER_KEY = 'helpshift'


class InventaScraper(LeverScraper):
    employer_name = 'Inventa'
    EMPLOYER_KEY = 'inventa'


class LightningLabsScraper(AshbyHQScraper):
    employer_name = 'Lightning Labs'
    EMPLOYER_KEY = 'lightning'


class ActivecampaignScraper(LeverScraper):
    employer_name = 'ActiveCampaign'
    EMPLOYER_KEY = 'activecampaign'


class VettedScraper(LeverScraper):
    employer_name = 'Vetted'
    EMPLOYER_KEY = 'vetted'


class TallyScraper(GreenhouseScraper):
    employer_name = 'Tally'
    EMPLOYER_KEY = 'tally'


class BitpandaScraper(GreenhouseScraper):
    employer_name = 'Bitpanda'
    EMPLOYER_KEY = 'bitpanda'


class ThunkableScraper(LeverScraper):
    employer_name = 'Thunkable'
    EMPLOYER_KEY = 'thunkable'


class FrontifyScraper(LeverScraper):
    employer_name = 'Frontify'
    EMPLOYER_KEY = 'frontify'


class DegreedScraper(GreenhouseScraper):
    employer_name = 'Degreed'
    EMPLOYER_KEY = 'degreed'


class SafeaiScraper(LeverScraper):
    employer_name = 'SafeAI'
    EMPLOYER_KEY = 'safeai'


class CommonwealthScraper(GreenhouseScraper):
    employer_name = 'Commonwealth'
    EMPLOYER_KEY = 'commonwealth'


class NamelyScraper(GreenhouseApiScraper):
    employer_name = 'Namely'
    EMPLOYER_KEY = 'namely6'


class TrendyolScraper(LeverScraper):
    employer_name = 'Trendyol'
    EMPLOYER_KEY = 'trendyol'


class OfferupScraper(GreenhouseScraper):
    employer_name = 'OfferUp'
    EMPLOYER_KEY = 'offerup'


class WisetackScraper(GreenhouseScraper):
    employer_name = 'Wisetack'
    EMPLOYER_KEY = 'wisetack'


class CommerceiqScraper(GreenhouseScraper):
    employer_name = 'CommerceIQ'
    EMPLOYER_KEY = 'commerceiq'


class AptdecoScraper(LeverScraper):
    employer_name = 'AptDeco'
    EMPLOYER_KEY = 'apt-deco'


class LacedScraper(LeverScraper):
    employer_name = 'Laced'
    EMPLOYER_KEY = 'Laced'


class QontoScraper(LeverScraper):
    employer_name = 'Qonto'
    EMPLOYER_KEY = 'qonto'


class JackpocketScraper(GreenhouseScraper):
    employer_name = 'Jackpocket'
    EMPLOYER_KEY = 'jackpocket'


class FixieScraper(GreenhouseScraper):
    employer_name = 'Fixie'
    EMPLOYER_KEY = 'fixieai'


class OutreachScraper(LeverScraper):
    employer_name = 'Outreach'
    EMPLOYER_KEY = 'outreach'


class VenafiScraper(GreenhouseScraper):
    employer_name = 'Venafi'
    EMPLOYER_KEY = 'venafi'


class OtriumScraper(GreenhouseScraper):
    employer_name = 'Otrium'
    EMPLOYER_KEY = 'otrium'


class SemgrepScraper(GreenhouseScraper):
    employer_name = 'Semgrep'
    EMPLOYER_KEY = 'semgrep'


class DottScraper(LeverScraper):
    employer_name = 'Dott'
    EMPLOYER_KEY = 'dott'


class ZillizScraper(GreenhouseApiScraper):
    employer_name = 'Zilliz'
    EMPLOYER_KEY = 'zilliz'


class ProductboardScraper(GreenhouseApiScraper):
    employer_name = 'Productboard'
    EMPLOYER_KEY = 'productboard'


class BasetenScraper(AshbyHQScraper):
    employer_name = 'BaseTen'
    EMPLOYER_KEY = 'baseten'


class ConnecteamScraper(GreenhouseApiScraper):
    employer_name = 'Connecteam'
    EMPLOYER_KEY = 'connecteam'


class StubhubScraper(LeverScraper):
    employer_name = 'StubHub'
    EMPLOYER_KEY = 'StubHubHoldings'


class BanyanSecurityScraper(GreenhouseScraper):
    employer_name = 'Banyan Security'
    EMPLOYER_KEY = 'banyansecurity'


class TaptapSendScraper(LeverScraper):
    employer_name = 'Taptap Send'
    EMPLOYER_KEY = 'taptapsend'


class SpotAiScraper(GreenhouseScraper):
    employer_name = 'Spot AI'
    EMPLOYER_KEY = 'spotai'


class WatershedScraper(GreenhouseApiScraper):
    employer_name = 'Watershed'
    EMPLOYER_KEY = 'watershedclimate'


class HyperscienceScraper(LeverScraper):
    employer_name = 'Hyperscience'
    EMPLOYER_KEY = 'hyperscience'


class CortexScraper(AshbyHQScraper):
    employer_name = 'Cortex'
    EMPLOYER_KEY = 'cortex'


class SupportlogicScraper(GreenhouseScraper):
    employer_name = 'SupportLogic'
    EMPLOYER_KEY = 'supportlogic'


class BeewiseScraper(GreenhouseApiScraper):
    employer_name = 'Beewise'
    EMPLOYER_KEY = 'beewise'


class MindtickleScraper(LeverScraper):
    employer_name = 'MindTickle'
    EMPLOYER_KEY = 'mindtickle'


class GrabangoScraper(GreenhouseScraper):
    employer_name = 'Grabango'
    EMPLOYER_KEY = 'grabango'


class RoboflowScraper(LeverScraper):
    employer_name = 'Roboflow'
    EMPLOYER_KEY = 'roboflow'


class HostingerScraper(LeverScraper):
    employer_name = 'Hostinger'
    EMPLOYER_KEY = 'hostinger'


class EnchargeAiScraper(GreenhouseScraper):
    employer_name = 'EnCharge AI'
    EMPLOYER_KEY = 'enchargeai'


class BerealScraper(GreenhouseScraper):
    employer_name = 'BeReal'
    EMPLOYER_KEY = 'bereal'


class FullstoryScraper(GreenhouseApiScraper):
    employer_name = 'Fullstory'
    EMPLOYER_KEY = 'fullstory'


class QuoraScraper(AshbyHQScraper):
    employer_name = 'Quora'
    EMPLOYER_KEY = 'quora'


class GensynScraper(AshbyHQScraper):
    employer_name = 'Gensyn'
    EMPLOYER_KEY = 'gensyn'


class MashginScraper(LeverScraper):
    employer_name = 'Mashgin'
    EMPLOYER_KEY = 'mashgin'


class LucidScraper(GreenhouseScraper):
    employer_name = 'Lucid'
    EMPLOYER_KEY = 'lucidsoftware'


class ScanditScraper(GreenhouseApiScraper):
    employer_name = 'Scandit'
    EMPLOYER_KEY = 'scandit'


class RelyanceAiScraper(GreenhouseScraper):
    employer_name = 'Relyance AI'
    EMPLOYER_KEY = 'relyance'


class IllumioScraper(GreenhouseApiScraper):
    employer_name = 'Illumio'
    EMPLOYER_KEY = 'illumio'


class CoactiveAiScraper(GreenhouseScraper):
    employer_name = 'Coactive AI'
    EMPLOYER_KEY = 'coactivesystems'


class BenchsciScraper(LeverScraper):
    employer_name = 'BenchSci'
    EMPLOYER_KEY = 'benchsci'


class SmartrecruitersScraper(SmartRecruitersScraper):
    employer_name = 'SmartRecruiters'
    EMPLOYER_KEY = 'smartrecruiters'


class NetographyScraper(GreenhouseApiScraper):
    employer_name = 'Netography'
    EMPLOYER_KEY = 'netography'


class AxiosHqScraper(GreenhouseScraper):
    employer_name = 'Axios HQ'
    EMPLOYER_KEY = 'axioshq1'


class HebbiaScraper(GreenhouseScraper):
    employer_name = 'Hebbia'
    EMPLOYER_KEY = 'hebbia'


class AppzenScraper(LeverScraper):
    employer_name = 'AppZen'
    EMPLOYER_KEY = 'appzen'


class HumaneScraper(GreenhouseScraper):
    employer_name = 'Humane'
    EMPLOYER_KEY = 'humane'


class CymulateScraper(GreenhouseApiScraper):
    employer_name = 'Cymulate'
    EMPLOYER_KEY = 'cymulate'


class TruepicScraper(GreenhouseScraper):
    employer_name = 'Truepic'
    EMPLOYER_KEY = 'truepiccareers'


class IntrinsicScraper(GreenhouseApiScraper):
    employer_name = 'Intrinsic'
    EMPLOYER_KEY = 'intrinsicrobotics'


class XageSecurityScraper(LeverScraper):
    employer_name = 'Xage Security'
    EMPLOYER_KEY = 'xage-security'


class TiaScraper(GreenhouseScraper):
    employer_name = 'Tia'
    EMPLOYER_KEY = 'tia'


class TradeRepublicScraper(GreenhouseApiScraper):
    employer_name = 'Trade Republic'
    EMPLOYER_KEY = 'traderepublicbank'


class MenloSecurityScraper(GreenhouseScraper):
    employer_name = 'Menlo Security'
    EMPLOYER_KEY = 'menlosecurity'


class CheckScraper(GreenhouseScraper):
    employer_name = 'Check'
    EMPLOYER_KEY = 'check'


class WeavegridScraper(GreenhouseApiScraper):
    employer_name = 'WeaveGrid'
    EMPLOYER_KEY = 'weavegrid'


class TaxbitScraper(GreenhouseScraper):
    employer_name = 'TaxBit'
    EMPLOYER_KEY = 'taxbit'


class Unit410Scraper(GreenhouseScraper):
    employer_name = 'Unit 410'
    EMPLOYER_KEY = 'u410'


class SpecteropsScraper(GreenhouseScraper):
    employer_name = 'SpecterOps'
    EMPLOYER_KEY = 'specterops'


class SemtechScraper(WorkdayScraper):
    employer_name = 'Semtech'
    start_url = 'https://semtech.wd1.myworkdayjobs.com/en-US/SemtechCareers/'
    has_job_departments = False


class WovenPlanetScraper(LeverScraper):
    employer_name = 'Woven Planet'
    EMPLOYER_KEY = 'woven-by-toyota'


class GametimeScraper(LeverScraper):
    employer_name = 'Gametime'
    EMPLOYER_KEY = 'gametime'


class NexhealthScraper(GreenhouseApiScraper):
    employer_name = 'NexHealth'
    EMPLOYER_KEY = 'nexhealth'


class JustworksScraper(GreenhouseApiScraper):
    employer_name = 'Justworks'
    EMPLOYER_KEY = 'justworks'


class GofundmeScraper(GreenhouseScraper):
    employer_name = 'GoFundMe'
    EMPLOYER_KEY = 'gofundme'


class DomoScraper(GreenhouseScraper):
    employer_name = 'Domo'
    EMPLOYER_KEY = 'domo'


class KajabiScraper(GreenhouseApiScraper):
    employer_name = 'Kajabi'
    EMPLOYER_KEY = 'kajabi'


class AllscriptsScraper(GreenhouseApiScraper):
    employer_name = 'Allscripts'
    EMPLOYER_KEY = 'allscripts'


class BitmexScraper(GreenhouseScraper):
    employer_name = 'Bitmex'
    EMPLOYER_KEY = 'bitmex'


class SlingshotAerospaceScraper(GreenhouseApiScraper):
    employer_name = 'Slingshot Aerospace'
    EMPLOYER_KEY = 'slingshotaerospace'


class ManomanoScraper(LeverScraper):
    employer_name = 'ManoMano'
    EMPLOYER_KEY = 'manomano'


class QualiaScraper(GreenhouseScraper):
    employer_name = 'Qualia'
    EMPLOYER_KEY = 'qualia'


class TakeTwoInteractiveScraper(GreenhouseApiScraper):
    employer_name = 'Take-Two Interactive'
    EMPLOYER_KEY = 'taketwo'


class HarrysRazorCoScraper(GreenhouseScraper):
    employer_name = 'Harry\'s Razor Co'
    EMPLOYER_KEY = 'harrys'


class OpenseaScraper(LeverScraper):
    employer_name = 'OpenSea'
    EMPLOYER_KEY = 'OpenSea'


class VantaScraper(AshbyHQScraper):
    employer_name = 'Vanta'
    EMPLOYER_KEY = 'vanta'


class DydxScraper(GreenhouseScraper):
    employer_name = 'dYdX'
    EMPLOYER_KEY = 'dydx'


class SardineScraper(AshbyHQScraper):
    employer_name = 'Sardine'
    EMPLOYER_KEY = 'sardine'


class ClickatellScraper(GreenhouseScraper):
    employer_name = 'Clickatell'
    EMPLOYER_KEY = 'clickatell18'


class WetransferScraper(AshbyHQScraper):
    employer_name = 'WeTransfer'
    EMPLOYER_KEY = 'wetransfer'


class RemitlyScraper(WorkdayScraper):
    employer_name = 'Remitly'
    start_url = 'https://remitly.wd5.myworkdayjobs.com/en-US/Remitly_Careers/'
    has_job_departments = False


class SkydanceMediaScraper(LeverScraper):
    employer_name = 'Skydance Media'
    EMPLOYER_KEY = 'skydance'


class OptimismScraper(GreenhouseScraper):
    employer_name = 'Optimism'
    EMPLOYER_KEY = 'oplabs'


class PalantirScraper(LeverScraper):
    employer_name = 'Palantir'
    EMPLOYER_KEY = 'palantir'


class SalesloftScraper(GreenhouseApiScraper):
    employer_name = 'SalesLoft'
    EMPLOYER_KEY = 'salesloft'


class NearScraper(GreenhouseScraper):
    employer_name = 'NEAR'
    EMPLOYER_KEY = 'near'


class PoshmarkScraper(GreenhouseScraper):
    employer_name = 'Poshmark'
    EMPLOYER_KEY = 'poshmark'


class CoalfireScraper(LeverScraper):
    employer_name = 'Coalfire'
    EMPLOYER_KEY = 'coalfire'


class RivosScraper(LeverScraper):
    employer_name = 'Rivos'
    EMPLOYER_KEY = 'rivosinc'
