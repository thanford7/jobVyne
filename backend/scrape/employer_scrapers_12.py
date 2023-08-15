from scrape.base_scrapers import AshbyHQScraper, BreezyScraper, GreenhouseApiScraper, GreenhouseIframeScraper, \
    GreenhouseScraper, LeverScraper, \
    SmartRecruitersScraper, UltiProScraper, WorkdayScraper


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


class CarbonHealthScraper(LeverScraper):
    employer_name = 'Carbon Health'
    EMPLOYER_KEY = 'carbonhealth'


class RiseUpScraper(SmartRecruitersScraper):
    employer_name = 'Rise Up'
    EMPLOYER_KEY = 'RiseUp'


class SondermindScraper(GreenhouseScraper):
    employer_name = 'SonderMind'
    EMPLOYER_KEY = 'sondermind'


class ConvelioScraper(LeverScraper):
    employer_name = 'Convelio'
    EMPLOYER_KEY = 'convelio'


class CanaryTechnologiesScraper(LeverScraper):
    employer_name = 'Canary Technologies'
    EMPLOYER_KEY = 'canarytechnologies'


class SaltboxScraper(GreenhouseScraper):
    employer_name = 'Saltbox'
    EMPLOYER_KEY = 'saltbox'


class DreamGamesScraper(LeverScraper):
    employer_name = 'Dream Games'
    EMPLOYER_KEY = 'dreamgames'


class OrcaBioScraper(LeverScraper):
    employer_name = 'Orca Bio'
    EMPLOYER_KEY = 'orcabiosystems'


class MindmazeScraper(SmartRecruitersScraper):
    employer_name = 'MindMaze'
    EMPLOYER_KEY = 'MindMaze'


class WishScraper(SmartRecruitersScraper):
    employer_name = 'Wish'
    EMPLOYER_KEY = 'Wish'


class NfiniteScraper(GreenhouseScraper):
    employer_name = 'nfinite'
    EMPLOYER_KEY = 'nfinite'


class SynthegoScraper(LeverScraper):
    employer_name = 'Synthego'
    EMPLOYER_KEY = 'synthego'


class AtlanScraper(LeverScraper):
    employer_name = 'Atlan'
    EMPLOYER_KEY = 'atlan'


class GearsetScraper(LeverScraper):
    employer_name = 'Gearset'
    EMPLOYER_KEY = 'gearset'


class NotableScraper(AshbyHQScraper):
    employer_name = 'Notable'
    EMPLOYER_KEY = 'notable'


class NourishIngredientsScraper(GreenhouseScraper):
    employer_name = 'Nourish Ingredients'
    EMPLOYER_KEY = 'nourishingredients'


class AltamlScraper(LeverScraper):
    employer_name = 'AltaML'
    EMPLOYER_KEY = 'altaml'


class MakersFundScraper(GreenhouseScraper):
    employer_name = 'Makers Fund'
    EMPLOYER_KEY = 'makersfund'


class InsightsoftwareScraper(SmartRecruitersScraper):
    employer_name = 'insightsoftware'
    EMPLOYER_KEY = 'Insightsoftware'


class RefyneScraper(SmartRecruitersScraper):
    employer_name = 'Refyne'
    EMPLOYER_KEY = 'Refyne'


class FirstRoundScraper(LeverScraper):
    employer_name = 'First Round'
    EMPLOYER_KEY = 'firstround'


class TripleliftScraper(GreenhouseApiScraper):
    employer_name = 'TripleLift'
    EMPLOYER_KEY = 'triplelift'


class VroomScraper(WorkdayScraper):
    employer_name = 'Vroom'
    start_url = 'https://vroom.wd5.myworkdayjobs.com/en-US/vroom/'
    has_job_departments = False


class ArcticWolfScraper(WorkdayScraper):
    employer_name = 'Arctic Wolf'
    start_url = 'https://arcticwolf.wd1.myworkdayjobs.com/External/'
    has_job_departments = False


class GetaroundScraper(LeverScraper):
    employer_name = 'Getaround'
    EMPLOYER_KEY = 'getaround'


class MantraHealthScraper(GreenhouseScraper):
    employer_name = 'Mantra Health'
    EMPLOYER_KEY = 'mantrahealth'


