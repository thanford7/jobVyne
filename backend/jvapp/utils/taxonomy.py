# https://docs.google.com/spreadsheets/d/1G5-9y6bp0QHjZmxIWmGtjI6F_AbuqfHmYYFmQC6p_UU/edit#gid=0
import logging
import re
from collections import namedtuple

from django.db.models import Count, Prefetch, Q, Subquery
from django.db.transaction import atomic
from django.utils import timezone

from jvapp.models.employer import EmployerJob, JobTaxonomy, Taxonomy

logger = logging.getLogger(__name__)

TAXONOMY_PROFESSION_EA = 'ea'  # None
TAXONOMY_PROFESSION_COS = 'cos'  # None
TAXONOMY_PROFESSION_LAW = 'law'  # x
TAXONOMY_PROFESSION_GOV = 'gov'  # x
TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT = 'product-management'  # x
TAXONOMY_PROFESSION_PRODUCT_ENGINEERING = 'product-engineer'  # x
TAXONOMY_PROFESSION_PRODUCT_MARKETING = 'product-marketing'  # x
TAXONOMY_PROFESSION_CUSTOMER_SUCCESS = 'customer-success'  # x
TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT = 'account-management'  # x
TAXONOMY_PROFESSION_CLIENT_SOLUTIONS = 'client-solutions'  # x
TAXONOMY_PROFESSION_CUSTOMER_SUPPORT = 'customer-support'  # x
TAXONOMY_PROFESSION_HR = 'hr'  # x
TAXONOMY_PROFESSION_TA = 'ta'  # x
TAXONOMY_PROFESSION_ENG_HARDWARE = 'eng-hardware'
TAXONOMY_PROFESSION_ENG_SOFTWARE = 'eng-software'  # x
TAXONOMY_PROFESSION_ENG_FRONTEND = 'eng-frontend'  # x
TAXONOMY_PROFESSION_ENG_BACKEND = 'eng-backend'  # x
TAXONOMY_PROFESSION_ENG_MOBILE = 'eng-mobile'  # x
TAXONOMY_PROFESSION_DEVOPS = 'devops'  # x
TAXONOMY_PROFESSION_QA = 'qa'  # x
TAXONOMY_PROFESSION_IT = 'it'  # x
TAXONOMY_PROFESSION_DATA_ANALYSIS = 'data-analysis'  # x
TAXONOMY_PROFESSION_DATA_SCIENCE = 'data-science'  # x
TAXONOMY_PROFESSION_ML = 'ml'  # x
TAXONOMY_PROFESSION_ENG_DATA = 'eng-data'  # x
TAXONOMY_PROFESSION_DBA = 'dba'  # x
TAXONOMY_PROFESSION_SDR = 'sdr'  # x
TAXONOMY_PROFESSION_SALES = 'sales'  # x
TAXONOMY_PROFESSION_BUS_DEV = 'bus-dev'  # x
TAXONOMY_PROFESSION_MARKETING = 'marketing'  # x
TAXONOMY_PROFESSION_MARKETING_GROWTH = 'marketing-growth'  # x
TAXONOMY_PROFESSION_MARKETING_DIGITAL = 'marketing-digital'  # x
TAXONOMY_PROFESSION_MARKETING_SEO = 'marketing-seo'  # x
TAXONOMY_PROFESSION_MARKETING_EVENTS = 'marketing-events'  # x
TAXONOMY_PROFESSION_PR = 'pr'  # x
TAXONOMY_PROFESSION_MARKETING_RESEARCH = 'marketing-research'  # x
TAXONOMY_PROFESSION_UI = 'ui'  # x
TAXONOMY_PROFESSION_PRODUCT_DESIGN = 'product-design'  # x
TAXONOMY_PROFESSION_PROJECT_MANAGEMENT = 'project-management'  # x
TAXONOMY_PROFESSION_BUSINESS_ANALYSIS = 'business-analysis'  # x
TAXONOMY_PROFESSION_STRATEGY_OPS = 'strategy-ops'  # x
TAXONOMY_PROFESSION_GROWTH = 'growth'  # x
TAXONOMY_PROFESSION_FINANCE = 'finance'
TAXONOMY_PROFESSION_ACCOUNTING = 'accounting'

