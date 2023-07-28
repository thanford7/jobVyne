from scrape.base_scrapers import AshbyHQScraper, GreenhouseApiScraper, GreenhouseScraper, LeverScraper, WorkdayScraper


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


class FilmhubScraper(AshbyHQScraper):
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


class AnrokScraper(AshbyHQScraper):
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


class AuroraSolarScraper(AshbyHQScraper):
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
