from scrape.base_scrapers import AshbyHQScraper, \
    GreenhouseApiScraper, \
    GreenhouseScraper, LeverScraper, SmartRecruitersScraper, \
    WorkdayScraper


class AsimovScraper(LeverScraper):
    employer_name = 'Asimov'
    EMPLOYER_KEY = 'asimov'


class H1Scraper(LeverScraper):
    employer_name = 'H1'
    EMPLOYER_KEY = 'h1'


class LyellImmunopharmaScraper(GreenhouseScraper):
    employer_name = 'Lyell Immunopharma'
    EMPLOYER_KEY = 'lyellimmunopharma'


class OpenzeppelinScraper(GreenhouseApiScraper):
    employer_name = 'OpenZeppelin'
    EMPLOYER_KEY = 'openzeppelin'


class JumpTradingScraper(GreenhouseApiScraper):
    employer_name = 'Jump Trading'
    EMPLOYER_KEY = 'jumptrading'


class IconScraper(GreenhouseApiScraper):
    employer_name = 'ICON'
    EMPLOYER_KEY = 'iconcareers'


class MimecastScraper(WorkdayScraper):
    employer_name = 'Mimecast'
    start_url = 'https://mimecast.wd5.myworkdayjobs.com/en-US/Mimecast-Careers/'
    has_job_departments = False


class ArtaFinanceScraper(AshbyHQScraper):
    employer_name = 'Arta Finance'
    EMPLOYER_KEY = 'artafinance'


class PortofinoScraper(SmartRecruitersScraper):
    employer_name = 'Portofino'
    EMPLOYER_KEY = 'PortofinoLtd'


class MorningConsultScraper(LeverScraper):
    employer_name = 'Morning Consult'
    EMPLOYER_KEY = 'morningconsult'


class CermatiScraper(SmartRecruitersScraper):
    employer_name = 'Cermati'
    EMPLOYER_KEY = 'Cermaticom'


class KitopiScraper(LeverScraper):
    employer_name = 'Kitopi'
    EMPLOYER_KEY = 'kitopi'


class RiskifiedScraper(GreenhouseApiScraper):
    employer_name = 'Riskified'
    EMPLOYER_KEY = 'riskified'


class FourthlineScraper(GreenhouseScraper):
    employer_name = 'Fourthline'
    EMPLOYER_KEY = 'fourthline'


class PremiseScraper(GreenhouseApiScraper):
    employer_name = 'Premise'
    EMPLOYER_KEY = 'premise'


class HigharcScraper(GreenhouseScraper):
    employer_name = 'Higharc'
    EMPLOYER_KEY = 'higharc'


class PipedriveScraper(LeverScraper):
    employer_name = 'Pipedrive'
    EMPLOYER_KEY = 'pipedrive'


class OnespanScraper(GreenhouseApiScraper):
    employer_name = 'OneSpan'
    EMPLOYER_KEY = 'onespan'


class AlarmComScraper(GreenhouseApiScraper):
    employer_name = 'Alarm.com'
    EMPLOYER_KEY = 'alarmcom'


class WonderScraper(GreenhouseScraper):
    employer_name = 'Wonder'
    EMPLOYER_KEY = 'careersatwonder'


class OnepasswordScraper(LeverScraper):
    employer_name = '1Password'
    EMPLOYER_KEY = '1password'


class MKopaScraper(LeverScraper):
    employer_name = 'M-KOPA'
    EMPLOYER_KEY = 'm-kopa'


class TomorrowHealthScraper(GreenhouseScraper):
    employer_name = 'Tomorrow Health'
    EMPLOYER_KEY = 'tomorrowhealth'


class FeedzaiScraper(GreenhouseApiScraper):
    employer_name = 'Feedzai'
    EMPLOYER_KEY = 'feedzai'


class VolocopterScraper(SmartRecruitersScraper):
    employer_name = 'Volocopter'
    EMPLOYER_KEY = 'VolocopterGmbH'


class HadrianScraper(LeverScraper):
    employer_name = 'Hadrian'
    EMPLOYER_KEY = 'hadrian'


class CdkGlobalScraper(WorkdayScraper):
    employer_name = 'CDK Global'
    start_url = 'https://cdk.wd1.myworkdayjobs.com/en-US/CDK/'
    has_job_departments = False