JOB_PROFESSIONS = [
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Executive Assistant', key=TAXONOMY_PROFESSION_EA),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Chief of Staff', key=TAXONOMY_PROFESSION_COS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Law', key=TAXONOMY_PROFESSION_LAW),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Government & Regulation', key=TAXONOMY_PROFESSION_GOV),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Product Management',
             key=TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Product Engineering',
             key=TAXONOMY_PROFESSION_PRODUCT_ENGINEERING),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Product Marketing',
             key=TAXONOMY_PROFESSION_PRODUCT_MARKETING),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Customer Success', key=TAXONOMY_PROFESSION_CUSTOMER_SUCCESS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Account Management',
             key=TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Client Solutions', key=TAXONOMY_PROFESSION_CLIENT_SOLUTIONS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Customer Support', key=TAXONOMY_PROFESSION_CUSTOMER_SUPPORT),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Human Resources', key=TAXONOMY_PROFESSION_HR),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Talent Acquisition', key=TAXONOMY_PROFESSION_TA),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Hardware Engineering', key=TAXONOMY_PROFESSION_ENG_HARDWARE),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Software Engineering', key=TAXONOMY_PROFESSION_ENG_SOFTWARE),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Front-End Development', key=TAXONOMY_PROFESSION_ENG_FRONTEND),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Back-End Development', key=TAXONOMY_PROFESSION_ENG_BACKEND),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Mobile Development', key=TAXONOMY_PROFESSION_ENG_MOBILE),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Devops Engineering', key=TAXONOMY_PROFESSION_DEVOPS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='QA Engineering', key=TAXONOMY_PROFESSION_QA),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='IT (Non-Engineering)', key=TAXONOMY_PROFESSION_IT),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Data Analysis', key=TAXONOMY_PROFESSION_DATA_ANALYSIS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Data Science', key=TAXONOMY_PROFESSION_DATA_SCIENCE),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Machine Learning / AI Engineering',
             key=TAXONOMY_PROFESSION_ML),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Data Engineering', key=TAXONOMY_PROFESSION_ENG_DATA),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Database Administration', key=TAXONOMY_PROFESSION_DBA),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='SDR / BDR', key=TAXONOMY_PROFESSION_SDR),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Sales Executive', key=TAXONOMY_PROFESSION_SALES),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Business/Corporate Development',
             key=TAXONOMY_PROFESSION_BUS_DEV),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Marketing', key=TAXONOMY_PROFESSION_MARKETING),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Growth Marketing', key=TAXONOMY_PROFESSION_MARKETING_GROWTH),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Digital Marketing',
             key=TAXONOMY_PROFESSION_MARKETING_DIGITAL),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='SEO', key=TAXONOMY_PROFESSION_MARKETING_SEO),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Event Marketing', key=TAXONOMY_PROFESSION_MARKETING_EVENTS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Public Relations', key=TAXONOMY_PROFESSION_PR),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Market Research', key=TAXONOMY_PROFESSION_MARKETING_RESEARCH),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='UI/UX', key=TAXONOMY_PROFESSION_UI),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Product Design', key=TAXONOMY_PROFESSION_PRODUCT_DESIGN),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Project Management',
             key=TAXONOMY_PROFESSION_PROJECT_MANAGEMENT),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Business Analysis',
             key=TAXONOMY_PROFESSION_BUSINESS_ANALYSIS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Strategy & Operations', key=TAXONOMY_PROFESSION_STRATEGY_OPS),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Growth', key=TAXONOMY_PROFESSION_GROWTH),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Finance', key=TAXONOMY_PROFESSION_FINANCE),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Accounting', key=TAXONOMY_PROFESSION_ACCOUNTING)
]

