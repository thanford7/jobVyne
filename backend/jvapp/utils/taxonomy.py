# https://docs.google.com/spreadsheets/d/1G5-9y6bp0QHjZmxIWmGtjI6F_AbuqfHmYYFmQC6p_UU/edit#gid=0
import re

from django.db.models import Count, Prefetch, Q, Subquery
from django.utils import timezone

from jvapp.models.employer import EmployerJob, JobTaxonomy, Taxonomy

JOB_TITLES = [
    'Product Manager',
    'Product Marketing Manager',
    'Customer Success Manager',
    'Account Manager',
    'HR Business Partner',
    'Talent Acquisition',
    'Training & Development',
    'HR Specialist',
    'Compensation & Benefits',
    'Recruitment Marketing',
    'Full Stack Developer',
    'Front-End Developer',
    'Back-End Developer',
    'Mobile Developer',
    'Devops Engineer',
    'QA Engineer',
    'Data Analyst',
    'Data Scientist',
    'Machine Learning / AI Engineer',
    'Data Engineer',
    'Database Administrator',
    'SDR / BDR',
    'Sales Executive',
    'Business Development',
    'Marketing Specialist',
    'Digital Marketing',
    'SEO',
    'Event Marketing',
    'Public Relations',
    'Market Research',
    'UI/UX',
    'Product Design',
    'Project Manager',
    'Business Analyst',
    'Strategy & Operations',
]

INDUSTRIES = [
    'Real Estate',
    'B2B',
    'B2C',
    'Agriculture',
    'Education',
    'Software',
    'Artificial Intelligence',
    'Finance',
    'Hardware',
    'Manufacturing',
    'Transportation',
    'Life Sciences',
    'Mining',
    'Energy',
    'Non-Profit',
    'Media & Entertainment',
    'Construction',
    'Insurance',
    'Retail',
    'Hospitality and Tourism',
    'Food',
    'Healthcare',
    'Management Consulting',
    'Fashion',
    'Law',
    'Marketing',
    'Technology',
    'Robotics',
    'Consumer Goods',
    'Telecommunications',
    'Chemicals',
]

JOB_LEVELS = [
    'Intern',
    'Entry Individual Contributor',
    'Senior Individual Contributor',
    'Manager / Director',
    'Vice President',
    'C-Suite',
]

taxonomy_cfgs = set()
for job_title in JOB_TITLES:
    taxonomy_cfgs.add((Taxonomy.TAX_TYPE_JOB_TITLE, job_title))
for industry in INDUSTRIES:
    taxonomy_cfgs.add((Taxonomy.TAX_TYPE_INDUSTRY, industry))
for job_level in JOB_LEVELS:
    taxonomy_cfgs.add((Taxonomy.TAX_TYPE_JOB_LEVEL, job_level))


def update_taxonomies(*args, **kwargs):
    current_taxonomies = {(t.tax_type, t.name): t.id for t in Taxonomy.objects.all()}
    tax_to_add = []
    tax_to_delete = []
    for tax_cfg in taxonomy_cfgs:
        if existing_tax := current_taxonomies.get(tax_cfg):
            continue
        tax_to_add.append(Taxonomy(tax_type=tax_cfg[0], name=tax_cfg[1]))
    
    for tax_key, current_tax_id in current_taxonomies.items():
        if tax_key not in taxonomy_cfgs:
            tax_to_delete.append(current_tax_id)
    
    Taxonomy.objects.bulk_create(tax_to_add)
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
    job_title_tax_query = JobTaxonomy.objects.filter(taxonomy__tax_type=Taxonomy.TAX_TYPE_JOB_TITLE)
    job_title_tax_prefetch = Prefetch(
        'taxonomy', queryset=job_title_tax_query
    )
    if is_non_standardized_only:
        # job_filter &= Q(has_job_title__isnull=True)
        job_filter &= ~Q(taxonomy__taxonomy__tax_type=Taxonomy.TAX_TYPE_JOB_TITLE)
        # .annotate(has_job_title=Subquery(job_title_tax_query.annotate(c=Count('*')).values('c')))\
        jobs = EmployerJob.objects\
            .prefetch_related(job_title_tax_prefetch)\
            .filter(job_filter)\
            .distinct()
    else:
        jobs = EmployerJob.objects \
            .prefetch_related(job_title_tax_prefetch) \
            .filter(job_filter)
    
    job_taxes_to_save = []
    for idx, job in enumerate(jobs):
        # TODO: Make sure this doesn't delete taxonomies other than job title
        job.taxonomy.all().delete()  # Remove existing taxonomy
        standardized_job_tax = get_standardized_job_taxonomy(job.job_title)
        if not standardized_job_tax:
            continue
        job_taxes_to_save.append(JobTaxonomy(
            taxonomy=standardized_job_tax,
            job=job,
            created_dt=timezone.now(),
            modified_dt=timezone.now()
        ))
        if idx and (idx % 100 == 0 or idx == len(jobs)):
            print(f'Total jobs ({idx + 1}). Saving jobs.')
            JobTaxonomy.objects.bulk_create(job_taxes_to_save)
            job_taxes_to_save = []

    
