from scrape.base_scrapers import AshbyHQScraper, \
    GreenhouseApiScraper, \
    GreenhouseScraper, LeverScraper, SmartRecruitersScraper, \
    WorkdayScraper


class SleeperScraper(AshbyHQScraper):
    employer_name = 'Sleeper'
    EMPLOYER_KEY = 'sleeper'


class SamsaraScraper(GreenhouseApiScraper):
    employer_name = 'Samsara'
    EMPLOYER_KEY = 'samsara'


class AcronisScraper(GreenhouseScraper):
    employer_name = 'Acronis'
    EMPLOYER_KEY = 'acronis'


class WrapbookScraper(GreenhouseApiScraper):
    employer_name = 'Wrapbook'
    EMPLOYER_KEY = 'wrapbook'


class JamfScraper(GreenhouseApiScraper):
    employer_name = 'JAMF'
    EMPLOYER_KEY = 'jamf'


class LiquibaseScraper(GreenhouseApiScraper):
    employer_name = 'Liquibase'
    EMPLOYER_KEY = 'liquibase'


class GlintsScraper(LeverScraper):
    employer_name = 'Glints'
    EMPLOYER_KEY = 'glints'


class MudflapScraper(GreenhouseApiScraper):
    employer_name = 'Mudflap'
    EMPLOYER_KEY = 'mudflap'


class BabylonHealthScraper(GreenhouseScraper):
    employer_name = 'Babylon Health'
    EMPLOYER_KEY = 'babylon'


class KlueScraper(LeverScraper):
    employer_name = 'Klue'
    EMPLOYER_KEY = 'klue'


class AstranisScraper(GreenhouseScraper):
    employer_name = 'Astranis'
    EMPLOYER_KEY = 'astranis'


class OmnipresentScraper(GreenhouseScraper):
    employer_name = 'Omnipresent'
    EMPLOYER_KEY = 'omnipresent'


class TemplafyScraper(GreenhouseScraper):
    employer_name = 'Templafy'
    EMPLOYER_KEY = 'templafy'


class OutbrainScraper(GreenhouseScraper):
    employer_name = 'Outbrain'
    EMPLOYER_KEY = 'outbraininc'


class AssembledScraper(GreenhouseScraper):
    employer_name = 'Assembled'
    EMPLOYER_KEY = 'assembled'


class NiumScraper(LeverScraper):
    employer_name = 'Nium'
    EMPLOYER_KEY = 'nium'


class GwiScraper(GreenhouseApiScraper):
    employer_name = 'GWI'
    EMPLOYER_KEY = 'globalwebindex'


class Three60learningScraper(LeverScraper):
    employer_name = '360learning'
    EMPLOYER_KEY = '360learning'


class GrouponScraper(WorkdayScraper):
    employer_name = 'Groupon'
    start_url = 'https://grab.wd3.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class FiservScraper(WorkdayScraper):
    employer_name = 'Fiserv'
    start_url = 'https://fiserv.wd5.myworkdayjobs.com/en-US/EXT/'
    has_job_departments = False


class AspentechScraper(WorkdayScraper):
    employer_name = 'AspenTech'
    start_url = 'https://aspentech.wd5.myworkdayjobs.com/en-US/aspentech/'
    has_job_departments = False


class HazelHealthScraper(GreenhouseScraper):
    employer_name = 'Hazel Health'
    EMPLOYER_KEY = 'hazel'


class QumuloScraper(GreenhouseApiScraper):
    employer_name = 'Qumulo'
    EMPLOYER_KEY = 'qumulo'


class BlinkistScraper(GreenhouseScraper):
    employer_name = 'Blinkist'
    EMPLOYER_KEY = 'blinkist'


class SmartlyScraper(GreenhouseApiScraper):
    employer_name = 'Smartly'
    EMPLOYER_KEY = 'smartlyio'


class QualysScraper(WorkdayScraper):
    employer_name = 'Qualys'
    start_url = 'https://qualys.wd5.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class MobileyeScraper(LeverScraper):
    employer_name = 'Mobileye'
    EMPLOYER_KEY = 'mobileye'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class LumafieldScraper(LeverScraper):
    employer_name = 'Lumafield'
    EMPLOYER_KEY = 'lumafield'