TAXONOMY_PROFESSION_LEGAL_CAT_REGULATORY = 'legal-reg'
TAXONOMY_PROFESSION_CAT_PRODUCT = 'product'
TAXONOMY_PROFESSION_CAT_CUSTOMER = 'customer'
TAXONOMY_PROFESSION_CAT_SALES = 'all-sales'
TAXONOMY_PROFESSION_CAT_HR_TA = 'hr-ta'
TAXONOMY_PROFESSION_CAT_SOFTWARE_ENGINEERING = 'all-software'
TAXONOMY_PROFESSION_CAT_IT_QA = 'all-it'
TAXONOMY_PROFESSION_CAT_DATA = 'data'
TAXONOMY_PROFESSION_CAT_MARKETING = 'all-marketing'
TAXONOMY_PROFESSION_CAT_DESIGN = 'design'
TAXONOMY_PROFESSION_CAT_BUS_STRAT = 'bus-strat'
TAXONOMY_PROFESSION_CAT_FIN_ACCT = 'fin-acct'

JOB_PROFESSION_CATEGORIES = [
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Legal & Regulatory',
                 key=TAXONOMY_PROFESSION_LEGAL_CAT_REGULATORY),
        [TAXONOMY_PROFESSION_LAW, TAXONOMY_PROFESSION_GOV]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Product', key=TAXONOMY_PROFESSION_CAT_PRODUCT),
        [TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT, TAXONOMY_PROFESSION_PRODUCT_DESIGN,
         TAXONOMY_PROFESSION_PRODUCT_ENGINEERING, TAXONOMY_PROFESSION_PRODUCT_MARKETING]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Customer Focus',
                 key=TAXONOMY_PROFESSION_CAT_CUSTOMER),
        [TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, TAXONOMY_PROFESSION_CUSTOMER_SUCCESS,
         TAXONOMY_PROFESSION_CUSTOMER_SUPPORT, TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Sales (Pre & Post)',
                 key=TAXONOMY_PROFESSION_CAT_SALES),
        [TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT, TAXONOMY_PROFESSION_SALES, TAXONOMY_PROFESSION_CUSTOMER_SUCCESS,
         TAXONOMY_PROFESSION_SDR, TAXONOMY_PROFESSION_BUS_DEV, TAXONOMY_PROFESSION_GROWTH]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='HR & TA',
                 key=TAXONOMY_PROFESSION_CAT_HR_TA),
        [TAXONOMY_PROFESSION_HR, TAXONOMY_PROFESSION_TA]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='All Software Engineering',
                 key=TAXONOMY_PROFESSION_CAT_SOFTWARE_ENGINEERING),
        [TAXONOMY_PROFESSION_ENG_SOFTWARE, TAXONOMY_PROFESSION_ENG_FRONTEND, TAXONOMY_PROFESSION_ENG_BACKEND,
         TAXONOMY_PROFESSION_ENG_MOBILE, TAXONOMY_PROFESSION_ENG_DATA, TAXONOMY_PROFESSION_DEVOPS,
         TAXONOMY_PROFESSION_ML, TAXONOMY_PROFESSION_DATA_SCIENCE]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='IT & QA',
                 key=TAXONOMY_PROFESSION_CAT_IT_QA),
        [TAXONOMY_PROFESSION_IT, TAXONOMY_PROFESSION_QA]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Data',
                 key=TAXONOMY_PROFESSION_CAT_DATA),
        [TAXONOMY_PROFESSION_DATA_SCIENCE, TAXONOMY_PROFESSION_ENG_DATA, TAXONOMY_PROFESSION_DATA_ANALYSIS,
         TAXONOMY_PROFESSION_DBA]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='All Marketing',
                 key=TAXONOMY_PROFESSION_CAT_MARKETING),
        [TAXONOMY_PROFESSION_MARKETING_GROWTH, TAXONOMY_PROFESSION_MARKETING_DIGITAL,
         TAXONOMY_PROFESSION_PRODUCT_MARKETING, TAXONOMY_PROFESSION_MARKETING_EVENTS, TAXONOMY_PROFESSION_MARKETING,
         TAXONOMY_PROFESSION_MARKETING_SEO, TAXONOMY_PROFESSION_MARKETING_RESEARCH, TAXONOMY_PROFESSION_GROWTH, TAXONOMY_PROFESSION_PR]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Design',
                 key=TAXONOMY_PROFESSION_CAT_DESIGN),
        [TAXONOMY_PROFESSION_UI, TAXONOMY_PROFESSION_PRODUCT_DESIGN]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Business & Strategy',
                 key=TAXONOMY_PROFESSION_CAT_BUS_STRAT),
        [TAXONOMY_PROFESSION_BUSINESS_ANALYSIS, TAXONOMY_PROFESSION_BUS_DEV, TAXONOMY_PROFESSION_STRATEGY_OPS, TAXONOMY_PROFESSION_PROJECT_MANAGEMENT]
    ),
    (
        Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name='Finance & Accounting',
                 key=TAXONOMY_PROFESSION_CAT_FIN_ACCT),
        [TAXONOMY_PROFESSION_FINANCE, TAXONOMY_PROFESSION_ACCOUNTING]
    ),
]

