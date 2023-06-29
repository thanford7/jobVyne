# https://docs.google.com/spreadsheets/d/1G5-9y6bp0QHjZmxIWmGtjI6F_AbuqfHmYYFmQC6p_UU/edit#gid=0
from jvapp.models.employer import Taxonomy

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
