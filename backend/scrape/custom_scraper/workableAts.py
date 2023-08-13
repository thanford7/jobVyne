import datetime
import logging
import os
import re
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

import requests

from jvapp.models.employer import Employer
from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none
from jvapp.utils.money import parse_compensation_text
from scrape.base_scrapers import WorkableScraper, get_recent_scraped_job_urls
from scrape.custom_scraper.workable_company_whitelist import company_whitelist
from scrape.job_processor import JobItem, ScrapedJobProcessor

logger = logging.getLogger(__name__)

key_map = {
    'title': 'job_title',
    'date': 'first_posted_date',
    'url': 'application_url',
    'company': 'employer_name',
    'city': 'city',
    'state': 'state',
    'country': 'country',
    'postalcode': 'postal_code',
    'remote': 'is_remote',
    'description': 'job_description',
    'jobtype': 'employment_type',
    'category': 'job_department',
    'website': 'website'
}


def _get_current_workable_file_name():
    current_date = datetime.datetime.now().date()
    return f'workable_{current_date}.xml'


# Only write the file once per day
# Workable limits the number of requests to this endpoint
def _write_workable_xml():
    current_file_name = _get_current_workable_file_name()
    current_workable_files = [f for f in listdir(os.getcwd()) if
                              isfile(join(os.getcwd(), f)) and re.match('^workable_.+?\.xml', f)]
    if current_file_name in current_workable_files:
        logger.info(f'Current workable file <{current_file_name}> already exists')
        return
    
    for f in current_workable_files:
        logger.info(f'Removing Workable file - {f}')
        os.remove(f)
    logger.info('Starting Workable request')
    workable_data = requests.get('https://www.workable.com/boards/workable.xml')
    logger.info('Response received from Workable')
    with open(current_file_name, 'w') as f:
        logger.info('Writing Workable file')
        f.write(workable_data.content.decode('utf-8'))


def parse_workable_xml_jobs():
    _write_workable_xml()
    tree = ET.parse(_get_current_workable_file_name())
    root = tree.getroot()
    employer_map = {e.employer_name: e for e in Employer.objects.all()}
    employer_parsers = {}
    employer_recent_scraped_urls = {}
    for idx, job in enumerate(root):
        # Memory size issues occur due to the large file size
        # Periodically dump data to keep memory within limits
        # if len(employer_parsers) == 20:
        #     employer_parsers = {}
        # if len(employer_recent_scraped_urls) == 20:
        #     employer_recent_scraped_urls = {}
        if job.tag != 'job':
            continue
        job_data = {}
        for job_attr in job:
            if norm_key := key_map.get(job_attr.tag):
                job_data[norm_key] = job_attr.text.strip() if job_attr.text else None
        
        if job_data['employer_name'] not in company_whitelist:
            continue
        
        job_data['employer_name'] = company_whitelist[job_data['employer_name']] or job_data['employer_name']
        
        job_data['city'] = [c.strip() for c in job_data['city'].split(',')][0]
        
        location = ', '.join(
            [x for x in [job_data['city'], job_data['state'], job_data['country'], job_data['postal_code']] if x])
        if job_data.get('remote'):
            location = f'Remote: {location}'
        description_compensation_data = parse_compensation_text(job_data['job_description'])
        
        if not (employer := employer_map.get(job_data['employer_name'])):
            employer = Employer(
                employer_name=job_data['employer_name'],
                is_use_job_url=True
            )
            employer.save()
            employer_map[employer.employer_name] = employer
        
        if not (recent_scraped_urls := employer_recent_scraped_urls.get(employer.employer_name)):
            recent_scraped_urls = get_recent_scraped_job_urls(employer.employer_name)
            employer_recent_scraped_urls[employer.employer_name] = recent_scraped_urls
        
        if job_data['application_url'] in recent_scraped_urls:
            logger.info(f'Skipping {job_data["employer_name"]} - {job_data["job_title"]}. Recently processed')
            continue
        
        job_item = JobItem(
            employer_name=job_data['employer_name'],
            application_url=job_data['application_url'],
            job_title=job_data['job_title'],
            locations=[location],
            job_department=job_data['job_department'],
            job_description=job_data['job_description'],
            employment_type=job_data['employment_type'],
            first_posted_date=get_datetime_format_or_none(
                get_datetime_or_none(job_data['first_posted_date'], as_date=True)),
            website_domain=re.sub('https?://(www)?', '', job_data['website']) if job_data['website'] else None,
            **description_compensation_data
        )
        if not (employer_parser := employer_parsers.get(job_item.employer_name)):
            employer_parser = ScrapedJobProcessor(employer)
            employer_parsers[job_item.employer_name] = employer_parser
        logger.info(f'Processing {job_data["employer_name"]} - {job_data["job_title"]}.')
        employer_parser.process_job(job_item)
    
    for employer_name, employer_parser in employer_parsers.items():
        employer_parser.finalize_data(employer_recent_scraped_urls[employer_name])