JOB_PROFESSION_KEY_MAP = {tax.key: tax for tax in JOB_PROFESSIONS}

INDUSTRIES = [
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Real Estate'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='B2B'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='B2C'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Agriculture'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Education'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Software'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Artificial Intelligence'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Finance'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Hardware'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Manufacturing'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Transportation'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Life Sciences'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Mining'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Energy'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Non-Profit'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Media & Entertainment'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Construction'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Insurance'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Retail'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Hospitality and Tourism'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Food'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Healthcare'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Management Consulting'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Fashion'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Law'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Marketing'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Technology'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Robotics'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Consumer Goods'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Telecommunications'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_INDUSTRY, name='Chemicals'),
]

JOB_LEVELS = [
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL, name='Intern', sort_order=1),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL, name='Entry Individual Contributor', sort_order=2),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL, name='Senior Individual Contributor', sort_order=3),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL, name='Manager / Director', sort_order=4),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL, name='Vice President', sort_order=5),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL, name='C-Suite', sort_order=6),
]

ALL_TAXONOMIES = {
    tax.get_unique_key(): tax for tax in JOB_LEVELS + INDUSTRIES + JOB_PROFESSIONS
}


def update_taxonomies(*args, **kwargs):
    # Only get "child" taxonomies. We'll add the parent taxonomies once we have the children
    current_taxonomies = {t.get_unique_key(): t for t in Taxonomy.objects.filter(sub_taxonomies__isnull=True)}
    tax_to_add = []
    tax_to_update = []
    tax_to_delete = []
    for tax_key, tax in ALL_TAXONOMIES.items():
        if existing_tax := current_taxonomies.get(tax_key):
            existing_tax.key = tax.key
            existing_tax.description = tax.description
            existing_tax.sort_order = tax.sort_order
            tax_to_update.append(existing_tax)
        else:
            tax_to_add.append(tax)
    
    for tax_key, current_tax in current_taxonomies.items():
        if tax_key not in ALL_TAXONOMIES:
            tax_to_delete.append(current_tax.id)
    
    Taxonomy.objects.bulk_create(tax_to_add)
    Taxonomy.objects.bulk_update(tax_to_update, ['key', 'description', 'sort_order'])
    Taxonomy.objects.filter(id__in=tax_to_delete).delete()
    
    # Update parent taxonomies
    parent_professions = {t.get_unique_key(): t for t in Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_PROFESSION, sub_taxonomies__isnull=False)}
    used_profession_keys = []
    for profession_cfg in JOB_PROFESSION_CATEGORIES:
        parent_profession_raw, child_profession_keys = profession_cfg
        profession_key = parent_profession_raw.get_unique_key()
        parent_taxonomy = parent_professions.get(profession_key)
        used_profession_keys.append(profession_key)
        if not parent_taxonomy:
            parent_profession_raw.save()
            parent_taxonomy = parent_profession_raw
        child_professions = Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_PROFESSION, key__in=child_profession_keys)
        parent_taxonomy.sub_taxonomies.set(child_professions)
        
    for profession_key, profession in parent_professions.items():
        if profession_key not in used_profession_keys:
            profession.delete()