def get_standardized_job_taxonomy(job_title: str):
    job_title = job_title.lower()
    space_and_word_or_end_re = '(\W.+?$|$)'
    start_or_word_and_space_re = '(^|^.+?\W)'
    if any((
        re.match(f'{start_or_word_and_space_re}product (manager|owner|analyst|lead|management|operations|mgr){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}chief product{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Product Manager')
    if re.match(f'{start_or_word_and_space_re}product market.+?$', job_title):
        return get_or_create_job_title_tax('Product Marketing Manager')
    if any((
        re.match(f'{start_or_word_and_space_re}customer success.+?$', job_title),
    )):
        return get_or_create_job_title_tax('Customer Success Manager')
    if any((
        re.match(f'{start_or_word_and_space_re}account manage.+?$', job_title),
    )):
        return get_or_create_job_title_tax('Account Manager')
    if any((
        re.match(f'{start_or_word_and_space_re}hr business.+?$', job_title),
        re.match(f'{start_or_word_and_space_re}hrbp.*?$', job_title),
    )):
        return get_or_create_job_title_tax('HR Business Partner')
    if any((
        re.match(f'{start_or_word_and_space_re}talent acquisition.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Talent Acquisition')
    if any((
        re.match(f'{start_or_word_and_space_re}training.+?development.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Training & Development')
    if any((
        re.match(f'{start_or_word_and_space_re}hr specialist.*?$', job_title),
    )):
        return get_or_create_job_title_tax('HR Specialist')
    if any((
        re.match(f'{start_or_word_and_space_re}(compensation|benefits).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Compensation & Benefits')
    if any((
        re.match(f'{start_or_word_and_space_re}recruitment market.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Recruitment Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}full stack (developer|engineer).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Full Stack Developer')
    if any((
        re.match(f'{start_or_word_and_space_re}front.+?(developer|engineer).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Front-End Developer')
    if any((
        re.match(f'{start_or_word_and_space_re}front.+?(developer|engineer).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Back-End Developer')
    if any((
        re.match(f'{start_or_word_and_space_re}mobile.+?(developer|engineer).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Mobile Developer')
    if any((
        re.match(f'{start_or_word_and_space_re}devops.+?(developer|engineer).*?$', job_title),
        re.match(f'{start_or_word_and_space_re}sre{space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}site reliability engineer{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Devops Engineer')
    if any((
        re.match(f'{start_or_word_and_space_re}(qa|quality).+?(developer|engineer).*?$', job_title),
    )):
        return get_or_create_job_title_tax('QA Engineer')
    if any((
        re.match(f'{start_or_word_and_space_re}data analyst{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Data Analyst')
    if any((
        re.match(f'{start_or_word_and_space_re}data scien.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Data Scientist')
    if any((
        re.match(f'{start_or_word_and_space_re}(ml|ai|machine learning).+?(developer|engineer).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Machine Learning / AI Engineer')
    if any((
        re.match(f'{start_or_word_and_space_re}data engineer{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Data Engineer')
    if any((
        re.match(f'{start_or_word_and_space_re}(dba|database admin).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Database Administrator')
    if any((
        re.match(f'{start_or_word_and_space_re}(sdr|bdr){space_and_word_or_end_re}', job_title),
        re.match(f'{start_or_word_and_space_re}(sales|business) development rep.*?$', job_title),
    )):
        return get_or_create_job_title_tax('SDR / BDR')
    if any((
        re.match(f'{start_or_word_and_space_re}sales{space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Sales Executive')
    if any((
        re.match(f'{start_or_word_and_space_re}business dev.+?$', job_title),
    )):
        return get_or_create_job_title_tax('Business Development')
    if any((
        re.match(f'{start_or_word_and_space_re}digital market(er|ing){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Digital Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}(seo|search engine optimization){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('SEO')
    if any((
        re.match(f'{start_or_word_and_space_re}event market(er|ing){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Event Marketing')
    if any((
        re.match(f'{start_or_word_and_space_re}(pr|public relations){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Public Relations')
    if any((
        re.match(f'{start_or_word_and_space_re}market research.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Market Research')
    if any((
        re.match(f'{start_or_word_and_space_re}market(er|ing).*?$', job_title),
    )):
        return get_or_create_job_title_tax('Marketing Specialist')
    if any((
        re.match(f'{start_or_word_and_space_re}(ui|ux|user interface|user experience){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('UI/UX')
    if any((
        re.match(f'{start_or_word_and_space_re}product design.*?', job_title),
    )):
        return get_or_create_job_title_tax('Product Design')
    if any((
        re.match(f'{start_or_word_and_space_re}project manage.*?$', job_title),
    )):
        return get_or_create_job_title_tax('Project Manager')
    if any((
        re.match(f'{start_or_word_and_space_re}business anal.+?$', job_title),
    )):
        return get_or_create_job_title_tax('Business Analyst')
    if any((
        re.match(f'{start_or_word_and_space_re}(strategy|operations){space_and_word_or_end_re}', job_title),
    )):
        return get_or_create_job_title_tax('Strategy & Operations')

    return None
