from scrape.base_scrapers import AshbyHQScraper, GreenhouseApiScraper, GreenhouseScraper, LeverScraper, \
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