class TheRoundsScraper(LeverScraper):
    employer_name = 'The Rounds'
    EMPLOYER_KEY = 'therounds'


class LittleOtterScraper(LeverScraper):
    employer_name = 'Little Otter'
    EMPLOYER_KEY = 'littleotter'


class BrightlineScraper(AshbyHQScraper):
    employer_name = 'Brightline'
    EMPLOYER_KEY = 'hellobrightline'


class MonumentScraper(LeverScraper):
    employer_name = 'Monument'
    EMPLOYER_KEY = 'joinmonument-2'


class TalkspaceScraper(GreenhouseApiScraper):
    employer_name = 'Talkspace'
    EMPLOYER_KEY = 'talkspace'


class Science37Scraper(GreenhouseScraper):
    employer_name = 'Science 37'
    EMPLOYER_KEY = 'science37'


class IntelycareScraper(LeverScraper):
    employer_name = 'IntelyCare'
    EMPLOYER_KEY = 'intelycare'


class BicycleHealthScraper(GreenhouseApiScraper):
    employer_name = 'Bicycle Health'
    EMPLOYER_KEY = 'bicyclehealth'


class NeurobladeScraper(GreenhouseScraper):
    employer_name = 'NeuroBlade'
    EMPLOYER_KEY = 'neuroblade'


class AltoPharmacyScraper(GreenhouseApiScraper):
    employer_name = 'Alto Pharmacy'
    EMPLOYER_KEY = 'alto'


class BraveHealthScraper(GreenhouseScraper):
    employer_name = 'Brave Health'
    EMPLOYER_KEY = 'bravehealth'


class JourneyClinicalScraper(LeverScraper):
    employer_name = 'Journey Clinical'
    EMPLOYER_KEY = 'JourneyClinical'


class PrenuvoScraper(GreenhouseApiScraper):
    employer_name = 'Prenuvo'
    EMPLOYER_KEY = 'prenuvo'


class TwentyThreeAndmeScraper(GreenhouseApiScraper):
    employer_name = '23andMe'
    EMPLOYER_KEY = '23andme'


class EdenHealthScraper(LeverScraper):
    employer_name = 'Eden Health'
    EMPLOYER_KEY = 'edenhealth'


class SonatusScraper(LeverScraper):
    employer_name = 'Sonatus'
    EMPLOYER_KEY = 'sonatus'


class TusimpleScraper(GreenhouseScraper):
    employer_name = 'TuSimple'
    EMPLOYER_KEY = 'tusimple'


class BoweryScraper(LeverScraper):
    employer_name = 'Bowery'
    EMPLOYER_KEY = 'boweryfarming'


class CommonScraper(GreenhouseScraper):
    employer_name = 'Common'
    EMPLOYER_KEY = 'common'


class JamaSoftwareScraper(GreenhouseApiScraper):
    employer_name = 'Jama Software'
    EMPLOYER_KEY = 'jamasoftware'


class AntoraEnergyScraper(GreenhouseScraper):
    employer_name = 'Antora Energy'
    EMPLOYER_KEY = 'antora'


class EffyScraper(SmartRecruitersScraper):
    employer_name = 'Effy'
    EMPLOYER_KEY = 'Effy'


class SpotonScraper(GreenhouseScraper):
    employer_name = 'SpotOn'
    EMPLOYER_KEY = 'spotonproduct'


class TeamsharesScraper(LeverScraper):
    employer_name = 'Teamshares'
    EMPLOYER_KEY = 'teamshares'


class RedfinScraper(WorkdayScraper):
    employer_name = 'Redfin'
    start_url = 'https://redfin.wd1.myworkdayjobs.com/en-US/redfin_careers/'
    has_job_departments = False


class TomoScraper(GreenhouseScraper):
    employer_name = 'Tomo'
    EMPLOYER_KEY = 'tomonetworks'


class FlockHomesScraper(GreenhouseScraper):
    employer_name = 'Flock Homes'
    EMPLOYER_KEY = 'flockhomes'


class OrchardScraper(GreenhouseScraper):
    employer_name = 'Orchard'
    EMPLOYER_KEY = 'orchard'


class FlyhomesScraper(GreenhouseScraper):
    employer_name = 'Flyhomes'
    EMPLOYER_KEY = 'flyhomes'