class VasionScraper(WorkableScraper):
    employer_name = 'Vasion'
    EMPLOYER_KEY = 'vasion'


class RoktScraper(WorkableScraper):
    employer_name = 'Rokt'
    EMPLOYER_KEY = 'rokt'


class OutdoorsyScraper(WorkableScraper):
    employer_name = 'Outdoorsy'
    EMPLOYER_KEY = 'outdoorsy'


class TetraScienceScraper(WorkableScraper):
    employer_name = 'TetraScience'
    EMPLOYER_KEY = 'tetrascience'


class AthleticGreensScraper(WorkableScraper):
    employer_name = 'Athletic Greens'
    EMPLOYER_KEY = 'athletic-greens-hiring'


class StellarCyberScraper(WorkableScraper):
    employer_name = 'Stellar Cyber'
    EMPLOYER_KEY = 'stellar-cyber'


class IoGlobalScraper(WorkableScraper):
    employer_name = 'IO Global'
    EMPLOYER_KEY = 'io-global'


class NuveiScraper(WorkableScraper):
    employer_name = 'Nuvei'
    EMPLOYER_KEY = 'nuvei'


class PaytrixScraper(WorkableScraper):
    employer_name = 'Paytrix'
    EMPLOYER_KEY = 'paytrix'


class ArchiproScraper(WorkableScraper):
    employer_name = 'ArchiPro'
    EMPLOYER_KEY = 'archipro-3'


class QuantexaScraper(WorkableScraper):
    employer_name = 'Quantexa'
    EMPLOYER_KEY = 'quantexa'


class HikeScraper(WorkableScraper):
    employer_name = 'Hike'
    EMPLOYER_KEY = 'hike'


class BitgetScraper(WorkableScraper):
    employer_name = 'Bitget'
    EMPLOYER_KEY = 'bitget'


class YapilyScraper(WorkableScraper):
    employer_name = 'Yapily'
    EMPLOYER_KEY = 'yapily'


class GohenryScraper(WorkableScraper):
    employer_name = 'GoHenry'
    EMPLOYER_KEY = 'gohenry'


class KeeperSecurityScraper(WorkableScraper):
    employer_name = 'Keeper Security'
    EMPLOYER_KEY = 'keepersecurity'


class StarlingBankScraper(WorkableScraper):
    employer_name = 'Starling Bank'
    EMPLOYER_KEY = 'starling-bank'


class GlorifyScraper(WorkableScraper):
    employer_name = 'Glorify'
    EMPLOYER_KEY = 'glorify'


class NuvemshopScraper(WorkableScraper):
    employer_name = 'Nuvemshop'
    EMPLOYER_KEY = 'tiendanube-nuvemshop'


class LetsDoThisScraper(WorkableScraper):
    employer_name = 'Let\'s Do This'
    EMPLOYER_KEY = 'lets-do-this'


class ZoneAndCoScraper(WorkableScraper):
    employer_name = 'Zone & Co'
    EMPLOYER_KEY = 'zoneandco'


class Cars24Scraper(WorkableScraper):
    employer_name = 'Cars24'
    EMPLOYER_KEY = 'cars24'


class NinefinScraper(WorkableScraper):
    employer_name = '9fin'
    EMPLOYER_KEY = '9fin'


class SinchScraper(WorkableScraper):
    employer_name = 'Sinch'
    EMPLOYER_KEY = 'sinch'


class QuintoandarScraper(WorkableScraper):
    employer_name = 'QuintoAndar'
    EMPLOYER_KEY = 'quintoandar'


class BuilderAiScraper(WorkableScraper):
    employer_name = 'Builder.ai'
    EMPLOYER_KEY = 'builderai'


class BlackbirdAiScraper(WorkableScraper):
    employer_name = 'Blackbird AI'
    EMPLOYER_KEY = 'blackbirdai'


class RelianceHealthScraper(WorkableScraper):
    employer_name = 'Reliance Health'
    EMPLOYER_KEY = 'get-reliance-health'


class EpignosisScraper(WorkableScraper):
    employer_name = 'Epignosis'
    EMPLOYER_KEY = 'epignosis'


class NeoFinancialScraper(WorkableScraper):
    employer_name = 'Neo Financial'
    EMPLOYER_KEY = 'neo-financial'


class SatispayScraper(WorkableScraper):
    employer_name = 'Satispay'
    EMPLOYER_KEY = 'satispay'


class MoladinScraper(WorkableScraper):
    employer_name = 'Moladin'
    EMPLOYER_KEY = 'moladin'


class MotorwayScraper(WorkableScraper):
    employer_name = 'Motorway'
    EMPLOYER_KEY = 'motorway'


class Akur8Scraper(WorkableScraper):
    employer_name = 'Akur8'
    EMPLOYER_KEY = 'akur8'