class ThymeCareScraper(GreenhouseApiScraper):
    employer_name = 'Thyme Care'
    EMPLOYER_KEY = 'thymecare'


class TabbyScraper(GreenhouseScraper):
    employer_name = 'Tabby'
    EMPLOYER_KEY = 'tabby'


class SkillsoftScraper(GreenhouseApiScraper):
    employer_name = 'Skillsoft'
    EMPLOYER_KEY = 'skillsoft'


class HumanSecurityScraper(LeverScraper):
    employer_name = 'Human Security'
    EMPLOYER_KEY = 'humansecurity'


class SwileScraper(LeverScraper):
    employer_name = 'Swile'
    EMPLOYER_KEY = 'swile'


class AnyscaleScraper(LeverScraper):
    employer_name = 'Anyscale'
    EMPLOYER_KEY = 'anyscale'


class HearthScraper(GreenhouseApiScraper):
    employer_name = 'Hearth'
    EMPLOYER_KEY = 'hearth'


class FlatironSchoolScraper(GreenhouseScraper):
    employer_name = 'Flatiron School'
    EMPLOYER_KEY = 'theflatironschool'


class OpenerScraper(LeverScraper):
    employer_name = 'Opener'
    EMPLOYER_KEY = 'opener'


class ShipmonkScraper(GreenhouseApiScraper):
    employer_name = 'ShipMonk'
    EMPLOYER_KEY = 'shipmonk'


class EzcaterScraper(GreenhouseApiScraper):
    employer_name = 'ezCater'
    EMPLOYER_KEY = 'ezcaterinc'


class RentTheRunwayScraper(GreenhouseScraper):
    employer_name = 'Rent the Runway'
    EMPLOYER_KEY = 'renttherunway'


class VeeamScraper(SmartRecruitersScraper):
    employer_name = 'Veeam'
    EMPLOYER_KEY = 'Veeam2'


class TopHatScraper(LeverScraper):
    employer_name = 'Top Hat'
    EMPLOYER_KEY = 'tophat'


class SoleraScraper(WorkdayScraper):
    employer_name = 'Solera'
    start_url = 'https://solera.wd5.myworkdayjobs.com/en-US/Global_Career_Site/'
    has_job_departments = False


class RazerScraper(WorkdayScraper):
    employer_name = 'Razer'
    start_url = 'https://razer.wd3.myworkdayjobs.com/en-US/Careers/'
    has_job_departments = False


class AdvanceIntelligenceScraper(GreenhouseScraper):
    employer_name = 'Advance Intelligence'
    EMPLOYER_KEY = 'advanceintelligencegroup'


class BarstoolSportsScraper(GreenhouseApiScraper):
    employer_name = 'Barstool Sports'
    EMPLOYER_KEY = 'barstoolsports'


class DesktopMetalScraper(GreenhouseScraper):
    employer_name = 'Desktop Metal'
    EMPLOYER_KEY = 'desktopmetal'


class NextivaScraper(GreenhouseApiScraper):
    employer_name = 'Nextiva'
    EMPLOYER_KEY = 'nextiva'


class PieInsuranceScraper(GreenhouseScraper):
    employer_name = 'Pie Insurance'
    EMPLOYER_KEY = 'pieinsurance'


class LyftScraper(GreenhouseApiScraper):
    employer_name = 'Lyft'
    EMPLOYER_KEY = 'lyft'


class AgicapScraper(LeverScraper):
    employer_name = 'Agicap'
    EMPLOYER_KEY = 'agicap'


class PoplarScraper(LeverScraper):
    employer_name = 'Poplar'
    EMPLOYER_KEY = 'poplarhomes'


class MarvellScraper(WorkdayScraper):
    employer_name = 'Marvell'
    start_url = 'https://marvell.wd1.myworkdayjobs.com/en-US/MarvellCareers/'
    has_job_departments = False


class UnityScraper(GreenhouseApiScraper):
    employer_name = 'Unity'
    EMPLOYER_KEY = 'unity3d'


class RecordedFutureScraper(GreenhouseScraper):
    employer_name = 'Recorded Future'
    EMPLOYER_KEY = 'recordedfuture'


