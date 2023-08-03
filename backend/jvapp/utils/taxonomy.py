# https://docs.google.com/spreadsheets/d/1G5-9y6bp0QHjZmxIWmGtjI6F_AbuqfHmYYFmQC6p_UU/edit#gid=0
import logging
import re

from django.db.models import Count, Prefetch, Q, Subquery
from django.db.transaction import atomic
from django.utils import timezone

from jvapp.models.employer import EmployerJob, JobTaxonomy, Taxonomy

logger = logging.getLogger(__name__)

JOB_PROFESSIONS = [
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Executive Assistant', key='ea'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Chief of Staff', key='cos'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Law', key='law'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Government & Regulation', key='gov'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Product Management', key='product-management'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Product Marketing', key='product-marketing'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Customer Success', key='customer-success'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Account Management', key='account-management'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Client Solutions', key='client-solutions'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Customer Support', key='customer-support'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Human Resources', key='hr'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Talent Acquisition', key='ta'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Hardware Engineering', key='eng-hardware'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Software Engineering', key='eng-software'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Front-End Development', key='eng-frontend'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Back-End Development', key='eng-backend'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Mobile Development', key='eng-mobile'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Devops Engineering', key='devops'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='QA Engineering', key='qa'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='IT (Non-Engineering)', key='it'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Data Analysis', key='data-analysis'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Data Science', key='data-science'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Machine Learning / AI Engineering', key='ml'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Data Engineering', key='eng-data'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Database Administration', key='dba'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='SDR / BDR', key='sdr'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Sales Executive', key='sales'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Business/Corporate Development', key='bus-dev'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Marketing', key='marketing'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Growth Marketing', key='marketing-growth'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Digital Marketing', key='marketing-digital'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='SEO', key='marketing-seo'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Event Marketing', key='marketing-events'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Public Relations', key='pr'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Market Research', key='marketing-research'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='UI/UX', key='ui'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Product Design', key='product-design'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Project Management', key='project-management'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Business Analysis', key='business-analysis'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Strategy & Operations', key='strategy-ops'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Growth', key='growth'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Finance', key='finance'),
    Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name='Accounting', key='accounting')
]

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
    current_taxonomies = {t.get_unique_key(): t for t in Taxonomy.objects.all()}
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
    
    
def get_or_create_taxonomy(tax_name, tax_type):
    try:
        return Taxonomy.objects.get(name=tax_name, tax_type=tax_type)
    except Taxonomy.DoesNotExist:
        tax = Taxonomy(name=tax_name, tax_type=tax_type)
        tax.save()
        return tax
    

def get_or_create_job_title_tax(job_title_standardized):
    return get_or_create_taxonomy(job_title_standardized, Taxonomy.TAX_TYPE_JOB_TITLE)


def run_job_title_standardization(job_filter=None, is_non_standardized_only=True):
    job_filter = job_filter or Q()
    if is_non_standardized_only:
        job_filter &= ~Q(taxonomy__taxonomy__tax_type=Taxonomy.TAX_TYPE_JOB_TITLE)
        jobs = EmployerJob.objects\
            .filter(job_filter)\
            .distinct().values('id', 'job_title')
    else:
        jobs = EmployerJob.objects.filter(job_filter).values('id', 'job_title')
    
    logger.info(f'Running job standardization for {len(jobs)} jobs')
    job_taxes_to_save = []
    for idx, job in enumerate(jobs):
        standardized_job_tax = get_standardized_job_taxonomy(job['job_title'])
        if not standardized_job_tax:
            # logger.info(f'Could not find standardized title for {job.job_title}')
            continue
        job_taxes_to_save.append(JobTaxonomy(
            taxonomy=standardized_job_tax,
            job_id=job['id'],
            created_dt=timezone.now(),
            modified_dt=timezone.now()
        ))
        if (idx and (idx % 5000 == 0 or idx == len(jobs) - 1)) or len(jobs) == 1:
            logger.info(f'Total jobs ({idx + 1}). Removing existing taxonomies and saving new ones.')
            with atomic():
                JobTaxonomy.objects.filter(job_id__in=[jt.job_id for jt in job_taxes_to_save], taxonomy__tax_type=Taxonomy.TAX_TYPE_JOB_TITLE).delete()
                JobTaxonomy.objects.bulk_create(job_taxes_to_save, ignore_conflicts=True)
            job_taxes_to_save = []

    