class SkeduloScraper(WorkableScraper):
    employer_name = 'Skedulo'
    EMPLOYER_KEY = 'skedulo'


class IdovenScraper(WorkableScraper):
    employer_name = 'Idoven'
    EMPLOYER_KEY = 'idoven'


class BlinkScraper(WorkableScraper):
    employer_name = 'Blink'
    EMPLOYER_KEY = 'blink'


class LightyearScraper(WorkableScraper):
    employer_name = 'Lightyear'
    EMPLOYER_KEY = 'lightyear'


class ResortpassScraper(WorkableScraper):
    employer_name = 'ResortPass'
    EMPLOYER_KEY = 'resortpass'


class BeamScraper(WorkableScraper):
    employer_name = 'Beam'
    EMPLOYER_KEY = 'beam'


class ApnaScraper(WorkableScraper):
    employer_name = 'Apna'
    EMPLOYER_KEY = 'apna'


class LingoaceScraper(WorkableScraper):
    employer_name = 'LingoAce'
    EMPLOYER_KEY = 'lingoace'


class FairmoneyScraper(WorkableScraper):
    employer_name = 'FairMoney'
    EMPLOYER_KEY = 'fairmoney'


class HexTrustScraper(WorkableScraper):
    employer_name = 'Hex Trust'
    EMPLOYER_KEY = 'hextrust'


class AmogyScraper(WorkableScraper):
    employer_name = 'Amogy'
    EMPLOYER_KEY = 'amogy'


class SemiosScraper(WorkableScraper):
    employer_name = 'Semios'
    EMPLOYER_KEY = 'semios'


class BoohooGroupScraper(WorkableScraper):
    employer_name = 'Boohoo Group'
    EMPLOYER_KEY = 'boohoogroup'


class ColdquantaScraper(WorkableScraper):
    employer_name = 'ColdQuanta'
    EMPLOYER_KEY = 'coldquanta'


class ExotecScraper(WorkableScraper):
    employer_name = 'Exotec'
    EMPLOYER_KEY = 'exotec'


class ProjectCanaryScraper(WorkableScraper):
    employer_name = 'Project Canary'
    EMPLOYER_KEY = 'projectcanary'


class PreferredNetworksScraper(WorkableScraper):
    employer_name = 'Preferred Networks'
    EMPLOYER_KEY = 'preferrednetworks'


class ClarityAiScraper(WorkableScraper):
    employer_name = 'Clarity AI'
    EMPLOYER_KEY = 'clarityai'


class SharegainScraper(WorkableScraper):
    employer_name = 'Sharegain'
    EMPLOYER_KEY = 'sharegain'


class ParoScraper(WorkableScraper):
    employer_name = 'Paro'
    EMPLOYER_KEY = 'paro'


class EvolvScraper(WorkableScraper):
    employer_name = 'Evolv'
    EMPLOYER_KEY = 'evolv'


class DroneupScraper(WorkableScraper):
    employer_name = 'DroneUp'
    EMPLOYER_KEY = 'droneup'


class EquitybeeScraper(WorkableScraper):
    employer_name = 'EquityBee'
    EMPLOYER_KEY = 'equitybee'


class BibitScraper(WorkableScraper):
    employer_name = 'Bibit'
    EMPLOYER_KEY = 'bibit'


class TiledbScraper(WorkableScraper):
    employer_name = 'TileDB'
    EMPLOYER_KEY = 'tiledb'


class GigsScraper(WorkableScraper):
    employer_name = 'Gigs'
    EMPLOYER_KEY = 'gigs'


class AxelarScraper(WorkableScraper):
    employer_name = 'Axelar'
    EMPLOYER_KEY = 'axelar'


class UniversalQuantumScraper(WorkableScraper):
    employer_name = 'Universal Quantum'
    EMPLOYER_KEY = 'universalquantum'


class ConstructorScraper(WorkableScraper):
    employer_name = 'Constructor'
    EMPLOYER_KEY = 'constructor'


class AllSpaceScraper(WorkableScraper):
    employer_name = 'All.Space'
    EMPLOYER_KEY = 'allspace'


class ZoomoScraper(WorkableScraper):
    employer_name = 'Zoomo'
    EMPLOYER_KEY = 'zoomo'


class PrecisionNeuroscienceScraper(WorkableScraper):
    employer_name = 'Precision Neuroscience'
    EMPLOYER_KEY = 'precisionneuroscience'


class MoneyFellowsScraper(WorkableScraper):
    employer_name = 'Money Fellows'
    EMPLOYER_KEY = 'moneyfellows'


class Shift4Scraper(WorkableScraper):
    employer_name = 'Shift4'
    EMPLOYER_KEY = 'shift4'


class PersadoScraper(WorkableScraper):
    employer_name = 'Persado'
    EMPLOYER_KEY = 'persado'


class IesoScraper(WorkableScraper):
    employer_name = 'Ieso'
    EMPLOYER_KEY = 'ieso'