class BlablacarScraper(LeverScraper):
    employer_name = 'BlaBlaCar'
    EMPLOYER_KEY = 'blablacar'


class ZooxScraper(LeverScraper):
    employer_name = 'Zoox'
    EMPLOYER_KEY = 'zoox'


class SnapprScraper(LeverScraper):
    employer_name = 'Snappr'
    EMPLOYER_KEY = 'snappr'


class ModernizingMedicineScraper(GreenhouseApiScraper):
    employer_name = 'Modernizing Medicine'
    EMPLOYER_KEY = 'modernizingmedicineinc'


class NcsoftWestScraper(GreenhouseScraper):
    employer_name = 'NCSoft West'
    EMPLOYER_KEY = 'ncsoftwest'


class CarsalesComScraper(SmartRecruitersScraper):
    employer_name = 'Carsales.com'
    EMPLOYER_KEY = 'carsales'


class GetyourguideScraper(GreenhouseApiScraper):
    employer_name = 'GetYourGuide'
    EMPLOYER_KEY = 'getyourguide'


class BigHealthScraper(LeverScraper):
    employer_name = 'Big Health'
    EMPLOYER_KEY = 'bighealth'


class YipitdataScraper(GreenhouseApiScraper):
    employer_name = 'YipitData'
    EMPLOYER_KEY = 'yipitdata'


class IndexVenturesScraper(LeverScraper):
    employer_name = 'Index Ventures'
    EMPLOYER_KEY = 'indexventures'


class TheProductionBoardScraper(GreenhouseScraper):
    employer_name = 'The Production Board'
    EMPLOYER_KEY = 'tpb'


class DunzoScraper(GreenhouseApiScraper):
    employer_name = 'Dunzo'
    EMPLOYER_KEY = 'dunzo13'


class TechstarsScraper(GreenhouseScraper):
    employer_name = 'TechStars'
    EMPLOYER_KEY = 'techstars57'


class AndreessenHorowitzScraper(GreenhouseApiScraper):
    employer_name = 'Andreessen Horowitz'
    EMPLOYER_KEY = 'a16z'


class YieldstreetScraper(GreenhouseScraper):
    employer_name = 'Yieldstreet'
    EMPLOYER_KEY = 'yieldstreet'


class PanteraCapitalScraper(LeverScraper):
    employer_name = 'Pantera Capital'
    EMPLOYER_KEY = 'panteracapital'


class InsitroScraper(GreenhouseScraper):
    employer_name = 'Insitro'
    EMPLOYER_KEY = 'insitro'


class BukuwarungScraper(LeverScraper):
    employer_name = 'BukuWarung'
    EMPLOYER_KEY = 'bukuwarung'


class InsiderScraper(LeverScraper):
    employer_name = 'Insider'
    EMPLOYER_KEY = 'useinsider'


class GrayscaleScraper(GreenhouseScraper):
    employer_name = 'Grayscale'
    EMPLOYER_KEY = 'grayscaleinvestments'


class SummitPartnersScraper(GreenhouseScraper):
    employer_name = 'Summit Partners'
    EMPLOYER_KEY = 'summitpartnerslp'


class RedesignHealthScraper(GreenhouseScraper):
    employer_name = 'Redesign Health'
    EMPLOYER_KEY = 'redesignhealth'


class PolymathVenturesScraper(GreenhouseApiScraper):
    employer_name = 'Polymath Ventures'
    EMPLOYER_KEY = 'polymathventures'


class CaisScraper(GreenhouseScraper):
    employer_name = 'CAIS'
    EMPLOYER_KEY = 'cais'


class SoundcloudScraper(GreenhouseApiScraper):
    employer_name = 'SoundCloud'
    EMPLOYER_KEY = 'soundcloud71'


class PolysignScraper(GreenhouseScraper):
    employer_name = 'PolySign'
    EMPLOYER_KEY = 'polysign'


class EthicScraper(GreenhouseApiScraper):
    employer_name = 'Ethic'
    EMPLOYER_KEY = 'ethicinvesting'


class OptoInvestmentsScraper(GreenhouseScraper):
    employer_name = 'Opto Investments'
    EMPLOYER_KEY = 'optoinvest'


