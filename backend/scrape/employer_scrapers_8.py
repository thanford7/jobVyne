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
    
    