class FisScraper(WorkdayScraper):
    employer_name = 'FIS'
    start_url = 'https://fis.wd5.myworkdayjobs.com/en-US/SearchJobs/'
    has_job_departments = False


class RingcentralScraper(WorkdayScraper):
    employer_name = 'RingCentral'
    start_url = 'https://ringcentral.wd1.myworkdayjobs.com/en-US/RingCentral_Careers/'
    has_job_departments = False


class BoxScraper(GreenhouseScraper):
    employer_name = 'Box'
    EMPLOYER_KEY = 'boxinc'


class UpguardScraper(LeverScraper):
    employer_name = 'UpGuard'
    EMPLOYER_KEY = 'upguard'


class TrendMicroScraper(WorkdayScraper):
    employer_name = 'Trend Micro'
    start_url = 'https://trendmicro.wd3.myworkdayjobs.com/en-US/External/'
    has_job_departments = False


class Auto1GroupScraper(SmartRecruitersScraper):
    employer_name = 'Auto1 Group'
    EMPLOYER_KEY = 'Auto1'


class PandadocScraper(GreenhouseApiScraper):
    employer_name = 'PandaDoc'
    EMPLOYER_KEY = 'pandadoc'


class TruliooScraper(GreenhouseApiScraper):
    employer_name = 'Trulioo'
    EMPLOYER_KEY = 'trulioo'


class PersonaScraper(LeverScraper):
    employer_name = 'Persona'
    EMPLOYER_KEY = 'persona'


class TigeraScraper(GreenhouseApiScraper):
    employer_name = 'Tigera'
    EMPLOYER_KEY = 'tigera'


class PeakAiScraper(GreenhouseScraper):
    employer_name = 'Peak AI'
    EMPLOYER_KEY = 'peakailimited'


class PitchbookScraper(GreenhouseScraper):
    employer_name = 'Pitchbook'
    EMPLOYER_KEY = 'pitchbookdata'


class DlocalScraper(LeverScraper):
    employer_name = 'dLocal'
    EMPLOYER_KEY = 'dlocal'


class MeritScraper(LeverScraper):
    employer_name = 'Merit'
    EMPLOYER_KEY = 'merit'


class LaceworkScraper(GreenhouseApiScraper):
    employer_name = 'Lacework'
    EMPLOYER_KEY = 'lacework'


class ApolloIoScraper(GreenhouseScraper):
    employer_name = 'Apollo.io'
    EMPLOYER_KEY = 'apolloio'


class ExpediaScraper(WorkdayScraper):
    employer_name = 'Expedia'
    start_url = 'https://expedia.wd5.myworkdayjobs.com/en-US/search/'
    has_job_departments = False


class KlookScraper(WorkdayScraper):
    employer_name = 'Klook'
    start_url = 'https://klook.wd3.myworkdayjobs.com/en-US/KlookCareers/'
    has_job_departments = False


class PreplyScraper(GreenhouseApiScraper):
    employer_name = 'Preply'
    EMPLOYER_KEY = 'preply'


class VectraAiScraper(GreenhouseScraper):
    employer_name = 'Vectra AI'
    EMPLOYER_KEY = 'vectranetworks'


class IncortaScraper(LeverScraper):
    employer_name = 'Incorta'
    EMPLOYER_KEY = 'incorta'


class ShelfIoScraper(GreenhouseApiScraper):
    employer_name = 'Shelf.io'
    EMPLOYER_KEY = 'shelf'


class PaymongoScraper(LeverScraper):
    employer_name = 'PayMongo'
    EMPLOYER_KEY = 'paymongo'


class TekionScraper(GreenhouseScraper):
    employer_name = 'Tekion'
    EMPLOYER_KEY = 'tekion'


class AlchemyScraper(GreenhouseScraper):
    employer_name = 'Alchemy'
    EMPLOYER_KEY = 'alchemy'