class OnesourceScraper(WorkdayScraper):
    employer_name = 'OneSource'
    start_url = 'https://vhr-osvhr.wd1.myworkdayjobs.com/en-US/OSV_External_Career_Site/'
    has_job_departments = False


class SquarespaceScraper(GreenhouseApiScraper):
    employer_name = 'Squarespace'
    EMPLOYER_KEY = 'squarespace'


class RapidsosScraper(GreenhouseScraper):
    employer_name = 'RapidSOS'
    EMPLOYER_KEY = 'rapidsos'


class BungieScraper(GreenhouseScraper):
    employer_name = 'Bungie'
    EMPLOYER_KEY = 'bungie'


class DecileGroupScraper(LeverScraper):
    employer_name = 'Decile Group'
    EMPLOYER_KEY = 'decilegroup'


class DeezerScraper(SmartRecruitersScraper):
    employer_name = 'Deezer'
    EMPLOYER_KEY = 'Deezer'


class AmazeScraper(LeverScraper):
    employer_name = 'Amaze'
    EMPLOYER_KEY = 'amaze'


class UpgradeScraper(GreenhouseScraper):
    employer_name = 'Upgrade'
    EMPLOYER_KEY = 'upgrade'


class CryptoComScraper(LeverScraper):
    employer_name = 'Crypto.com'
    EMPLOYER_KEY = 'crypto'


class LivepersonScraper(GreenhouseScraper):
    employer_name = 'LivePerson'
    EMPLOYER_KEY = 'liveperson'


class FlywireScraper(SmartRecruitersScraper):
    employer_name = 'Flywire'
    EMPLOYER_KEY = 'Flywire1'


class RocketInternetScraper(SmartRecruitersScraper):
    employer_name = 'Rocket Internet'
    EMPLOYER_KEY = 'RocketInternet'


class FandomScraper(GreenhouseApiScraper):
    employer_name = 'Fandom'
    EMPLOYER_KEY = 'fandom'


class ViseScraper(GreenhouseScraper):
    employer_name = 'Vise'
    EMPLOYER_KEY = 'viseai'


class FoundersFactoryScraper(LeverScraper):
    employer_name = 'Founders Factory'
    EMPLOYER_KEY = 'foundersfactory'


class CanaanScraper(LeverScraper):
    employer_name = 'Canaan'
    EMPLOYER_KEY = 'canaan'


class AccoladeScraper(WorkdayScraper):
    employer_name = 'Accolade'
    start_url = 'https://osv-accolade.wd5.myworkdayjobs.com/en-US/External_Careers/'
    has_job_departments = False


class MxTechnologiesScraper(WorkdayScraper):
    employer_name = 'MX Technologies'
    start_url = 'https://mx.wd1.myworkdayjobs.com/en-US/EXT-MX/'
    has_job_departments = False


class GoodwaterCapitalScraper(LeverScraper):
    employer_name = 'Goodwater Capital'
    EMPLOYER_KEY = 'goodwatercap'


class AblSpaceScraper(LeverScraper):
    employer_name = 'ABL Space'
    EMPLOYER_KEY = 'ablspacesystems'


class MyndScraper(GreenhouseScraper):
    employer_name = 'Mynd'
    EMPLOYER_KEY = 'mynd'


class AngellistScraper(LeverScraper):
    employer_name = 'AngelList'
    EMPLOYER_KEY = 'angellist'


class SonderScraper(GreenhouseApiScraper):
    employer_name = 'Sonder'
    EMPLOYER_KEY = 'sonder'


class FiScraper(LeverScraper):
    employer_name = 'Fi'
    EMPLOYER_KEY = 'epifi'


class CockroachLabsScraper(GreenhouseApiScraper):
    employer_name = 'Cockroach Labs'
    EMPLOYER_KEY = 'cockroachlabs'


class CommercetoolsScraper(GreenhouseScraper):
    employer_name = 'Commercetools'
    EMPLOYER_KEY = 'commercetools'


class MariadbScraper(GreenhouseScraper):
    employer_name = 'MariaDB'
    EMPLOYER_KEY = 'mariadbplc'


class NightfallAiScraper(GreenhouseScraper):
    employer_name = 'Nightfall AI'
    EMPLOYER_KEY = 'nightfall'


class MethodFinancialScraper(AshbyHQScraper):
    employer_name = 'Method Financial'
    EMPLOYER_KEY = 'method'