class ValonScraper(GreenhouseScraper):
    employer_name = 'Valon'
    EMPLOYER_KEY = 'valon'


class IndustriousScraper(GreenhouseScraper):
    employer_name = 'Industrious'
    EMPLOYER_KEY = 'industrious'


class HomewardScraper(GreenhouseScraper):
    employer_name = 'Homeward'
    EMPLOYER_KEY = 'homeward'


class CalendlyScraper(GreenhouseApiScraper):
    employer_name = 'Calendly'
    EMPLOYER_KEY = 'calendly'


class AyaHealthcareScraper(GreenhouseApiScraper):
    employer_name = 'Aya Healthcare'
    EMPLOYER_KEY = 'ayahealthcare'


class AbInBevScraper(GreenhouseScraper):
    employer_name = 'AB InBev'
    EMPLOYER_KEY = 'abinbev'


class ThousandEyesScraper(GreenhouseScraper):
    employer_name = 'ThousandEyes'
    EMPLOYER_KEY = 'thousandeyes'


class ArgoGroupScraper(GreenhouseScraper):
    employer_name = 'Argo Group'
    EMPLOYER_KEY = 'argo83'


class MindfulCareScraper(GreenhouseApiScraper):
    employer_name = 'Mindful Care'
    EMPLOYER_KEY = 'mindfulcare'


class RecodeTherapeuticsScraper(GreenhouseApiScraper):
    employer_name = 'ReCode Therapeutics'
    EMPLOYER_KEY = 'recodetherapeutics'


class ConvivaScraper(GreenhouseApiScraper):
    employer_name = 'Conviva'
    EMPLOYER_KEY = 'conviva'


class PantheonScraper(GreenhouseApiScraper):
    employer_name = 'Pantheon'
    EMPLOYER_KEY = 'pantheon'


class GrahamCapitalScraper(GreenhouseApiScraper):
    employer_name = 'Graham Capital Management'
    EMPLOYER_KEY = 'grahamcapitalmanagement'


class FinancialTimesScraper(GreenhouseApiScraper):
    employer_name = 'Financial Times'
    EMPLOYER_KEY = 'financialtimes33'


class CenterScraper(LeverScraper):
    employer_name = 'Center'
    EMPLOYER_KEY = 'getcenter'


class ScaledAgileScraper(SmartRecruitersScraper):
    employer_name = 'Scaled Agile, Inc.'
    EMPLOYER_KEY = 'ScaledAgileInc'


class FylloScraper(GreenhouseScraper):
    employer_name = 'Fyllo'
    EMPLOYER_KEY = 'fyllo'


class OptoInvestmentsScraper(GreenhouseApiScraper):
    employer_name = 'Opto Investments'
    EMPLOYER_KEY = 'optoinvest'


class ExtraHopScraper(GreenhouseIframeScraper):
    employer_name = 'ExtraHop'
    EMPLOYER_KEY = 'extrahopnetworks'


class BeyondLimitsScraper(GreenhouseApiScraper):
    employer_name = 'Beyond Limits'
    EMPLOYER_KEY = 'beyondlimits'


class KenshoScraper(LeverScraper):
    employer_name = 'Kensho'
    EMPLOYER_KEY = 'kensho'


class OstroScraper(GreenhouseScraper):
    employer_name = 'Ostro'
    EMPLOYER_KEY = 'ostrohealth'


class WalkerEdisonScraper(GreenhouseIframeScraper):
    employer_name = 'Walker Edison'
    EMPLOYER_KEY = 'walkeredison'


class NuSkinScraper(WorkdayScraper):
    employer_name = 'Nu Skin'
    start_url = 'https://nuskin.wd5.myworkdayjobs.com/en-US/nuskin/'
    has_job_departments = False


class CustomerIoScraper(GreenhouseScraper):
    employer_name = 'Customer.io'
    EMPLOYER_KEY = 'customerio'


class PatternScraper(WorkdayScraper):
    employer_name = 'Pattern'
    start_url = 'https://pattern.wd1.myworkdayjobs.com/en-US/Pattern_Careers/'
    has_job_departments = False


class HeartFlowScraper(GreenhouseScraper):
    employer_name = 'Heartflow, Inc.'
    EMPLOYER_KEY = 'heartflowinc'