class AxiosScraper(GreenhouseScraper):
    employer_name = 'Axios'
    EMPLOYER_KEY = 'axios'


class GrailScraper(LeverScraper):
    employer_name = 'GRAIL'
    EMPLOYER_KEY = 'grailbio'


class RippleScraper(GreenhouseApiScraper):
    employer_name = 'Ripple'
    EMPLOYER_KEY = 'ripple'


class CandidlyScraper(GreenhouseScraper):
    employer_name = 'Candidly'
    EMPLOYER_KEY = 'candidly'


class OzowScraper(GreenhouseScraper):
    employer_name = 'Ozow'
    EMPLOYER_KEY = 'ozow'


class LatticeScraper(GreenhouseApiScraper):
    employer_name = 'Lattice'
    EMPLOYER_KEY = 'lattice'


class KnakScraper(GreenhouseApiScraper):
    employer_name = 'Knak'
    EMPLOYER_KEY = 'knak'


class DuolingoScraper(GreenhouseScraper):
    employer_name = 'Duolingo'
    EMPLOYER_KEY = 'duolingo'


class EvertrueScraper(GreenhouseApiScraper):
    employer_name = 'EverTrue'
    EMPLOYER_KEY = 'evertrue'


class LandingaiScraper(LeverScraper):
    employer_name = 'LandingAI'
    EMPLOYER_KEY = 'landing'


class EcoreScraper(GreenhouseScraper):
    employer_name = 'e-core'
    EMPLOYER_KEY = 'ecore'


class PostmanScraper(GreenhouseScraper):
    employer_name = 'Postman'
    EMPLOYER_KEY = 'postman'


class JobberScraper(GreenhouseScraper):
    employer_name = 'Jobber'
    EMPLOYER_KEY = 'jobber'


class GleanScraper(GreenhouseScraper):
    employer_name = 'Glean'
    EMPLOYER_KEY = 'gleanwork'


class MozillaScraper(GreenhouseScraper):
    employer_name = 'Mozilla'
    EMPLOYER_KEY = 'mozilla'


class RobloxScraper(GreenhouseApiScraper):
    employer_name = 'Roblox'
    EMPLOYER_KEY = 'roblox'


class EvolutioniqScraper(GreenhouseApiScraper):
    employer_name = 'EvolutionIQ'
    EMPLOYER_KEY = 'evolutioniq'


class HologramScraper(GreenhouseScraper):
    employer_name = 'Hologram'
    EMPLOYER_KEY = 'hologram'


class ClickupScraper(GreenhouseScraper):
    employer_name = 'ClickUp'
    EMPLOYER_KEY = 'clickup'


class SparrowScraper(GreenhouseScraper):
    employer_name = 'Sparrow'
    EMPLOYER_KEY = 'sparrow'


class WorkivaScraper(WorkdayScraper):
    employer_name = 'Workiva'
    start_url = 'https://workiva.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class RecoraScraper(GreenhouseScraper):
    employer_name = 'Recora'
    EMPLOYER_KEY = 'recorainc'


class MasterclassScraper(GreenhouseApiScraper):
    employer_name = 'Masterclass'
    EMPLOYER_KEY = 'masterclass'


class VendrScraper(GreenhouseScraper):
    employer_name = 'Vendr'
    EMPLOYER_KEY = 'vendr'


class OriginScraper(GreenhouseApiScraper):
    employer_name = 'Origin'
    EMPLOYER_KEY = 'originfinancial'


class LandisScraper(GreenhouseApiScraper):
    employer_name = 'Landis'
    EMPLOYER_KEY = 'landis'


class StellateScraper(GreenhouseScraper):
    employer_name = 'Stellate'
    EMPLOYER_KEY = 'stellate'


class RocketreachScraper(GreenhouseScraper):
    employer_name = 'RocketReach'
    EMPLOYER_KEY = 'rocketreach'


class ScaleScraper(GreenhouseScraper):
    employer_name = 'Scale'
    EMPLOYER_KEY = 'scaleai'