class DigitaloceanScraper(GreenhouseApiScraper):
    employer_name = 'DigitalOcean'
    EMPLOYER_KEY = 'digitalocean98'


class LitmusScraper(GreenhouseScraper):
    employer_name = 'Litmus'
    EMPLOYER_KEY = 'litmus46'


class TaniumScraper(GreenhouseApiScraper):
    employer_name = 'Tanium'
    EMPLOYER_KEY = 'tanium'


class NetomiScraper(LeverScraper):
    employer_name = 'Netomi'
    EMPLOYER_KEY = 'netomi'


class VillagemdScraper(GreenhouseApiScraper):
    employer_name = 'VillageMD'
    EMPLOYER_KEY = 'villagemd'


class AttaboticsScraper(LeverScraper):
    employer_name = 'Attabotics'
    EMPLOYER_KEY = 'attabotics'


class LeanixScraper(GreenhouseApiScraper):
    employer_name = 'LeanIX'
    EMPLOYER_KEY = 'leanix'


class MavenirScraper(WorkdayScraper):
    employer_name = 'Mavenir'
    start_url = 'https://mavenir.wd1.myworkdayjobs.com/en-US/Mavenir_Careers/'
    has_job_departments = False


class CopadoScraper(GreenhouseApiScraper):
    employer_name = 'Copado'
    EMPLOYER_KEY = 'copado'


class SoftwareAgScraper(WorkdayScraper):
    employer_name = 'Software AG'
    start_url = 'https://softwareag.wd3.myworkdayjobs.com/en-US/REC_SAG_ext/'
    has_job_departments = False


class WellskyScraper(WorkdayScraper):
    employer_name = 'WellSky'
    start_url = 'https://wellsky.wd1.myworkdayjobs.com/en-US/WellSkyCareers/'
    has_job_departments = False


class FinastraScraper(WorkdayScraper):
    employer_name = 'Finastra'
    start_url = 'https://dh.wd3.myworkdayjobs.com/en-US/DHC/'
    has_job_departments = False


class CoupaScraper(LeverScraper):
    employer_name = 'Coupa'
    EMPLOYER_KEY = 'coupa'


class OrkesScraper(LeverScraper):
    employer_name = 'Orkes'
    EMPLOYER_KEY = 'Orkes'


class AppdirectScraper(GreenhouseScraper):
    employer_name = 'AppDirect'
    EMPLOYER_KEY = 'appdirect'


class AdHocScraper(GreenhouseScraper):
    employer_name = 'Ad Hoc'
    EMPLOYER_KEY = 'adhocteam'


class SendbirdScraper(GreenhouseApiScraper):
    employer_name = 'Sendbird'
    EMPLOYER_KEY = 'sendbird'


class QuotientTechScraper(LeverScraper):
    employer_name = 'Quotient Tech'
    EMPLOYER_KEY = 'quotient'


class BlueoceanScraper(LeverScraper):
    employer_name = 'BlueOcean'
    EMPLOYER_KEY = 'blueoceanai'


class PubmaticScraper(SmartRecruitersScraper):
    employer_name = 'PubMatic'
    EMPLOYER_KEY = 'PubMatic'


class ZerofoxScraper(LeverScraper):
    employer_name = 'ZeroFox'
    EMPLOYER_KEY = 'zerofox'


class RocketChatScraper(GreenhouseApiScraper):
    employer_name = 'Rocket.Chat'
    EMPLOYER_KEY = 'rocketchat'


class CongaScraper(SmartRecruitersScraper):
    employer_name = 'Conga'
    EMPLOYER_KEY = 'Conga'


class UshurScraper(LeverScraper):
    employer_name = 'Ushur'
    EMPLOYER_KEY = 'ushur'


class SailpointScraper(WorkdayScraper):
    employer_name = 'SailPoint'
    start_url = 'https://sailpoint.wd1.myworkdayjobs.com/en-US/SailPoint/'
    has_job_departments = False


class OlxScraper(LeverScraper):
    employer_name = 'OLX'
    EMPLOYER_KEY = 'olx'
    
    def get_start_url(self):
        return f'https://jobs.eu.lever.co/{self.EMPLOYER_KEY}/'