class InsiteScraper(WorkableScraper):
    employer_name = 'Insite'
    EMPLOYER_KEY = 'insite'


class ProphecyScraper(WorkableScraper):
    employer_name = 'Prophecy'
    EMPLOYER_KEY = 'prophecy'


class EmploymentHeroScraper(WorkableScraper):
    employer_name = 'Employment Hero'
    EMPLOYER_KEY = 'employmenthero'


class AldrinScraper(WorkableScraper):
    employer_name = 'Aldrin'
    EMPLOYER_KEY = 'aldrin'


class WorkableCoScraper(WorkableScraper):
    employer_name = 'Workable'
    EMPLOYER_KEY = 'workable'


class KudaScraper(WorkableScraper):
    employer_name = 'Kuda'
    EMPLOYER_KEY = 'kuda'


class FortanixScraper(WorkableScraper):
    employer_name = 'Fortanix'
    EMPLOYER_KEY = 'fortanix'


class FoodicsScraper(WorkableScraper):
    employer_name = 'Foodics'
    EMPLOYER_KEY = 'foodics'


class QuizizzScraper(WorkableScraper):
    employer_name = 'Quizizz'
    EMPLOYER_KEY = 'quizizz'


class TavusScraper(WorkableScraper):
    employer_name = 'Tavus'
    EMPLOYER_KEY = 'tavus'


class LightmatterScraper(WorkableScraper):
    employer_name = 'Lightmatter'
    EMPLOYER_KEY = 'lightmatter'


class IntuitionMachinesScraper(WorkableScraper):
    employer_name = 'Intuition Machines'
    EMPLOYER_KEY = 'intuitionmachines'


class TenXScraper(WorkableScraper):
    employer_name = '10x'
    EMPLOYER_KEY = '10x'


class ProxymityScraper(WorkableScraper):
    employer_name = 'Proxymity'
    EMPLOYER_KEY = 'proxymity'


class AjaibScraper(WorkableScraper):
    employer_name = 'Ajaib'
    EMPLOYER_KEY = 'ajaib'


class HeartexScraper(WorkableScraper):
    employer_name = 'Heartex'
    EMPLOYER_KEY = 'heartex'


class SkyMavisScraper(WorkableScraper):
    employer_name = 'Sky Mavis'
    EMPLOYER_KEY = 'skymavis'


class ClerkScraper(WorkableScraper):
    employer_name = 'Clerk'
    EMPLOYER_KEY = 'clerk'


class EntainScraper(WorkableScraper):
    employer_name = 'Entain'
    EMPLOYER_KEY = 'entain'


class SpatialScraper(WorkableScraper):
    employer_name = 'Spatial'
    EMPLOYER_KEY = 'spatial'


class IceyeScraper(WorkableScraper):
    employer_name = 'ICEYE'
    EMPLOYER_KEY = 'iceye'


class CarbyneScraper(WorkableScraper):
    employer_name = 'Carbyne'
    EMPLOYER_KEY = 'carbyne'


class IslandScraper(WorkableScraper):
    employer_name = 'Island'
    EMPLOYER_KEY = 'island'


class TresataScraper(WorkableScraper):
    employer_name = 'Tresata'
    EMPLOYER_KEY = 'tresata'


class StakefishScraper(WorkableScraper):
    employer_name = 'stakefish'
    EMPLOYER_KEY = 'stakefish'


class EleosHealthScraper(WorkableScraper):
    employer_name = 'Eleos Health'
    EMPLOYER_KEY = 'eleoshealth'


class PerceptyxScraper(WorkableScraper):
    employer_name = 'Perceptyx'
    EMPLOYER_KEY = 'perceptyx'


class BetterhelpScraper(WorkableScraper):
    employer_name = 'BetterHelp'
    EMPLOYER_KEY = 'betterhelp'


class ReversinglabsScraper(WorkableScraper):
    employer_name = 'ReversingLabs'
    EMPLOYER_KEY = 'reversinglabs'


class OxboticaScraper(WorkableScraper):
    employer_name = 'Oxbotica'
    EMPLOYER_KEY = 'oxbotica'


class InspectorioScraper(WorkableScraper):
    employer_name = 'Inspectorio'
    EMPLOYER_KEY = 'inspectorio'


class LearnworldsScraper(WorkableScraper):
    employer_name = 'LearnWorlds'
    EMPLOYER_KEY = 'learnworlds'


class ProducepayScraper(WorkableScraper):
    employer_name = 'ProducePay'
    EMPLOYER_KEY = 'producepay'


class FreelancerComScraper(WorkableScraper):
    employer_name = 'Freelancer.com'
    EMPLOYER_KEY = 'freelancercom'


class ElvieScraper(WorkableScraper):
    employer_name = 'Elvie'
    EMPLOYER_KEY = 'elvie'


