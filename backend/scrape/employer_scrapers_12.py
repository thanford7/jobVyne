from scrape.base_scrapers import AshbyHQScraper, GreenhouseApiScraper, GreenhouseScraper, LeverScraper, \
    SmartRecruitersScraper, WorkdayScraper


class DaveScraper(LeverScraper):
    employer_name = 'Dave'
    EMPLOYER_KEY = 'dave'


class FoxtrotScraper(LeverScraper):
    employer_name = 'Foxtrot'
    EMPLOYER_KEY = 'foxtrotco'


class HydrowScraper(LeverScraper):
    employer_name = 'Hydrow'
    EMPLOYER_KEY = 'Hydrow'


class ShiftTechnologyScraper(GreenhouseApiScraper):
    employer_name = 'Shift Technology'
    EMPLOYER_KEY = 'shifttechnology'


class WorkriseScraper(GreenhouseScraper):
    employer_name = 'Workrise'
    EMPLOYER_KEY = 'workrise'


class OxioScraper(LeverScraper):
    employer_name = 'OXIO'
    EMPLOYER_KEY = 'oxio'


class FlowScraper(LeverScraper):
    employer_name = 'Flow'
    EMPLOYER_KEY = 'flowlife'


class FlinkScraper(SmartRecruitersScraper):
    employer_name = 'Flink'
    EMPLOYER_KEY = 'Flink3'


class NoyoScraper(LeverScraper):
    employer_name = 'Noyo'
    EMPLOYER_KEY = 'noyo'


class SidecarHealthScraper(GreenhouseScraper):
    employer_name = 'Sidecar Health'
    EMPLOYER_KEY = 'sidecarhealth'


class TendScraper(LeverScraper):
    employer_name = 'Tend'
    EMPLOYER_KEY = 'tend'


class BokuScraper(GreenhouseApiScraper):
    employer_name = 'Boku'
    EMPLOYER_KEY = 'boku'


class ZenEducateScraper(LeverScraper):
    employer_name = 'Zen Educate'
    EMPLOYER_KEY = 'zeneducate'


class YounitedScraper(LeverScraper):
    employer_name = 'Younited'
    EMPLOYER_KEY = 'younited'


class ShiftsmartScraper(AshbyHQScraper):
    employer_name = 'Shiftsmart'
    EMPLOYER_KEY = 'shiftsmart'


class ClearStreetScraper(GreenhouseScraper):
    employer_name = 'Clear Street'
    EMPLOYER_KEY = 'clearstreet'


class StitchScraper(GreenhouseScraper):
    employer_name = 'Stitch'
    EMPLOYER_KEY = 'stitchmoneyptyltd'


class LinqiaScraper(GreenhouseApiScraper):
    employer_name = 'Linqia'
    EMPLOYER_KEY = 'linqia'


class HumanCapitalScraper(GreenhouseApiScraper):
    employer_name = 'Human Capital'
    EMPLOYER_KEY = 'humancapital'


class PelagoScraper(LeverScraper):
    employer_name = 'Pelago'
    EMPLOYER_KEY = 'pelago'


class SuperblocksScraper(GreenhouseScraper):
    employer_name = 'Superblocks'
    EMPLOYER_KEY = 'superblocks'


class HeliogenScraper(GreenhouseApiScraper):
    employer_name = 'Heliogen'
    EMPLOYER_KEY = 'heliogen'


class VastScraper(GreenhouseApiScraper):
    employer_name = 'Vast'
    EMPLOYER_KEY = 'vast'


class OwlLabsScraper(GreenhouseApiScraper):
    employer_name = 'Owl Labs'
    EMPLOYER_KEY = 'owllabs'


class OusterScraper(LeverScraper):
    employer_name = 'Ouster'
    EMPLOYER_KEY = 'ouster'


class AnyboticsScraper(LeverScraper):
    employer_name = 'ANYbotics'
    EMPLOYER_KEY = 'anybotics'


class EnervenueScraper(GreenhouseApiScraper):
    employer_name = 'EnerVenue'
    EMPLOYER_KEY = 'enervenue'


