from scrape.base_scrapers import AshbyHQScraper, BambooHrScraper, GreenhouseApiScraper, GreenhouseScraper, LeverScraper


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