class SmartScraper(WorkableScraper):
    employer_name = 'Smart'
    EMPLOYER_KEY = 'smart'


class SquareEnixScraper(WorkableScraper):
    employer_name = 'Square Enix'
    EMPLOYER_KEY = 'squareenix'


class SpenmoScraper(WorkableScraper):
    employer_name = 'Spenmo'
    EMPLOYER_KEY = 'spenmo'


class FinexioScraper(WorkableScraper):
    employer_name = 'Finexio'
    EMPLOYER_KEY = 'finexio'


class EntropikScraper(WorkableScraper):
    employer_name = 'Entropik'
    EMPLOYER_KEY = 'entropik'


class BitstampScraper(WorkableScraper):
    employer_name = 'Bitstamp'
    EMPLOYER_KEY = 'bitstamp'


class FundamentalvrScraper(WorkableScraper):
    employer_name = 'FundamentalVR'
    EMPLOYER_KEY = 'fundamentalvr'


class PerlegoScraper(WorkableScraper):
    employer_name = 'Perlego'
    EMPLOYER_KEY = 'perlego'


class KrooScraper(WorkableScraper):
    employer_name = 'Kroo'
    EMPLOYER_KEY = 'kroo'


class TransfermateScraper(WorkableScraper):
    employer_name = 'TransferMate'
    EMPLOYER_KEY = 'transfermate'


class SirionlabsScraper(WorkableScraper):
    employer_name = 'SirionLabs'
    EMPLOYER_KEY = 'sirionlabs'


class MeasurablScraper(WorkableScraper):
    employer_name = 'Measurabl'
    EMPLOYER_KEY = 'measurabl'


class OxfordQuantumScraper(WorkableScraper):
    employer_name = 'Oxford Quantum'
    EMPLOYER_KEY = 'oxfordquantum'


class MedwingScraper(WorkableScraper):
    employer_name = 'Medwing'
    EMPLOYER_KEY = 'medwing'


class HackTheBoxScraper(WorkableScraper):
    employer_name = 'Hack the Box'
    EMPLOYER_KEY = 'hackthebox'


class TadoScraper(WorkableScraper):
    employer_name = 'Tado'
    EMPLOYER_KEY = 'tado'


class SharesScraper(WorkableScraper):
    employer_name = 'Shares'
    EMPLOYER_KEY = 'shares'


class EterlastScraper(WorkableScraper):
    employer_name = 'Eterlast'
    EMPLOYER_KEY = 'eterlast'


class VerticeScraper(WorkableScraper):
    employer_name = 'Vertice'
    EMPLOYER_KEY = 'vertice'


class Carry1stScraper(WorkableScraper):
    employer_name = 'Carry1st'
    EMPLOYER_KEY = 'carry1st'


class SaryScraper(WorkableScraper):
    employer_name = 'Sary'
    EMPLOYER_KEY = 'sary'


class AvantstayScraper(WorkableScraper):
    employer_name = 'AvantStay'
    EMPLOYER_KEY = 'avantstay'


class LeetcodeScraper(WorkableScraper):
    employer_name = 'Leetcode'
    EMPLOYER_KEY = 'leetcode'


class DiveplaneScraper(WorkableScraper):
    employer_name = 'Diveplane'
    EMPLOYER_KEY = 'diveplane'


class HydrosatScraper(WorkableScraper):
    employer_name = 'Hydrosat'
    EMPLOYER_KEY = 'hydrosat'


class DextScraper(WorkableScraper):
    employer_name = 'Dext'
    EMPLOYER_KEY = 'dext'


class SignalAiScraper(WorkableScraper):
    employer_name = 'Signal AI'
    EMPLOYER_KEY = 'signalai'


class OmetriaScraper(WorkableScraper):
    employer_name = 'Ometria'
    EMPLOYER_KEY = 'ometria'


class N8nScraper(WorkableScraper):
    employer_name = 'n8n'
    EMPLOYER_KEY = 'n8n'


class ClubrareScraper(WorkableScraper):
    employer_name = 'ClubRare'
    EMPLOYER_KEY = 'clubrare'


class RisingwaveLabsScraper(WorkableScraper):
    employer_name = 'RisingWave Labs'
    EMPLOYER_KEY = 'risingwavelabs'


class NearScraper(WorkableScraper):
    employer_name = 'Near'
    EMPLOYER_KEY = 'near'


class LoggiScraper(WorkableScraper):
    employer_name = 'Loggi'
    EMPLOYER_KEY = 'loggi'


class NillionScraper(WorkableScraper):
    employer_name = 'Nillion'
    EMPLOYER_KEY = 'nillion'


class SuperfluidScraper(WorkableScraper):
    employer_name = 'Superfluid'
    EMPLOYER_KEY = 'superfluid'


class OnomondoScraper(WorkableScraper):
    employer_name = 'Onomondo'
    EMPLOYER_KEY = 'onomondo'