def get_or_create_taxonomy(tax_name, tax_type):
    try:
        return Taxonomy.objects.get(name=tax_name, tax_type=tax_type)
    except Taxonomy.DoesNotExist:
        tax = Taxonomy(name=tax_name, tax_type=tax_type)
        tax.save()
        return tax


def get_or_create_job_title_tax(job_title_standardized):
    return get_or_create_taxonomy(job_title_standardized, Taxonomy.TAX_TYPE_PROFESSION)


def run_job_title_standardization(job_filter=None, is_non_standardized_only=True, limit=None, is_test=False):
    job_filter = job_filter or Q()
    if is_non_standardized_only:
        job_filter &= ~Q(taxonomy__taxonomy__tax_type=Taxonomy.TAX_TYPE_PROFESSION)
        jobs = EmployerJob.objects \
            .filter(job_filter) \
            .distinct().values('id', 'job_title')
    else:
        jobs = EmployerJob.objects.filter(job_filter).values('id', 'job_title')
    
    logger.info(f'Running job standardization for {len(jobs)} jobs')
    job_taxes_to_save = []
    if limit:
        jobs = jobs[:limit]
    for idx, job in enumerate(jobs):
        standardized_job_tax = get_standardized_job_taxonomy(job['job_title'], is_test=is_test)
        if not standardized_job_tax:
            # logger.info(f'Could not find standardized title for {job.job_title}')
            continue
        job_taxes_to_save.append(JobTaxonomy(
            taxonomy=standardized_job_tax,
            job_id=job['id'],
            created_dt=timezone.now(),
            modified_dt=timezone.now()
        ))
        if idx and (idx % 5000 == 0):
            logger.info(f'Total jobs ({idx + 1}). Removing existing taxonomies and saving new ones.')
            with atomic():
                JobTaxonomy.objects.filter(job_id__in=[jt.job_id for jt in job_taxes_to_save],
                                           taxonomy__tax_type=Taxonomy.TAX_TYPE_PROFESSION).delete()
                JobTaxonomy.objects.bulk_create(job_taxes_to_save, ignore_conflicts=True)
            job_taxes_to_save = []
    if job_taxes_to_save:
        with atomic():
            JobTaxonomy.objects.filter(job_id__in=[jt.job_id for jt in job_taxes_to_save],
                                       taxonomy__tax_type=Taxonomy.TAX_TYPE_PROFESSION).delete()
            JobTaxonomy.objects.bulk_create(job_taxes_to_save, ignore_conflicts=True)


CONFIDENCE_WEIGHT_VERY_STRONG = 10000
CONFIDENCE_WEIGHT_STRONG = 1000
CONFIDENCE_WEIGHT_NORMAL = 100
CONFIDENCE_WEIGHT_WEAK = 10

space_and_word_or_end_re = '(\W.*?$|$)'
start_or_word_and_space_re = '(^|^.+?\W)'
engineer_words = '(developer|engineer|architect|engineering)'
experience_level_words = '(chief|vp|vice president|head|executive|manager|owner|analyst|lead|leader|mgr|director|expert|intern|staff|senior|sr|principal|associate)'
customer_words = '(customer|client|partner|account|enterprise|executive)'
customer_solution_words = '(integration|specialist|solution|implementation|consultant|onboard|install|train)'
frontend_language_words = '(react|javascript|html|css|vue)'
backend_language_words = '(python|pytorch|\.net|java|ruby|drupal|c\+\+|rust|golang|php)'
devops_words = '(devops|secops|infrastructure|cloud|security|devsecops|privacy|secdev|dev ops|site reliability|aws|azure)'