class CloudOpsScraper(GreenhouseIframeScraper):
    employer_name = 'CloudOps'
    EMPLOYER_KEY = 'cloudops'


class VevoScraper(LeverScraper):
    employer_name = 'Vevo'
    EMPLOYER_KEY = 'vevo'


class CelonisScraper(GreenhouseScraper):
    employer_name = 'Celonis'
    EMPLOYER_KEY = 'celonis'


class FlexportScraper(GreenhouseScraper):
    employer_name = 'Flexport'
    EMPLOYER_KEY = 'flexport'


class AppliedIntuitionScraper(GreenhouseScraper):
    employer_name = 'Applied Intuition'
    EMPLOYER_KEY = 'appliedintuition'


class SightlineMediaGroupScraper(GreenhouseScraper):
    employer_name = 'Sightline Media Group'
    EMPLOYER_KEY = 'sightlinemediagroup'


class DiscoScraper(GreenhouseApiScraper):
    employer_name = 'Disco'
    EMPLOYER_KEY = 'disco'


class IonGroupScraper(LeverScraper):
    employer_name = 'ION Group'
    EMPLOYER_KEY = 'ion'


class AledadeScraper(LeverScraper):
    employer_name = 'Aledade'
    EMPLOYER_KEY = 'aledade'


class NvidiaScraper(WorkdayScraper):
    employer_name = 'NVIDIA'
    start_url = 'https://nvidia.wd5.myworkdayjobs.com/en-us/nvidiaexternalcareersite/'
    has_job_departments = False


class DatabricksScraper(GreenhouseScraper):
    employer_name = 'Databricks'
    EMPLOYER_KEY = 'databricks'


class IxlLearningScraper(GreenhouseApiScraper):
    employer_name = 'IXL Learning'
    EMPLOYER_KEY = 'ixllearning'


class IntelScraper(WorkdayScraper):
    employer_name = 'Intel'
    start_url = 'https://intel.wd1.myworkdayjobs.com/en-us/external/'
    has_job_departments = False


class SentryScraper(GreenhouseScraper):
    employer_name = 'Sentry'
    EMPLOYER_KEY = 'sentry'


class FlynnCompaniesScraper(LeverScraper):
    employer_name = 'Flynn Companies'
    EMPLOYER_KEY = 'flynncompanies'


class WesternDigitalScraper(SmartRecruitersScraper):
    employer_name = 'Western Digital'
    EMPLOYER_KEY = 'WesternDigital'


class BondVetScraper(GreenhouseScraper):
    employer_name = 'Bond Vet'
    EMPLOYER_KEY = 'bondvet'


class PalantirScraper(LeverScraper):
    employer_name = 'Palantir'
    EMPLOYER_KEY = 'palantir'


class SpacexScraper(GreenhouseScraper):
    employer_name = 'SpaceX'
    EMPLOYER_KEY = 'spacex'


class SearchForCommonGroundScraper(LeverScraper):
    employer_name = 'Search for Common Ground'
    EMPLOYER_KEY = 'sfcg'


class CapitalOneScraper(WorkdayScraper):
    employer_name = 'Capital One'
    start_url = 'https://capitalone.wd1.myworkdayjobs.com/Capital_One/'
    has_job_departments = False


class RecogniScraper(GreenhouseScraper):
    employer_name = 'Recogni'
    EMPLOYER_KEY = 'recogni'


class ForwardScraper(LeverScraper):
    employer_name = 'Forward'
    EMPLOYER_KEY = 'goforward'


class BeneschScraper(GreenhouseScraper):
    employer_name = 'Benesch'
    EMPLOYER_KEY = 'alfredbeneschco'


class RobinhoodScraper(GreenhouseScraper):
    employer_name = 'Robinhood'
    EMPLOYER_KEY = 'robinhood'


class MediabrandsScraper(GreenhouseApiScraper):
    employer_name = 'Mediabrands'
    EMPLOYER_KEY = 'mediabrands'


class InCompassHealthScraper(LeverScraper):
    employer_name = 'In Compass Health'
    EMPLOYER_KEY = 'incompasshealth'


class OldMissionScraper(GreenhouseApiScraper):
    employer_name = 'Old Mission'
    EMPLOYER_KEY = 'oldmissioncapital'