def get_standardized_job_taxonomy(job_title: str):
    job_title = job_title.lower()
    space_and_word_or_end_re = '(\W.*?$|$)'
    start_or_word_and_space_re = '(^|^.+?\W)'
    engineer_words = '(developer|engineer|architect)'
    if any((
        re.match(f'{start_or_word_and_space_re}(executive|administrative|office|personal) (assist|admin).+?$', job_title),
        re.match(f'{start_or_word_and_space_re}office (admin|manag).+?$', job_title),
        re.match(f'{start_or_word_and_space_re}ea{space_and_word_or_end_re}.+?$', job_title),
    )):
        return get_or_create_job_title_tax('Executive Assistant')
    if any((
        re.match(f'{start_or_word_and_space_re}chief of staff.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Chief Of Staff')
    if any((
        re.match(f'{start_or_word_and_space_re}(counsel|lawyer|attorney|paralegal|legal|intellectual property|ip){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}litigat.+?', job_title),
    )):
        return get_or_create_job_title_tax('Law')
    if any((
        re.match(f'{start_or_word_and_space_re}government.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}(corporate|public) (compliance|affairs){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(compliance|fraud|risk|ethics|regulatory).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Government & Regulation')
    if re.match(f'{start_or_word_and_space_re}product\W.*?market.+?$', job_title):
        return get_or_create_job_title_tax('Product Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}product\W.*?(manager|owner|analyst|lead|leader|management|mgr|director|expert|intern|line){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(chief|vp|vice president|head|director|manager).+?product (officer|manage).*?', job_title),
        re.match(f'{start_or_word_and_space_re}(chief|vp|vice president|head|director|manager).+?product$', job_title),
        re.match(f'{start_or_word_and_space_re}cpo{space_and_word_or_end_re}', job_title),
    )) and not re.match(f'{start_or_word_and_space_re}(design|support|product development|designer|engineer|engineering){space_and_word_or_end_re}', job_title):
        return get_or_create_job_title_tax('Product Management')
    if any((
        re.match(f'{start_or_word_and_space_re}(customer|client|partner).+?(success|delight|engagement|retention|journey|outcomes|excellence|happiness|loyalty|adoption){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(success|adoption) manager{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}tech.*?adoption{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Customer Success')
    if any((
        re.match(f'{start_or_word_and_space_re}(account|client|customer|enterprise).+?(manage|exec).+?$', job_title),
        re.match(f'{start_or_word_and_space_re}(account|client|customer|enterprise) (development|partner|director|advocate){space_and_word_or_end_re}$', job_title),
        re.match(f'{start_or_word_and_space_re}(account|client|customer|enterprise|partner) relation.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}crm{space_and_word_or_end_re}', job_title),
    )) and not any((
        re.match(f'{start_or_word_and_space_re}{engineer_words}{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}receivable{space_and_word_or_end_re}', job_title)
    )):
        return get_or_create_job_title_tax('Account Management')
    if any((
        re.match(f'{start_or_word_and_space_re}solution.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}(client|customer|enterprise|of|partner|product|technical).+?(integration|specialist|solution|implementation|consultant|onboard|install|train).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}presales.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}professional service.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(engagement manager|implementations?|service delivery){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}technical.+?manager.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Client Solutions')
    if any((
        re.match(f'{start_or_word_and_space_re}(account|client|customer|of|partner|product|tech).+?(services?|support|care|experience|excellence){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}service desk.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(helpdesk|help desk).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}support{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Customer Support')
    if any((
        re.match(f'{start_or_word_and_space_re}talent.*?(acqui|sourc).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(recruiter|recruitment|recruiting){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}recruit.+?coordinat.+?$', job_title),
        re.match(f'.+?of talent.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Talent Acquisition')
    if any((
        re.match(f'{start_or_word_and_space_re}(hr|people|hrbp|recursos humanos){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}human resource.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(training|learning|elearning|l&d){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(compensation|benefits|total reward).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}dei{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(diversity|inclusion){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(employee|workforce){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}org.+?development{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}hris{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}workplace.+?experiences?{space_and_word_or_end_re}', job_title),
    )) and not any((
        re.match(f'{start_or_word_and_space_re}(machine learning|deep learning|employee cloud){space_and_word_or_end_re}', job_title),
        re.match(f'^.+?(/hr|per hr).*?$', job_title),  # Avoid common patterns for hourly wages
    )):
        return get_or_create_job_title_tax('Human Resources')
    if any((
        re.match(f'{start_or_word_and_space_re}(embedded|system|hardware|mechanical|automation|chip|robot).+?{engineer_words}.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Hardware Engineering')
    if any((
        re.match(f'{start_or_word_and_space_re}(front|javascript|react|web).+?{engineer_words}.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}{engineer_words}.+?(front|javascript|react).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}web develop.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(frontend|front end|front-end).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Front-End Development')
    if any((
        re.match(f'{start_or_word_and_space_re}(back|python|pytorch|\.net|java|ruby|drupal|c\+\+|rust|golang|php).+?{engineer_words}.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}{engineer_words}.+?(back|python|pytorch|\.net|java|ruby|drupal|c\+\+|rust|golang|php).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(backend|back end|back-end).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Back-End Development')
    if any((
        re.match(f'{start_or_word_and_space_re}(mobile|android|ios).+?{engineer_words}.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(android|ios){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Mobile Development')
    
    devops_words = '(devops|secops|infrastructure|cloud|security|devsecops|privacy|secdev|dev ops|site reliability|aws|azure)'
    if any((
        re.match(f'{start_or_word_and_space_re}{devops_words}.+?{engineer_words}.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}{engineer_words}.+?{devops_words}.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(sre|soc){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}cyber security{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}linux (admin|develop).*?', job_title),
        re.match(f'{start_or_word_and_space_re}(devops|secops|devsecops|secdev|dev ops|information security|cloud security){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Devops Engineering')
    if any((
        re.match(f'{start_or_word_and_space_re}(qa|quality|software test).+?{engineer_words}.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(qa|quality assurance){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('QA Engineering')
    if any((
        re.match(f'{start_or_word_and_space_re}(software|sw|application|enterprise|xr) {engineer_words}.*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(cto|chief technology officer).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(engineer|full stack|full-stack|fullstack|software develop|computer scientist).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}tech.*?(lead|manager|architect).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}sdet?{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Software Engineering')
    if any((
        re.match(f'{start_or_word_and_space_re}(chief information security officer|ciso|cyber security|data center|informatics).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}(it|information|technical|network|saas|salesforce|sap|scrum|oracle|google cloud|azure|workday|netsuite){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}applications? manager{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}cloud.+?(manager|support){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}platform manage.+?', job_title),
        re.match(f'{start_or_word_and_space_re}developer relation.+?', job_title),
        re.match(f'{start_or_word_and_space_re}data govern.+?', job_title),
        re.match(f'{start_or_word_and_space_re}system.*?(admin|manager).+?', job_title),
    )):
        return get_or_create_job_title_tax('IT (Non-Engineering)')
    if any((
        re.match(f'{start_or_word_and_space_re}(data analyst|business intelligence|bi|analytics|insights|of data|sql){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Data Analysis')
    if any((
        re.match(f'{start_or_word_and_space_re}data scien.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Data Science')
    if any((
        re.match(f'{start_or_word_and_space_re}(ml|ai|ml/ai|ai/ml|machine learning|computer vision|deep learning|nlp){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Machine Learning / AI Engineering')
    if any((
        re.match(f'{start_or_word_and_space_re}data.*?{engineer_words}{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}data (automation|integration){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}data (privacy|protection|administrator|specialist|steward|support){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}data.*?(admin|service|solution|architecture|lead).*?', job_title),
    )):
        return get_or_create_job_title_tax('Data Engineering')
    if any((
        re.match(f'{start_or_word_and_space_re}(dba|database admin).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Database Administration')
    if any((
        re.match(f'{start_or_word_and_space_re}(sdr|bdr){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(sales|business) development rep.*?$', job_title),
    )):
        return get_or_create_job_title_tax('SDR / BDR')
    if any((
        re.match(f'{start_or_word_and_space_re}(sales|cro|chief revenue officer|chief commercial officer|executivo de vendas){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Sales Executive')
    if any((
        re.match(f'{start_or_word_and_space_re}(business|corporate) dev.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}(partner|alliance|acquisition|m&a).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Business/Corporate Development')
    if any((
        re.match(f'{start_or_word_and_space_re}digital (marketer|marketing|campaign|content){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(social|influencer|ecommmerce|e-commerce){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}paid (ad|media|search).+?', job_title),
    )):
        return get_or_create_job_title_tax('Digital Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}(seo|search engine optimization){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('SEO')
    if any((
        re.match(f'{start_or_word_and_space_re}events? market(er|ing){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}corporate events?{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}field market(er|ing){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Event Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}(pr|public relations){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Public Relations')
    if any((
        re.match(f'{start_or_word_and_space_re}market (research|intelligence).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Market Research')
    if any((
        re.match(f'{start_or_word_and_space_re}growth market(er|ing).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Growth Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}market(er|ing).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}content.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}copywrit.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}demand generation{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}product design.*?', job_title),
    )):
        return get_or_create_job_title_tax('Product Design')
    if any((
        re.match(f'{start_or_word_and_space_re}(ui|ux|user interface|user experience){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}design{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(graphic|creative|digital|3d).+?(design|develop).*?$', job_title),
    )):
        return get_or_create_job_title_tax('UI/UX')
    if any((
        re.match(f'{start_or_word_and_space_re}(project|program) (manage|coordinat|implement|mang|lead).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}pmo{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Project Management')
    if any((
        re.match(f'{start_or_word_and_space_re}business anal.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}analyst{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}analista{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Business Analysis')
    if any((
        re.match(f'{start_or_word_and_space_re}(strateg|operations|operational|procurement|logistic).*?', job_title),
        re.match(f'{start_or_word_and_space_re}(management|business) consult.*?', job_title),
        re.match(f'{start_or_word_and_space_re}business (operation|owner|plan|manage|strat|trans).*?', job_title),
        re.match(f'{start_or_word_and_space_re}(supply|go-to-market|go to market|gtm|innovation){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Strategy & Operations')
    if any((
        re.match(f'{start_or_word_and_space_re}(growth|monetization){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Growth')
    if any((
        re.match(f'{start_or_word_and_space_re}(finance|financial|asset management|revenue|pricing|investment|trading|capital|controller|credit|derivatives|billing|private equity){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}accounts? (payable|receivable){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(collections|payroll|payment){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(investment|bank|treasur|invoic).+?', job_title),
        re.match(f'{start_or_word_and_space_re}(fpa|fp&a){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Finance')
    if any((
        re.match(f'{start_or_word_and_space_re}(accountant|accounting|audit|auditor|tax){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Accounting')

    return None
