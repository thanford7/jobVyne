import logging
from itertools import groupby

from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.db.models import Count

from jvapp.models import EmployerJob, Taxonomy, JobTaxonomy, TaxType
from jvapp.utils import ai


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Max number of jobs to bucketize',
        )

    def handle(self, *args, **options):
        limit = options['limit']

        # Find jobs that have not yet been 'bucketed'
        jobs = (
            EmployerJob.objects
            .annotate(job_taxonomy_count=Count('jobtaxonomy'))
            .filter(job_taxonomy_count__lt=TaxType.objects.count())
            [:limit]
        )

        taxonomies = Taxonomy.objects.all().order_by('tax_type')
        taxonomies_by_type = {
            tax_type.name: ', '.join(list(t.name for t in tax_list)) for tax_type, tax_list in groupby(taxonomies, lambda t: t.tax_type)
        }

        for job in jobs:
            prompt = (
                'Choose Title from one of the following options:\n'
                f'{taxonomies_by_type["Title"]}\n\n'
                'Choose Level from one of the following options:\n'
                f'{taxonomies_by_type["Level"]}\n\n'
                'Description: Senior Infrastructure Engineer and Tech Lead: As the inaugural member of our infrastructure team, you will have hands-on responsibility for the design evolution, implementation, security, and maintenance of all parts of Hospital IQ\'s cloud infrastructure. You will collaborate closely with our other engineers as you set the technical direction and growth of this team. This is an essential role as we rapidly scale our platform to serve hospitals on our quest to make healthcare more efficient.\n'
                'JSON: {\n'
                '  "Level": "Manager / Director",\n'
                '  "Title": "Devops engineer"\n'
                '}\n\n'
                'Description: EHSQ Systems Analyst: As an EHSQ Systems Analyst, you will be focused on users and the administration of their data through Intelex, Invenergy’s compliance management and EHSQ software system. You will be focusing on coordinating the training tracking between the Learning Management System, LMS, and maintaining the records in Intelex. You will be working with the Training Team to align courses and qualifications between the systems. The Systems Analyst will conduct data entry, data analysis, and create training reports as needed.'
                'JSON: {\n'
                '  "Level": "Entry level / Individual contributor",\n'
                '  "Title": "Data analyst"\n'
                '}\n\n'
                f'Description: {job.job_title}\n{BeautifulSoup(job.job_description).text}\n'
                'JSON: '
            )
            # resp = {
            #     'Level': 'C-suite',
            #     'Title': 'Account manager',
            # }
            resp = ai.ask(prompt, model='davinci')
            print(resp)
            return
            for taxTypeName, taxName in resp.items():
                try:
                    tax = Taxonomy.objects.get(tax_type__name=taxTypeName, name=taxName)
                    JobTaxonomy(job=job, taxonomy=tax).save()
                except Taxonomy.DoesNotExist:
                    logging.error(f'Could not find taxonomy {taxName} for taxonomy type {taxTypeName}')
