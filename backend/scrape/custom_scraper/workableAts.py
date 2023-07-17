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
from scrape.job_processor import JobItem, JobProcessor

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
            employer_parser = JobProcessor(employer)
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


workable_scrapers = {
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