TaxonomyConfidenceWeight = namedtuple('TaxonomyConfidenceWeight', 'taxonomy_key, weight')


class TaxonomyTest:
    def __init__(self, test_pattern, confidence_weights, test_negate_pattern=None):
        self.test_pattern = test_pattern
        self.confidence_weights = confidence_weights
        self.test_negate_pattern = test_negate_pattern
    
    def is_match(self, job_title):
        is_match = bool(re.match(self.test_pattern, job_title, re.IGNORECASE))
        if self.test_negate_pattern:
            is_match = is_match and not bool(re.match(self.test_negate_pattern, job_title, re.IGNORECASE))
        return is_match
    
    def get_updated_weights(self, job_title, current_weights):
        is_match = self.is_match(job_title)
        if not is_match:
            return current_weights
        for idx, confidence_weight in enumerate(self.confidence_weights):
            weight = confidence_weight.weight + len(self.confidence_weights) - idx
            try:
                current_weights[confidence_weight.taxonomy_key] += weight
            except KeyError:
                current_weights[confidence_weight.taxonomy_key] = weight
        return current_weights


JOB_TAXONOMY_TESTS = [
    TaxonomyTest(
        f'{start_or_word_and_space_re}(executive|administrative|office|personal) (assist|admin).+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_EA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}office (admin|manag).+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_EA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}ea{space_and_word_or_end_re}.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_EA, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}chief of staff.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_COS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(counsel|lawyer|attorney|paralegal|legal|intellectual property|ip){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_LAW, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}litigat.+?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_LAW, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}government.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_GOV, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(corporate|public) (compliance|affairs){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_GOV, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(compliance|fraud|risk|ethics|regulatory).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_GOV, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}product{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_DESIGN, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MARKETING, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_ENGINEERING, CONFIDENCE_WEIGHT_WEAK),
        ],
        test_negate_pattern=f'{start_or_word_and_space_re}{experience_level_words}.+?{engineer_words}{space_and_word_or_end_re}'
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}product\W.*?engineer(ing)?{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_ENGINEERING, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}product\W.*?market.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MARKETING, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}product\W.*?management{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}product\W.*?engineer{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}.*?product$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT, CONFIDENCE_WEIGHT_STRONG)],
        test_negate_pattern=f'{start_or_word_and_space_re}{experience_level_words}.+?{engineer_words}{space_and_word_or_end_re}'
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}cpo{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MANAGEMENT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{customer_words}.+?(success|delight|engagement|retention|journey|outcomes|excellence|happiness|loyalty|adoption){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CUSTOMER_SUCCESS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{customer_words}{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CUSTOMER_SUCCESS, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CUSTOMER_SUPPORT, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_SALES, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_BUS_DEV, CONFIDENCE_WEIGHT_WEAK),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{customer_words}.+?(manage|exec).+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(account|client|customer|enterprise) (development|partner|director|advocate){space_and_word_or_end_re}$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}ae{space_and_word_or_end_re}$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{customer_words} relation.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}crm{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ACCOUNT_MANAGEMENT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{engineer_words}{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_BACKEND, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_DATA, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_MOBILE, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_HARDWARE, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ML, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DATA_SCIENCE, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_IT, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_QA, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DBA, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_WEAK),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{engineer_words}.+?{experience_level_words}{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_HARDWARE, CONFIDENCE_WEIGHT_STRONG)
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}solution.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_NORMAL)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(customer|solution) engineer.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{customer_words}.+?{customer_solution_words}.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_NORMAL)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{customer_solution_words}.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(presales|professional service).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(engagement manager|implementations?|service delivery){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}technical.+?manager.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}technical.+?manager.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(account|client|customer|of|partner|product|tech).+?(services?|support|care|experience|excellence|admin|administrator){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CUSTOMER_SUPPORT, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(service desk|helpdesk|help desk).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CUSTOMER_SUPPORT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}support{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CUSTOMER_SUPPORT, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}talent.*?(acqui|sourc).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_TA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(recruiter|recruitment|recruiting){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_TA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}recruit.+?coordinat.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_TA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'.+?of talent.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_TA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(hr|people|hrbp|recursos humanos|l&d|hris|diversity|inclusion|dei){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_HR, CONFIDENCE_WEIGHT_STRONG)],
        test_negate_pattern=f'^.+?(/hr|per hr).*?$'
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(human resource|total reward).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_HR, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(training|learning|elearning){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_HR, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(compensation|benefits).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_HR, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(employee|workforce){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_HR, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}org.+?development{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_HR, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}workplace.+?experiences?{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_HR, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(embedded|system|hardware|mechanical|automation|chip|robot|manufactur|electrical|laser).+?{engineer_words}.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_HARDWARE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{frontend_language_words}{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}front{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}web develop.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(frontend|front end|front-end).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{backend_language_words}{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_BACKEND, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(backend|back end|back-end).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(mobile|android|ios){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_MOBILE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}{devops_words}{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(sre|soc|cyber security){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}linux (admin|develop).*?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(qa|quality|quality assurance){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}software test.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}software test.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(software|sw|application|xr){space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_BACKEND, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_MOBILE, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_QA, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_WEAK),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(software|sw|application|xr).+?{engineer_words}{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_NORMAL),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_FRONTEND, CONFIDENCE_WEIGHT_NORMAL),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_BACKEND, CONFIDENCE_WEIGHT_NORMAL),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_MOBILE, CONFIDENCE_WEIGHT_NORMAL),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_QA, CONFIDENCE_WEIGHT_NORMAL),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DEVOPS, CONFIDENCE_WEIGHT_NORMAL),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(cto|chief technology officer|software engineer).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(full stack|full-stack|fullstack|computer scientist).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(cto|chief technology officer).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}tech.*?(lead|manager|architect).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}sdet?{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_SOFTWARE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(chief information security officer|ciso|cyber security|data center|informatics).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_IT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(it|information|technical|network|saas|salesforce|sap|scrum|oracle|google cloud|azure|workday|netsuite){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_IT, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}applications? manager{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_IT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}cloud.+?(manager|support){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_IT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(platform manage|developer relation|data govern).+?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_IT, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}system.*?(admin|manager).+?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_IT, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(data analyst|business intelligence|bi|analytics|insights|of data|sql){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DATA_ANALYSIS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(insights|of data){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DATA_ANALYSIS, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}data scien.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DATA_SCIENCE, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(ml|ai|ml/ai|ai/ml|machine learning|computer vision|deep learning|nlp){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ML, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}data{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_DATA, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DATA_SCIENCE, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DATA_ANALYSIS, CONFIDENCE_WEIGHT_WEAK)
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}data (automation|integration){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_DATA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}data (privacy|protection|administrator|specialist|steward|support){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_DATA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}data.*?(admin|service|solution|architecture|lead).*?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ENG_DATA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(dba|database admin).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DBA, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(sdr|bdr){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_SDR, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(sales|business) development rep.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_SDR, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(cro|chief revenue officer|chief commercial officer|executivo de vendas){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_SALES, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}sales{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_SALES, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_SDR, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_CLIENT_SOLUTIONS, CONFIDENCE_WEIGHT_WEAK),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(business|corporate) dev.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_BUS_DEV, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(partner|alliance|acquisition|m&a).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_BUS_DEV, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}digital (marketer|marketing|campaign|content){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_DIGITAL, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(social|influencer|ecommmerce|e-commerce){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_DIGITAL, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}paid (ad|media|search).+?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_DIGITAL, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(seo|search engine optimization){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_SEO, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}events? market(er|ing){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_EVENTS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}corporate events?{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_EVENTS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}field market(er|ing){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_EVENTS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(pr|public relations){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PR, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}market (research|intelligence).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_RESEARCH, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}growth market(er|ing).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_GROWTH, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}demand generation{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_GROWTH, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}market(er|ing){space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_DIGITAL, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_GROWTH, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_RESEARCH, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MARKETING, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_EVENTS, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_SEO, CONFIDENCE_WEIGHT_WEAK),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}marketing\W{experience_level_words}{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_DIGITAL, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_GROWTH, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_RESEARCH, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_MARKETING, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_EVENTS, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING_SEO, CONFIDENCE_WEIGHT_STRONG),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(content|copywrit).+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_MARKETING, CONFIDENCE_WEIGHT_WEAK)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}product design.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_DESIGN, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}product.*?design.*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_DESIGN, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(ui|ux|user interface|user experience){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_UI, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}design{space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PRODUCT_DESIGN, CONFIDENCE_WEIGHT_WEAK),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_UI, CONFIDENCE_WEIGHT_WEAK),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(graphic|creative|digital|3d).+?(design|develop).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_UI, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(project|program) (manage|coordinat|implement|mang|lead).*?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PROJECT_MANAGEMENT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}pmo{space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_PROJECT_MANAGEMENT, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(analyst|analista){space_and_word_or_end_re}',
        [
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_BUSINESS_ANALYSIS, CONFIDENCE_WEIGHT_STRONG),
            TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_DATA_ANALYSIS, CONFIDENCE_WEIGHT_STRONG),
        ]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}business anal.+?$',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_BUSINESS_ANALYSIS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(strateg|operations|operational|procurement|logistic).*?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_STRATEGY_OPS, CONFIDENCE_WEIGHT_NORMAL)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(management|business) consult.*?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_STRATEGY_OPS, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(consultant|consulting){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_STRATEGY_OPS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}business (operation|owner|plan|manage|strat|trans).*?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_STRATEGY_OPS, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(supply|go-to-market|go to market|gtm|innovation){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_STRATEGY_OPS, CONFIDENCE_WEIGHT_NORMAL)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(growth|monetization){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_GROWTH, CONFIDENCE_WEIGHT_NORMAL)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(finance|financial|asset management|revenue|pricing|investment|trading|capital|controller|credit|derivatives|billing|private equity){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_FINANCE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}accounts? (payable|receivable){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_FINANCE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}accounts? (payable|receivable){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_FINANCE, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(collections|payroll|payment){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_FINANCE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(investment|bank|treasur|invoic).+?',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_FINANCE, CONFIDENCE_WEIGHT_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(fpa|fp&a){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_FINANCE, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
    TaxonomyTest(
        f'{start_or_word_and_space_re}(accountant|accounting|audit|auditor|tax){space_and_word_or_end_re}',
        [TaxonomyConfidenceWeight(TAXONOMY_PROFESSION_ACCOUNTING, CONFIDENCE_WEIGHT_VERY_STRONG)]
    ),
]


def get_standardized_job_taxonomy(job_title: str, is_test=False):
    profession_weights = {}
    for tax_test in JOB_TAXONOMY_TESTS:
        profession_weights = tax_test.get_updated_weights(job_title, profession_weights)
    
    if not profession_weights:
        if is_test:
            print(f'Could not find a profession for {job_title}')
        return None
    
    ordered_profession_weights = sorted(
        [{'key': prof_key, 'weight': weight} for prof_key, weight in profession_weights.items()],
        key=lambda x: x['weight'], reverse=True)
    if is_test:
        print(f'Profession weights for {job_title}:')
        print(ordered_profession_weights)
    
    best_profession = ordered_profession_weights[0]
    raw_profession = JOB_PROFESSION_KEY_MAP[best_profession['key']]
    return get_or_create_job_title_tax(raw_profession.name)