class RedisLabsScraper(GreenhouseApiScraper):
    employer_name = 'Redis Labs'
    EMPLOYER_KEY = 'redislabs'


class NarvarScraper(GreenhouseScraper):
    employer_name = 'Narvar'
    EMPLOYER_KEY = 'narvar'


class MethodScraper(GreenhouseScraper):
    employer_name = 'Method'
    EMPLOYER_KEY = 'method'


class HumaScraper(LeverScraper):
    employer_name = 'Huma'
    EMPLOYER_KEY = 'huma'


class N26Scraper(GreenhouseApiScraper):
    employer_name = 'N26'
    EMPLOYER_KEY = 'n26'


class CodecademyScraper(GreenhouseApiScraper):
    employer_name = 'Codecademy'
    EMPLOYER_KEY = 'codeacademy'


class FocalScraper(GreenhouseScraper):
    employer_name = 'Focal'
    EMPLOYER_KEY = 'focalsystems'


class PatreonScraper(GreenhouseScraper):
    employer_name = 'Patreon'
    EMPLOYER_KEY = 'patreon'


class NextdoorScraper(GreenhouseApiScraper):
    employer_name = 'Nextdoor'
    EMPLOYER_KEY = 'nextdoor'


class ShipbobScraper(GreenhouseScraper):
    employer_name = 'ShipBob'
    EMPLOYER_KEY = 'shipbobinc'


class NumeradeScraper(GreenhouseApiScraper):
    employer_name = 'Numerade'
    EMPLOYER_KEY = 'numeradecareers'


class VedaScraper(LeverScraper):
    employer_name = 'Veda'
    EMPLOYER_KEY = 'vedadata'


class HomeboundScraper(GreenhouseScraper):
    employer_name = 'Homebound'
    EMPLOYER_KEY = 'homebound'


class AtBayScraper(GreenhouseScraper):
    employer_name = 'At-Bay'
    EMPLOYER_KEY = 'atbayjobs'


class PayoneerScraper(GreenhouseApiScraper):
    employer_name = 'Payoneer'
    EMPLOYER_KEY = 'payoneer'


class AlgoliaScraper(GreenhouseScraper):
    employer_name = 'Algolia'
    EMPLOYER_KEY = 'algolia'


class HowlScraper(GreenhouseScraper):
    employer_name = 'Howl'
    EMPLOYER_KEY = 'howl'


class PursuitScraper(GreenhouseScraper):
    employer_name = 'Pursuit'
    EMPLOYER_KEY = 'pursuit'


class AirslateScraper(LeverScraper):
    employer_name = 'airSlate'
    EMPLOYER_KEY = 'airslate'


class LulaScraper(GreenhouseScraper):
    employer_name = 'Lula'
    EMPLOYER_KEY = 'lula'


class CamundaScraper(GreenhouseApiScraper):
    employer_name = 'Camunda'
    EMPLOYER_KEY = 'camundaservices'


class EfisheryScraper(GreenhouseScraper):
    employer_name = 'eFishery'
    EMPLOYER_KEY = 'efishery'
    
    def process_location_text(self, location_text):
        locations = super().process_location_text(location_text)
        new_locations = []
        for location in locations:
            if 'anywhere' in location.lower():
                location = 'Remote'
            elif 'office' in location.lower():
                location = 'Cimenyan, Indonesia'
            new_locations.append(location)
        return new_locations


class CleverScraper(GreenhouseApiScraper):
    employer_name = 'Clever'
    EMPLOYER_KEY = 'clever'


class AccelbyteScraper(GreenhouseApiScraper):
    employer_name = 'AccelByte'
    EMPLOYER_KEY = 'accelbyte'


class RidgelineScraper(GreenhouseApiScraper):
    employer_name = 'Ridgeline'
    EMPLOYER_KEY = 'ridgeline'


class ApiiroScraper(GreenhouseApiScraper):
    employer_name = 'Apiiro'
    EMPLOYER_KEY = 'apiiro'


class GateIoScraper(LeverScraper):
    employer_name = 'Gate.io'
    EMPLOYER_KEY = 'gate.io'


