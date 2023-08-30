from scrape.base_scrapers import BambooHrScraper, GreenhouseApiScraper, GreenhouseIframeScraper, GreenhouseScraper, \
    LeverScraper, \
    PaylocityScraper, \
    PhenomPeopleScraper, SmartRecruitersScraper, UltiProScraper, WorkdayScraper


class MapleScraper(LeverScraper):
    employer_name = 'Maple'
    EMPLOYER_KEY = 'maple-finance'
    
    
class FiCollarScraper(LeverScraper):
    employer_name = 'Fi Collar'
    EMPLOYER_KEY = 'fi'
    
    
class CovariantScraper(LeverScraper):
    employer_name = 'Covariant'
    EMPLOYER_KEY = 'covariant'
    
    
class CorestreamScraper(LeverScraper):
    employer_name = 'Corestream'
    EMPLOYER_KEY = 'corestream'


class PossibleFinanceScraper(GreenhouseScraper):
    employer_name = 'Possible Finance'
    EMPLOYER_KEY = 'possiblefinancialinc'
    
    
class SignifyHealthScraper(GreenhouseIframeScraper):
    employer_name = 'Signify Health'
    EMPLOYER_KEY = 'signifyhealth'
    
    
class SkillableScraper(PaylocityScraper):
    employer_name = 'Skillable'
    start_url = 'https://recruiting.paylocity.com/recruiting/jobs/All/680f151f-b1e8-48cc-b07c-689df54fa3b4/Skillable'
    
    
class KraftHeinzScraper(WorkdayScraper):
    employer_name = 'KraftHeinz'
    start_url = 'https://heinz.wd1.myworkdayjobs.com/en-US/KraftHeinz_Careers'
    has_job_departments = False
    
    
class FlorenceHealthcareScraper(GreenhouseScraper):
    employer_name = 'Florence Healthcare'
    EMPLOYER_KEY = 'florencehealthcare'
    
    
class SunLifeScraper(WorkdayScraper):
    employer_name = 'Sun Life'
    start_url = 'https://sunlife.wd3.myworkdayjobs.com/en-US/Experienced-Jobs'
    has_job_departments = False
    
    
class TheTrevorProjectScraper(LeverScraper):
    employer_name = 'The Trevor Project'
    EMPLOYER_KEY = 'thetrevorproject'
    
    
class EvolentHealthScraper(WorkdayScraper):
    employer_name = 'Evolent Health'
    start_url = 'https://evolent.wd1.myworkdayjobs.com/External'
    has_job_departments = False
    
    
class MercerAdvisorsScraper(UltiProScraper):
    employer_name = 'Mercer Advisors Inc'
    start_url = 'https://recruiting2.ultipro.com/MER1031MRGA/JobBoard/28d24fb4-1c0a-422a-9afa-f8ec27c7a728/'
    
    
class ExperianScraper(SmartRecruitersScraper):
    employer_name = 'Experian'
    EMPLOYER_KEY = 'Experian'
    

class EunaSolutionsScraper(BambooHrScraper):
    employer_name = 'EUNA Solutions'
    EMPLOYER_KEY = 'euna'
    
    
class OlaplexScraper(GreenhouseIframeScraper):
    employer_name = 'Olaplex'
    EMPLOYER_KEY = 'olaplexcareers'
    
    
class BloomerangScraper(GreenhouseScraper):
    employer_name = 'Bloomerang'
    EMPLOYER_KEY = 'bloomerang'
    
    
class CohereHealthScraper(GreenhouseIframeScraper):
    employer_name = 'Cohere Health'
    EMPLOYER_KEY = 'coherehealth'
    
    
class UpsideScraper(GreenhouseApiScraper):
    employer_name = 'Upside'
    EMPLOYER_KEY = 'ericbuckleygetupsidegreenhouseio'
    
    
class SnapIncScraper(WorkdayScraper):
    employer_name = 'Snap Inc'
    start_url = 'https://wd1.myworkdaysite.com/recruiting/snapchat/snap'
    has_job_departments = False
    
    
class CenteneCorporationScraper(PhenomPeopleScraper):
    employer_name = 'Centene Corporation'
    start_url = 'https://jobs.centene.com/us/en/search-results'
    
    
class AdobeScraper(PhenomPeopleScraper):
    employer_name = 'Adobe'
    start_url = 'https://careers.adobe.com/us/en/search-results'
    
    
class YelpScraper(PhenomPeopleScraper):
    employer_name = 'Yelp'
    start_url = 'https://www.yelp.careers/us/en/search-results'
    
    
class GeneralElectricScraper(PhenomPeopleScraper):
    employer_name = 'General Electric'
    start_url = 'https://jobs.gecareers.com/global/en/search-results'
    
    
class AspenDentalScraper(PhenomPeopleScraper):
    employer_name = 'Aspen Dental'
    start_url = 'https://careers.aspendental.com/us/en/search-results'
    

class ThermoFisherScraper(PhenomPeopleScraper):
    employer_name = 'Thermo Fisher Scientific'
    start_url = 'https://jobs.thermofisher.com/global/en/search-results'
    
    
class IgniteReadingScraper(GreenhouseIframeScraper):
    employer_name = 'Ignite! Reading'
    EMPLOYER_KEY = 'ignitereading'
    
    
class GreifScraper(WorkdayScraper):
    employer_name = 'Greif'
    start_url = 'https://greif.wd5.myworkdayjobs.com/Greif'
    has_job_departments = False
    
    
class CircanaScraper(UltiProScraper):
    employer_name = 'Circana'
    start_url = 'https://recruiting2.ultipro.com/INF1019IRINC/JobBoard/17a8d008-9efe-4e51-8460-47ee205d5229/'
    
    
class ScribeScraper(GreenhouseIframeScraper):
    employer_name = 'Scribe'
    EMPLOYER_KEY = 'scribe'
