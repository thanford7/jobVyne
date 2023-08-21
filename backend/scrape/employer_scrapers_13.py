from scrape.base_scrapers import GreenhouseIframeScraper, GreenhouseScraper, LeverScraper


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