class ViaScraper(GreenhouseScraper):
    employer_name = 'Via'
    EMPLOYER_KEY = 'via'


class MomentiveScraper(GreenhouseScraper):
    employer_name = 'Momentive'
    EMPLOYER_KEY = 'surveymonkey'


class GlobalPaymentsScraper(WorkdayScraper):
    employer_name = 'Global Payments'
    start_url = 'https://tsys.wd1.myworkdayjobs.com/en-US/TSYS/'
    has_job_departments = False


class BubbleScraper(GreenhouseScraper):
    employer_name = 'Bubble'
    EMPLOYER_KEY = 'bubble'


class MatterLabsScraper(LeverScraper):
    employer_name = 'Matter Labs'
    EMPLOYER_KEY = 'matterlabs'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class GenDigitalScraper(WorkdayScraper):
    employer_name = 'Gen Digital'
    start_url = 'https://gen.wd1.myworkdayjobs.com/en-US/careers/'
    has_job_departments = False


class BitwardenScraper(GreenhouseApiScraper):
    employer_name = 'Bitwarden'
    EMPLOYER_KEY = 'bitwarden'


class SuperComScraper(LeverScraper):
    employer_name = 'Super.com'
    EMPLOYER_KEY = 'super-com'


class MatchGroupScraper(LeverScraper):
    employer_name = 'Match Group'
    EMPLOYER_KEY = 'matchgroup'


class BondFinancialScraper(GreenhouseScraper):
    employer_name = 'Bond Financial'
    EMPLOYER_KEY = 'bondfinancialtechnologies'


class FairmatScraper(LeverScraper):
    employer_name = 'Fairmat'
    EMPLOYER_KEY = 'Fairmat'


class TencentScraper(WorkdayScraper):
    employer_name = 'Tencent'
    start_url = 'https://tencent.wd1.myworkdayjobs.com/en-US/Tencent_Careers/'
    has_job_departments = False


class PineconeScraper(GreenhouseApiScraper):
    employer_name = 'Pinecone'
    EMPLOYER_KEY = 'hypercube'


class WeaveScraper(GreenhouseScraper):
    employer_name = 'Weave'
    EMPLOYER_KEY = 'weavehq'


class BrilliantScraper(LeverScraper):
    employer_name = 'Brilliant'
    EMPLOYER_KEY = 'brilliant'


class DuneAnalyticsScraper(AshbyHQScraper):
    employer_name = 'Dune Analytics'
    EMPLOYER_KEY = 'dune'


class Q2HoldingsScraper(WorkdayScraper):
    employer_name = 'Q2 Holdings'
    start_url = 'https://q2ebanking.wd5.myworkdayjobs.com/en-US/Q2/'
    has_job_departments = False


class UnitScraper(AshbyHQScraper):
    employer_name = 'Unit'
    EMPLOYER_KEY = 'unit'


class PanoramaScraper(GreenhouseScraper):
    employer_name = 'Panorama'
    EMPLOYER_KEY = 'panoramaed'


class InflectionAiScraper(GreenhouseScraper):
    employer_name = 'Inflection AI'
    EMPLOYER_KEY = 'inflectionai'


class ArizeAiScraper(GreenhouseScraper):
    employer_name = 'Arize AI'
    EMPLOYER_KEY = 'arizeai'


class FairmarkitScraper(GreenhouseApiScraper):
    employer_name = 'Fairmarkit'
    EMPLOYER_KEY = 'fairmarkit'


class StellarScraper(GreenhouseScraper):
    employer_name = 'Stellar'
    EMPLOYER_KEY = 'stellar'


class VirtruScraper(GreenhouseScraper):
    employer_name = 'Virtru'
    EMPLOYER_KEY = 'virtru'


class AsteraLabsScraper(GreenhouseScraper):
    employer_name = 'Astera Labs'
    EMPLOYER_KEY = 'asteralabs'


class FloScraper(GreenhouseScraper):
    employer_name = 'Flo'
    EMPLOYER_KEY = 'flohealth'


