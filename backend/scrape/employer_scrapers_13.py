from scrape.base_scrapers import GreenhouseIframeScraper, GreenhouseScraper, LeverScraper, PaylocityScraper, \
    WorkdayScraper


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