class ImpulseScraper(AshbyHQScraper):
    employer_name = 'Impulse'
    EMPLOYER_KEY = 'impulse'


class PykaScraper(GreenhouseScraper):
    employer_name = 'Pyka'
    EMPLOYER_KEY = 'pyka'


class KodiakRoboticsScraper(LeverScraper):
    employer_name = 'Kodiak Robotics'
    EMPLOYER_KEY = 'kodiak'


class DetectScraper(GreenhouseScraper):
    employer_name = 'Detect'
    EMPLOYER_KEY = 'homodeus1'


class GeckoRoboticsScraper(GreenhouseApiScraper):
    employer_name = 'Gecko Robotics'
    EMPLOYER_KEY = 'geckorobotics'


class BoomSupersonicScraper(GreenhouseScraper):
    employer_name = 'Boom Supersonic'
    EMPLOYER_KEY = 'boomsupersonic'


class AstraScraper(LeverScraper):
    employer_name = 'Astra'
    EMPLOYER_KEY = 'astra'


class NomagicScraper(LeverScraper):
    employer_name = 'Nomagic'
    EMPLOYER_KEY = 'Nomagic'


class FoundryDigitalScraper(GreenhouseScraper):
    employer_name = 'Foundry Digital'
    EMPLOYER_KEY = 'foundrydigital'


class VeoScraper(GreenhouseApiScraper):
    employer_name = 'Veo'
    EMPLOYER_KEY = 'veorobotics'


class OdysAviationScraper(LeverScraper):
    employer_name = 'Odys Aviation'
    EMPLOYER_KEY = 'OdysAviation'


class KargoScraper(GreenhouseScraper):
    employer_name = 'Kargo'
    EMPLOYER_KEY = 'kargo'


class QuantumscapeScraper(LeverScraper):
    employer_name = 'QuantumScape'
    EMPLOYER_KEY = 'quantumscape'


class AutostoreScraper(WorkdayScraper):
    employer_name = 'AutoStore'
    start_url = 'https://autostore.wd3.myworkdayjobs.com/en-US/autostore/'
    has_job_departments = False


class KeplerScraper(LeverScraper):
    employer_name = 'Kepler'
    EMPLOYER_KEY = 'kepler'


class MomentusScraper(GreenhouseApiScraper):
    employer_name = 'Momentus'
    EMPLOYER_KEY = 'momentus'


class ThirdWaveAutomationScraper(GreenhouseApiScraper):
    employer_name = 'Third Wave Automation'
    EMPLOYER_KEY = 'thirdwaveautomation'


class ReachScraper(LeverScraper):
    employer_name = 'Reach'
    EMPLOYER_KEY = 'reachpower'


class FormicScraper(GreenhouseScraper):
    employer_name = 'Formic'
    EMPLOYER_KEY = 'formic'


class PsiquantumScraper(GreenhouseApiScraper):
    employer_name = 'PsiQuantum'
    EMPLOYER_KEY = 'psiquantum'


class FulfilScraper(GreenhouseScraper):
    employer_name = 'Fulfil'
    EMPLOYER_KEY = 'fulfil'


class ScytheScraper(GreenhouseScraper):
    employer_name = 'Scythe'
    EMPLOYER_KEY = 'scytherobotics'


class AmpRoboticsScraper(GreenhouseApiScraper):
    employer_name = 'AMP Robotics'
    EMPLOYER_KEY = 'amprobotics'


class EightSleepScraper(AshbyHQScraper):
    employer_name = 'Eight Sleep'
    EMPLOYER_KEY = 'eightsleep'


class AgileSpaceScraper(GreenhouseScraper):
    employer_name = 'AGILE Space'
    EMPLOYER_KEY = 'agilespaceindustries'


class LilacScraper(GreenhouseScraper):
    employer_name = 'Lilac'
    EMPLOYER_KEY = 'lilacsolutionsinc'


class AevaScraper(LeverScraper):
    employer_name = 'Aeva'
    EMPLOYER_KEY = 'aeva'


class AtomicMachinesScraper(LeverScraper):
    employer_name = 'Atomic Machines'
    EMPLOYER_KEY = 'atomicmachines'