class InstaworkScraper(GreenhouseScraper):
    employer_name = 'Instawork'
    EMPLOYER_KEY = 'instawork'


class BankedScraper(GreenhouseScraper):
    employer_name = 'Banked'
    EMPLOYER_KEY = 'banked'


class WellthScraper(GreenhouseScraper):
    employer_name = 'Wellth'
    EMPLOYER_KEY = 'wellth'


class TwilioScraper(GreenhouseScraper):
    employer_name = 'Twilio'
    EMPLOYER_KEY = 'twilio'


class AgoricScraper(GreenhouseApiScraper):
    employer_name = 'Agoric'
    EMPLOYER_KEY = 'agoric'


class TigergraphScraper(GreenhouseScraper):
    employer_name = 'TigerGraph'
    EMPLOYER_KEY = 'tigergraph'


class EnteraScraper(GreenhouseScraper):
    employer_name = 'Entera'
    EMPLOYER_KEY = 'entera'


class DexterityScraper(LeverScraper):
    employer_name = 'Dexterity'
    EMPLOYER_KEY = 'dexterity'


class SennderScraper(GreenhouseApiScraper):
    employer_name = 'Sennder'
    EMPLOYER_KEY = 'sennder'


class ProtonScraper(GreenhouseScraper):
    employer_name = 'Proton'
    EMPLOYER_KEY = 'proton'


class HeadoutScraper(GreenhouseApiScraper):
    employer_name = 'Headout'
    EMPLOYER_KEY = 'headoutcareers'


class ChanZuckerbergScraper(GreenhouseApiScraper):
    employer_name = 'Chan Zuckerberg'
    EMPLOYER_KEY = 'chanzuckerberginitiative'


class PrintifyScraper(LeverScraper):
    employer_name = 'Printify'
    EMPLOYER_KEY = 'printify'


class WiseScraper(GreenhouseScraper):
    employer_name = 'Wise'
    EMPLOYER_KEY = 'transferwise'


class BcgDigitalScraper(GreenhouseApiScraper):
    employer_name = 'BCG Digital'
    EMPLOYER_KEY = 'bcgdv'


class SeonScraper(GreenhouseApiScraper):
    employer_name = 'Seon'
    EMPLOYER_KEY = 'seonfraudfighters'


class Pax8Scraper(GreenhouseApiScraper):
    employer_name = 'Pax8'
    EMPLOYER_KEY = 'pax8'


class FirstbaseScraper(AshbyHQScraper):
    employer_name = 'Firstbase'
    EMPLOYER_KEY = 'firstbaseio'


class RedwoodMaterialsScraper(GreenhouseApiScraper):
    employer_name = 'Redwood Materials'
    EMPLOYER_KEY = 'redwoodmaterials'


class IdMeScraper(GreenhouseScraper):
    employer_name = 'ID.me'
    EMPLOYER_KEY = 'idme'


class SnapdocsScraper(GreenhouseScraper):
    employer_name = 'Snapdocs'
    EMPLOYER_KEY = 'snapdocs'


class MparticleScraper(GreenhouseApiScraper):
    employer_name = 'mParticle'
    EMPLOYER_KEY = 'mparticle'


class StarburstScraper(LeverScraper):
    employer_name = 'Starburst'
    EMPLOYER_KEY = 'starburstdata'


class SprigScraper(GreenhouseScraper):
    employer_name = 'Sprig'
    EMPLOYER_KEY = 'sprig'


class BitsightScraper(WorkdayScraper):
    employer_name = 'BitSight'
    start_url = 'https://bitsight.wd1.myworkdayjobs.com/en-US/Bitsight/'
    has_job_departments = False


class NordSecurityScraper(LeverScraper):
    employer_name = 'Nord Security'
    EMPLOYER_KEY = 'nordsec'


class SkillzScraper(GreenhouseApiScraper):
    employer_name = 'Skillz'
    EMPLOYER_KEY = 'skillzinc'


class CoinflipScraper(LeverScraper):
    employer_name = 'CoinFlip'
    EMPLOYER_KEY = 'CoinFlip'