class MinaFoundationScraper(WorkableScraper):
    employer_name = 'Mina Foundation'
    EMPLOYER_KEY = 'minafoundation'


class BooksyScraper(WorkableScraper):
    employer_name = 'Booksy'
    EMPLOYER_KEY = 'booksy'


class DawnAerospaceScraper(WorkableScraper):
    employer_name = 'Dawn Aerospace'
    EMPLOYER_KEY = 'dawnaerospace'


class FreshaScraper(WorkableScraper):
    employer_name = 'Fresha'
    EMPLOYER_KEY = 'fresha'


class NovataScraper(WorkableScraper):
    employer_name = 'Novata'
    EMPLOYER_KEY = 'novata'


class SenseonScraper(WorkableScraper):
    employer_name = 'SenseOn'
    EMPLOYER_KEY = 'senseon'


class EllipticScraper(WorkableScraper):
    employer_name = 'Elliptic'
    EMPLOYER_KEY = 'elliptic'


class FlorenceHealthScraper(WorkableScraper):
    employer_name = 'Florence Health'
    EMPLOYER_KEY = 'florencehealth'


class EveryrealmScraper(WorkableScraper):
    employer_name = 'Everyrealm'
    EMPLOYER_KEY = 'everyrealm'


class PerfectStormScraper(WorkableScraper):
    employer_name = 'Perfect Storm'
    EMPLOYER_KEY = 'perfectstorm'


class MagicSpoonScraper(WorkableScraper):
    employer_name = 'Magic Spoon'
    EMPLOYER_KEY = 'magicspoon'


class N3tworkScraper(WorkableScraper):
    employer_name = 'N3TWORK'
    EMPLOYER_KEY = 'n3twork'


class PlumScraper(WorkableScraper):
    employer_name = 'Plum'
    EMPLOYER_KEY = 'plum'


class LandaScraper(WorkableScraper):
    employer_name = 'Landa'
    EMPLOYER_KEY = 'landa'


class InteractiveInvestorScraper(WorkableScraper):
    employer_name = 'interactive investor'
    EMPLOYER_KEY = 'interactiveinvestor'


class UkioScraper(WorkableScraper):
    employer_name = 'Ukio'
    EMPLOYER_KEY = 'ukio'


class ArcScraper(WorkableScraper):
    employer_name = 'Arc'
    EMPLOYER_KEY = 'arc'


class TesseractScraper(WorkableScraper):
    employer_name = 'Tesseract'
    EMPLOYER_KEY = 'tesseract'


class XploreScraper(WorkableScraper):
    employer_name = 'Xplore'
    EMPLOYER_KEY = 'xplore'


class OuraScraper(WorkableScraper):
    employer_name = 'Oura'
    EMPLOYER_KEY = 'oura'


class GourmeyScraper(WorkableScraper):
    employer_name = 'Gourmey'
    EMPLOYER_KEY = 'gourmey'


class VividMoneyScraper(WorkableScraper):
    employer_name = 'Vivid Money'
    EMPLOYER_KEY = 'vividmoney'


class MarleySpoonScraper(WorkableScraper):
    employer_name = 'Marley Spoon'
    EMPLOYER_KEY = 'marleyspoon'


class NmiScraper(WorkableScraper):
    employer_name = 'NMI'
    EMPLOYER_KEY = 'nmi'


class CodiScraper(WorkableScraper):
    employer_name = 'Codi'
    EMPLOYER_KEY = 'codi'


class AliceAndBobScraper(WorkableScraper):
    employer_name = 'Alice&Bob'
    EMPLOYER_KEY = 'alicebob'
    
    
class LeenaAiScraper(WorkableScraper):
    employer_name = 'Leena AI'
    EMPLOYER_KEY = 'leenaai'
    
    
class ScreencastifyScraper(WorkableScraper):
    employer_name = 'Screencastify'
    EMPLOYER_KEY = 'screencastify'
    
    
class WowzaScraper(WorkableScraper):
    employer_name = 'Wowza Media Systems'
    EMPLOYER_KEY = 'wowza-media-systems'