class WheelScraper(GreenhouseScraper):
    employer_name = 'Wheel'
    EMPLOYER_KEY = 'wheel'


class CorelightScraper(GreenhouseScraper):
    employer_name = 'Corelight'
    EMPLOYER_KEY = 'corelight'


class ModernfiScraper(AshbyHQScraper):
    employer_name = 'ModernFi'
    EMPLOYER_KEY = 'modernfi'


class ManypetsScraper(GreenhouseApiScraper):
    employer_name = 'ManyPets'
    EMPLOYER_KEY = 'manygroup'


class SharecareScraper(WorkdayScraper):
    employer_name = 'Sharecare'
    start_url = 'https://sharecare.wd1.myworkdayjobs.com/en-US/Sharecare_Careers/'
    has_job_departments = False


class TastyTradeScraper(GreenhouseApiScraper):
    employer_name = 'tastytrade'
    EMPLOYER_KEY = 'tastytrade'


class TorcScraper(GreenhouseScraper):
    employer_name = 'Torc'
    EMPLOYER_KEY = 'torcrobotics'


class HawkAiScraper(GreenhouseScraper):
    employer_name = 'Hawk AI'
    EMPLOYER_KEY = 'hawkai'


class PomeloScraper(GreenhouseScraper):
    employer_name = 'Pomelo'
    EMPLOYER_KEY = 'pomelo'


class GocardlessScraper(GreenhouseScraper):
    employer_name = 'GoCardless'
    EMPLOYER_KEY = 'gocardless'


class TrueworkScraper(GreenhouseScraper):
    employer_name = 'Truework'
    EMPLOYER_KEY = 'truework'


class PaidyScraper(GreenhouseScraper):
    employer_name = 'Paidy'
    EMPLOYER_KEY = 'paidyinc'


class AlanScraper(LeverScraper):
    employer_name = 'Alan'
    EMPLOYER_KEY = 'alan'


class EverlawScraper(GreenhouseScraper):
    employer_name = 'Everlaw'
    EMPLOYER_KEY = 'everlaw'


class NovaCreditScraper(LeverScraper):
    employer_name = 'Nova Credit'
    EMPLOYER_KEY = 'neednova'


class DhiGroupScraper(GreenhouseScraper):
    employer_name = 'DHI Group'
    EMPLOYER_KEY = 'dhigroupinc'


class CelestiaScraper(LeverScraper):
    employer_name = 'Celestia'
    EMPLOYER_KEY = 'celestia'


class ClassyScraper(GreenhouseApiScraper):
    employer_name = 'Classy'
    EMPLOYER_KEY = 'classy'


class BvnkScraper(GreenhouseScraper):
    employer_name = 'BVNK'
    EMPLOYER_KEY = 'bvnk'


class HackeroneScraper(LeverScraper):
    employer_name = 'HackerOne'
    EMPLOYER_KEY = 'hackerone'


class FigureFinancialScraper(GreenhouseScraper):
    employer_name = 'Figure Financial'
    EMPLOYER_KEY = 'figure'


class KadmosScraper(GreenhouseApiScraper):
    employer_name = 'Kadmos'
    EMPLOYER_KEY = 'kadmos3'


class CloverHealthScraper(GreenhouseApiScraper):
    employer_name = 'Clover Health'
    EMPLOYER_KEY = 'cloverhealth'


class SnaplogicScraper(LeverScraper):
    employer_name = 'SnapLogic'
    EMPLOYER_KEY = 'snaplogic'


class BookingScraper(WorkdayScraper):
    employer_name = 'Booking'
    start_url = 'https://priceline.wd1.myworkdayjobs.com/en-US/BookingHoldings/'
    has_job_departments = False


class EasypostScraper(LeverScraper):
    employer_name = 'EasyPost'
    EMPLOYER_KEY = 'easypost-2'


class MeatiFoodsScraper(GreenhouseScraper):
    employer_name = 'Meati Foods'
    EMPLOYER_KEY = 'meatifoods'
    
    
class MomentusTechnologiesScraper(SmartRecruitersScraper):
    employer_name = 'Momentus Technologies'
    EMPLOYER_KEY = 'MomentusTechnologies'