class PhreesiaScraper(WorkdayScraper):
    employer_name = 'Phreesia'
    start_url = 'https://phreesia.wd1.myworkdayjobs.com/en-US/Phreesia/'
    has_job_departments = False


class EnsembleScraper(WorkdayScraper):
    employer_name = 'Ensemble'
    start_url = 'https://ensemblehp.wd5.myworkdayjobs.com/en-US/EnsembleHealthPartnersCareers/'
    has_job_departments = False


class LinuxFoundationScraper(SmartRecruitersScraper):
    employer_name = 'Linux Foundation'
    EMPLOYER_KEY = 'LinuxFoundation'


class WeightsBiasesScraper(LeverScraper):
    employer_name = 'Weights & Biases'
    EMPLOYER_KEY = 'wandb'


class BrightspotScraper(LeverScraper):
    employer_name = 'Brightspot'
    EMPLOYER_KEY = 'brightspot'


class MagicScraper(LeverScraper):
    employer_name = 'Magic'
    EMPLOYER_KEY = 'magic'


class ServicetradeScraper(GreenhouseApiScraper):
    employer_name = 'ServiceTrade'
    EMPLOYER_KEY = 'servicetrade'


class SpreetailScraper(LeverScraper):
    employer_name = 'Spreetail'
    EMPLOYER_KEY = 'spreetail'


class MendelScraper(GreenhouseApiScraper):
    employer_name = 'Mendel'
    EMPLOYER_KEY = 'mendel'


class HelsingScraper(GreenhouseScraper):
    employer_name = 'Helsing'
    EMPLOYER_KEY = 'helsing'


class GlossgeniusScraper(GreenhouseScraper):
    employer_name = 'GlossGenius'
    EMPLOYER_KEY = 'glossgenius'


class BettercloudScraper(GreenhouseApiScraper):
    employer_name = 'BetterCloud'
    EMPLOYER_KEY = 'bettercloud'


class WorkeraScraper(GreenhouseScraper):
    employer_name = 'Workera'
    EMPLOYER_KEY = 'workera'


class MrYumScraper(GreenhouseScraper):
    employer_name = 'Mr Yum'
    EMPLOYER_KEY = 'mryum'


class LedgyScraper(GreenhouseApiScraper):
    employer_name = 'Ledgy'
    EMPLOYER_KEY = 'ledgy'


class LevelHomeScraper(GreenhouseScraper):
    employer_name = 'Level Home'
    EMPLOYER_KEY = 'levelhome'


class KinCartaScraper(GreenhouseApiScraper):
    employer_name = 'Kin + Carta'
    EMPLOYER_KEY = 'kinandcarta'


class BrexScraper(GreenhouseApiScraper):
    employer_name = 'Brex'
    EMPLOYER_KEY = 'brex'


class YugaLabsScraper(GreenhouseScraper):
    employer_name = 'Yuga Labs'
    EMPLOYER_KEY = 'yugalabs'


class HighnoteScraper(GreenhouseScraper):
    employer_name = 'Highnote'
    EMPLOYER_KEY = 'highnote'


class AbridgeScraper(LeverScraper):
    employer_name = 'Abridge'
    EMPLOYER_KEY = 'abridge'


class ClockworkScraper(GreenhouseScraper):
    employer_name = 'Clockwork'
    EMPLOYER_KEY = 'clockworksystems'


class FluxonScraper(GreenhouseApiScraper):
    employer_name = 'Fluxon'
    EMPLOYER_KEY = 'fluxon'


class NeonScraper(GreenhouseScraper):
    employer_name = 'Neon'
    EMPLOYER_KEY = 'neondatabase'


class EmbraceScraper(GreenhouseScraper):
    employer_name = 'Embrace'
    EMPLOYER_KEY = 'embrace'


class FormaAiScraper(GreenhouseScraper):
    employer_name = 'Forma.ai'
    EMPLOYER_KEY = 'formaaiinc'


class LumosScraper(GreenhouseScraper):
    employer_name = 'Lumos'
    EMPLOYER_KEY = 'lumos'


class PhaidraScraper(GreenhouseScraper):
    employer_name = 'Phaidra'
    EMPLOYER_KEY = 'phaidra'


