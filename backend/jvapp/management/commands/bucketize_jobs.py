from itertools import groupby

import openai
from django.core.management import BaseCommand

from jvapp.models import EmployerJob, Taxonomy


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Max number of jobs to bucketize',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        jobs = EmployerJob.objects.filter()[:limit]  # TODO: Filter un-bucket jobs
        taxonomies = Taxonomy.objects.all().order_by('tax_type')
        taxonomies_by_type = groupby(taxonomies, lambda t: t.tax_type)
        for job in jobs:
            prompt = (
                '"""'
                f'Job title: {job.job_title}\n'
                f'Job description: {job.job_description}\n'
                '"""\n\n'
            )
            for tax_type, taxonomies in taxonomies_by_type:
                prompt += f'Categorize the {tax_type} of the job as one of the following: ({[t.name for t in taxonomies]}). Call this output {tax_type}.\n\n'

            prompt += (
                'Provide the response as as the following format:\n\n'
                'Title: <title>\n'
                'Level: <level>\n'
            )
            resp = openai.Completion.create(
                model='davinci',
                prompt=prompt,
                temperature=0.1,
            )
            print(resp)
            # TODO: Parse response and save taxonomies