workable_scrapers = {
    ScreencastifyScraper.employer_name: ScreencastifyScraper,
    AliceAndBobScraper.employer_name: AliceAndBobScraper,
    CodiScraper.employer_name: CodiScraper,
    MarleySpoonScraper.employer_name: MarleySpoonScraper,
    NmiScraper.employer_name: NmiScraper,
    VividMoneyScraper.employer_name: VividMoneyScraper,
    GourmeyScraper.employer_name: GourmeyScraper,
    OuraScraper.employer_name: OuraScraper,
    XploreScraper.employer_name: XploreScraper,
    TesseractScraper.employer_name: TesseractScraper,
    ArcScraper.employer_name: ArcScraper,
    UkioScraper.employer_name: UkioScraper,
    InteractiveInvestorScraper.employer_name: InteractiveInvestorScraper,
    LandaScraper.employer_name: LandaScraper,
    PlumScraper.employer_name: PlumScraper,
    N3tworkScraper.employer_name: N3tworkScraper,
    MagicSpoonScraper.employer_name: MagicSpoonScraper,
    PerfectStormScraper.employer_name: PerfectStormScraper,
    EveryrealmScraper.employer_name: EveryrealmScraper,
    FlorenceHealthScraper.employer_name: FlorenceHealthScraper,
    EllipticScraper.employer_name: EllipticScraper,
    SenseonScraper.employer_name: SenseonScraper,
    NovataScraper.employer_name: NovataScraper,
    FreshaScraper.employer_name: FreshaScraper,
    DawnAerospaceScraper.employer_name: DawnAerospaceScraper,
    MinaFoundationScraper.employer_name: MinaFoundationScraper,
    BooksyScraper.employer_name: BooksyScraper,
    OnomondoScraper.employer_name: OnomondoScraper,
    SuperfluidScraper.employer_name: SuperfluidScraper,
    NillionScraper.employer_name: NillionScraper,
    LoggiScraper.employer_name: LoggiScraper,
    NearScraper.employer_name: NearScraper,
    RisingwaveLabsScraper.employer_name: RisingwaveLabsScraper,
    ClubrareScraper.employer_name: ClubrareScraper,
    N8nScraper.employer_name: N8nScraper,
    OmetriaScraper.employer_name: OmetriaScraper,
    SignalAiScraper.employer_name: SignalAiScraper,
    DextScraper.employer_name: DextScraper,
    HydrosatScraper.employer_name: HydrosatScraper,
    DiveplaneScraper.employer_name: DiveplaneScraper,
    LeetcodeScraper.employer_name: LeetcodeScraper,
    AvantstayScraper.employer_name: AvantstayScraper,
    SaryScraper.employer_name: SaryScraper,
    Carry1stScraper.employer_name: Carry1stScraper,
    EterlastScraper.employer_name: EterlastScraper,
    VerticeScraper.employer_name: VerticeScraper,
    SharesScraper.employer_name: SharesScraper,
    TadoScraper.employer_name: TadoScraper,
    HackTheBoxScraper.employer_name: HackTheBoxScraper,
    MedwingScraper.employer_name: MedwingScraper,
    OxfordQuantumScraper.employer_name: OxfordQuantumScraper,
    MeasurablScraper.employer_name: MeasurablScraper,
    SirionlabsScraper.employer_name: SirionlabsScraper,
    TransfermateScraper.employer_name: TransfermateScraper,
    KrooScraper.employer_name: KrooScraper,
    PerlegoScraper.employer_name: PerlegoScraper,
    FundamentalvrScraper.employer_name: FundamentalvrScraper,
    BitstampScraper.employer_name: BitstampScraper,
    EntropikScraper.employer_name: EntropikScraper,
    FinexioScraper.employer_name: FinexioScraper,
    SpenmoScraper.employer_name: SpenmoScraper,
    SquareEnixScraper.employer_name: SquareEnixScraper,
    SmartScraper.employer_name: SmartScraper,
    ElvieScraper.employer_name: ElvieScraper,
    FreelancerComScraper.employer_name: FreelancerComScraper,
    ProducepayScraper.employer_name: ProducepayScraper,
    LearnworldsScraper.employer_name: LearnworldsScraper,
    InspectorioScraper.employer_name: InspectorioScraper,
    OxboticaScraper.employer_name: OxboticaScraper,
    ReversinglabsScraper.employer_name: ReversinglabsScraper,
    BetterhelpScraper.employer_name: BetterhelpScraper,
    EleosHealthScraper.employer_name: EleosHealthScraper,
    PerceptyxScraper.employer_name: PerceptyxScraper,
    StakefishScraper.employer_name: StakefishScraper,
    CarbyneScraper.employer_name: CarbyneScraper,
    IslandScraper.employer_name: IslandScraper,
    TresataScraper.employer_name: TresataScraper,
    IceyeScraper.employer_name: IceyeScraper,
    SpatialScraper.employer_name: SpatialScraper,
    EntainScraper.employer_name: EntainScraper,
    ClerkScraper.employer_name: ClerkScraper,
    SkyMavisScraper.employer_name: SkyMavisScraper,
    HeartexScraper.employer_name: HeartexScraper,
    AjaibScraper.employer_name: AjaibScraper,
    ProxymityScraper.employer_name: ProxymityScraper,
    TenXScraper.employer_name: TenXScraper,
    LightmatterScraper.employer_name: LightmatterScraper,
    IntuitionMachinesScraper.employer_name: IntuitionMachinesScraper,
    TavusScraper.employer_name: TavusScraper,
    QuizizzScraper.employer_name: QuizizzScraper,
    FoodicsScraper.employer_name: FoodicsScraper,
    FortanixScraper.employer_name: FortanixScraper,
    KudaScraper.employer_name: KudaScraper,
    WorkableCoScraper.employer_name: WorkableCoScraper,
    AldrinScraper.employer_name: AldrinScraper,
    EmploymentHeroScraper.employer_name: EmploymentHeroScraper,
    ProphecyScraper.employer_name: ProphecyScraper,
    InsiteScraper.employer_name: InsiteScraper,
    IesoScraper.employer_name: IesoScraper,
    PersadoScraper.employer_name: PersadoScraper,
    Shift4Scraper.employer_name: Shift4Scraper,
    MoneyFellowsScraper.employer_name: MoneyFellowsScraper,
    PrecisionNeuroscienceScraper.employer_name: PrecisionNeuroscienceScraper,
    ZoomoScraper.employer_name: ZoomoScraper,
    AllSpaceScraper.employer_name: AllSpaceScraper,
    ConstructorScraper.employer_name: ConstructorScraper,
    UniversalQuantumScraper.employer_name: UniversalQuantumScraper,
    AxelarScraper.employer_name: AxelarScraper,
    GigsScraper.employer_name: GigsScraper,
    TiledbScraper.employer_name: TiledbScraper,
    BibitScraper.employer_name: BibitScraper,
    EquitybeeScraper.employer_name: EquitybeeScraper,
    DroneupScraper.employer_name: DroneupScraper,
    EvolvScraper.employer_name: EvolvScraper,
    ParoScraper.employer_name: ParoScraper,
    SharegainScraper.employer_name: SharegainScraper,
    ClarityAiScraper.employer_name: ClarityAiScraper,
    PreferredNetworksScraper.employer_name: PreferredNetworksScraper,
    ProjectCanaryScraper.employer_name: ProjectCanaryScraper,
    ExotecScraper.employer_name: ExotecScraper,
    ColdquantaScraper.employer_name: ColdquantaScraper,
    BoohooGroupScraper.employer_name: BoohooGroupScraper,
    SemiosScraper.employer_name: SemiosScraper,
    AmogyScraper.employer_name: AmogyScraper,
    HexTrustScraper.employer_name: HexTrustScraper,
    FairmoneyScraper.employer_name: FairmoneyScraper,
    LingoaceScraper.employer_name: LingoaceScraper,
    ApnaScraper.employer_name: ApnaScraper,
    BeamScraper.employer_name: BeamScraper,
    ResortpassScraper.employer_name: ResortpassScraper,
    LightyearScraper.employer_name: LightyearScraper,
    BlinkScraper.employer_name: BlinkScraper,
    IdovenScraper.employer_name: IdovenScraper,
    SkeduloScraper.employer_name: SkeduloScraper,
    Akur8Scraper.employer_name: Akur8Scraper,
    MotorwayScraper.employer_name: MotorwayScraper,
    MoladinScraper.employer_name: MoladinScraper,
    RelianceHealthScraper.employer_name: RelianceHealthScraper,
    NeoFinancialScraper.employer_name: NeoFinancialScraper,
    SatispayScraper.employer_name: SatispayScraper,
    EpignosisScraper.employer_name: EpignosisScraper,
    BlackbirdAiScraper.employer_name: BlackbirdAiScraper,
    BuilderAiScraper.employer_name: BuilderAiScraper,
    SinchScraper.employer_name: SinchScraper,
    QuintoandarScraper.employer_name: QuintoandarScraper,
    NinefinScraper.employer_name: NinefinScraper,
    ZoneAndCoScraper.employer_name: ZoneAndCoScraper,
    Cars24Scraper.employer_name: Cars24Scraper,
    LetsDoThisScraper.employer_name: LetsDoThisScraper,
    StarlingBankScraper.employer_name: StarlingBankScraper,
    NuvemshopScraper.employer_name: NuvemshopScraper,
    GlorifyScraper.employer_name: GlorifyScraper,
    KeeperSecurityScraper.employer_name: KeeperSecurityScraper,
    GohenryScraper.employer_name: GohenryScraper,
    YapilyScraper.employer_name: YapilyScraper,
    BitgetScraper.employer_name: BitgetScraper,
    HikeScraper.employer_name: HikeScraper,
    QuantexaScraper.employer_name: QuantexaScraper,
    ArchiproScraper.employer_name: ArchiproScraper,
    PaytrixScraper.employer_name: PaytrixScraper,
    NuveiScraper.employer_name: NuveiScraper,
    IoGlobalScraper.employer_name: IoGlobalScraper,
    AthleticGreensScraper.employer_name: AthleticGreensScraper,
    StellarCyberScraper.employer_name: StellarCyberScraper,
    TetraScienceScraper.employer_name: TetraScienceScraper,
    OutdoorsyScraper.employer_name: OutdoorsyScraper,
    RoktScraper.employer_name: RoktScraper,
    VasionScraper.employer_name: VasionScraper,
}