class CuratedScraper(GreenhouseScraper):
    employer_name = 'Curated'
    EMPLOYER_KEY = 'curated'


class CeligoScraper(GreenhouseApiScraper):
    employer_name = 'Celigo'
    EMPLOYER_KEY = 'celigo'


class FigureScraper(GreenhouseScraper):
    employer_name = 'Figure'
    EMPLOYER_KEY = 'figureai'


class CowbellCyberScraper(GreenhouseScraper):
    employer_name = 'Cowbell Cyber'
    EMPLOYER_KEY = 'cowbellcyber'


class CurrentScraper(GreenhouseApiScraper):
    employer_name = 'Current'
    EMPLOYER_KEY = 'current81'


class TheAthleticScraper(LeverScraper):
    employer_name = 'The Athletic'
    EMPLOYER_KEY = 'theathletic'


class BlankStreetScraper(GreenhouseScraper):
    employer_name = 'Blank Street'
    EMPLOYER_KEY = 'blankstreet'


class RetoolScraper(GreenhouseScraper):
    employer_name = 'ReTool'
    EMPLOYER_KEY = 'retool'


class BuynomicsScraper(GreenhouseScraper):
    employer_name = 'Buynomics'
    EMPLOYER_KEY = 'buynomics'


class BittrexScraper(GreenhouseScraper):
    employer_name = 'Bittrex'
    EMPLOYER_KEY = 'bittrex'


class WaveScraper(GreenhouseApiScraper):
    employer_name = 'Wave'
    EMPLOYER_KEY = 'wavexr'


class CedarScraper(GreenhouseApiScraper):
    employer_name = 'Cedar'
    EMPLOYER_KEY = 'careportalinc'


class BelongScraper(GreenhouseScraper):
    employer_name = 'Belong'
    EMPLOYER_KEY = 'belonghome'


class MetropolisScraper(GreenhouseScraper):
    employer_name = 'Metropolis'
    EMPLOYER_KEY = 'metropolis'


class ZilchScraper(GreenhouseApiScraper):
    employer_name = 'Zilch'
    EMPLOYER_KEY = 'zilch'


class NisumScraper(LeverScraper):
    employer_name = 'Nisum'
    EMPLOYER_KEY = 'nisum'


class StriveworksScraper(GreenhouseScraper):
    employer_name = 'Striveworks'
    EMPLOYER_KEY = 'striveworks'


class CraftScraper(LeverScraper):
    employer_name = 'Craft'
    EMPLOYER_KEY = 'craft'


class WizelineScraper(GreenhouseApiScraper):
    employer_name = 'Wizeline'
    EMPLOYER_KEY = 'wizeline'


class KeyrockScraper(AshbyHQScraper):
    employer_name = 'Keyrock'
    EMPLOYER_KEY = 'keyrock'


class WizardScraper(GreenhouseApiScraper):
    employer_name = 'Wizard'
    EMPLOYER_KEY = 'wizardcommerce'


class MavrckScraper(GreenhouseScraper):
    employer_name = 'Mavrck'
    EMPLOYER_KEY = 'mavrck'


class WiskAeroScraper(LeverScraper):
    employer_name = 'Wisk Aero'
    EMPLOYER_KEY = 'wisk'


class HalcyonScraper(GreenhouseScraper):
    employer_name = 'Halcyon'
    EMPLOYER_KEY = 'halcyon'


class Form3Scraper(GreenhouseApiScraper):
    employer_name = 'Form3'
    EMPLOYER_KEY = 'form3'


class DigibeeScraper(GreenhouseScraper):
    employer_name = 'Digibee'
    EMPLOYER_KEY = 'digibeeinc'


class MarkforgedScraper(GreenhouseScraper):
    employer_name = 'MarkForged'
    EMPLOYER_KEY = 'markforged'


class SabreScraper(WorkdayScraper):
    employer_name = 'Sabre'
    start_url = 'https://sabre.wd1.myworkdayjobs.com/en-US/SabreJobs/'
    has_job_departments = False


class StradvisionScraper(GreenhouseScraper):
    employer_name = 'StradVision'
    EMPLOYER_KEY = 'stradvision'


class NotionScraper(GreenhouseScraper):
    employer_name = 'Notion'
    EMPLOYER_KEY = 'notion'