class KavaScraper(LeverScraper):
    employer_name = 'Kava'
    EMPLOYER_KEY = 'kava'


class LinkScraper(LeverScraper):
    employer_name = 'Link'
    EMPLOYER_KEY = 'link-money'


class StoriScraper(GreenhouseScraper):
    employer_name = 'Stori'
    EMPLOYER_KEY = 'storicardmx'


class ZetaScraper(LeverScraper):
    employer_name = 'Zeta'
    EMPLOYER_KEY = 'zeta'


class CerebralScraper(GreenhouseScraper):
    employer_name = 'Cerebral'
    EMPLOYER_KEY = 'cerebral'


class BeameryScraper(AshbyHQScraper):
    employer_name = 'Beamery'
    EMPLOYER_KEY = 'beamery'


class IxlLearningScraper(GreenhouseApiScraper):
    employer_name = 'IXL Learning'
    EMPLOYER_KEY = 'ixllearning'


class TransfrScraper(LeverScraper):
    employer_name = 'Transfr'
    EMPLOYER_KEY = 'transfrvr'


class MyntScraper(WorkdayScraper):
    employer_name = 'Mynt'
    start_url = 'https://globe.wd3.myworkdayjobs.com/en-US/Mynt/'
    has_job_departments = False


class C3AiScraper(GreenhouseScraper):
    employer_name = 'C3.ai'
    EMPLOYER_KEY = 'c3iot'


class ViamScraper(GreenhouseScraper):
    employer_name = 'Viam'
    EMPLOYER_KEY = 'viamrobotics'


class GorgiasScraper(AshbyHQScraper):
    employer_name = 'Gorgias'
    EMPLOYER_KEY = 'gorgias'


class ParkerScraper(GreenhouseScraper):
    employer_name = 'Parker'
    EMPLOYER_KEY = 'parker'


class SimplyScraper(GreenhouseApiScraper):
    employer_name = 'Simply'
    EMPLOYER_KEY = 'simply'


class TemporalScraper(LeverScraper):
    employer_name = 'Temporal'
    EMPLOYER_KEY = 'temporal'


class EverlywellScraper(LeverScraper):
    employer_name = 'EverlyWell'
    EMPLOYER_KEY = 'everlywell'


class BabbelScraper(GreenhouseApiScraper):
    employer_name = 'Babbel'
    EMPLOYER_KEY = 'babbel'


class LedgerScraper(LeverScraper):
    employer_name = 'Ledger'
    EMPLOYER_KEY = 'ledger'


class MelioScraper(GreenhouseScraper):
    employer_name = 'Melio'
    EMPLOYER_KEY = 'melio'


class OkcoinScraper(GreenhouseScraper):
    employer_name = 'OKcoin'
    EMPLOYER_KEY = 'okcoin'


class AsappScraper(LeverScraper):
    employer_name = 'Asapp'
    EMPLOYER_KEY = 'asapp-2'


class MoonfareScraper(GreenhouseScraper):
    employer_name = 'Moonfare'
    EMPLOYER_KEY = 'moonfareintnl'


class IsomorphicLabsScraper(GreenhouseScraper):
    employer_name = 'Isomorphic Labs'
    EMPLOYER_KEY = 'isomorphiclabs'


class OslScraper(GreenhouseScraper):
    employer_name = 'OSL'
    EMPLOYER_KEY = 'osl'


class PaveScraper(GreenhouseScraper):
    employer_name = 'Pave'
    EMPLOYER_KEY = 'paveakatroveinformationtechnologies'


class NuroScraper(GreenhouseApiScraper):
    employer_name = 'Nuro'
    EMPLOYER_KEY = 'nuro'


class OnetrustScraper(GreenhouseScraper):
    employer_name = 'OneTrust'
    EMPLOYER_KEY = 'onetrust'


class TrueaccordScraper(LeverScraper):
    employer_name = 'TrueAccord'
    EMPLOYER_KEY = 'trueaccord'


class ClarifaiScraper(GreenhouseApiScraper):
    employer_name = 'Clarifai'
    EMPLOYER_KEY = 'clarifai'