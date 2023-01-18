import logging
from time import sleep

from django.core.management import BaseCommand

from jvapp.apis.ats import get_ats_api
from jvapp.models import EmployerAts


logger = logging.getLogger(__name__)


def save_ats_data(writer, success_style):
    ats_cfgs = EmployerAts.objects.select_related('employer').all()
    for ats in ats_cfgs:
        writer(f'Starting to save jobs for {ats.employer.employer_name}')
        ats_api = get_ats_api(ats)
        try:
            jobs = ats_api.get_jobs()
            ats_api.save_jobs(jobs)
        except Exception as e:
            logger.error(f'Error saving jobs for {ats.employer.employer_name}', exc_info=e)
            writer(f'Error saving jobs for {ats.employer.employer_name}')
            writer(e)
        writer(f'Successfully saved jobs for {ats.employer.employer_name}')

        writer(f'Starting to save application statuses for {ats.employer.employer_name}')
        try:
            application_statuses = ats_api.get_application_statuses()
            ats_api.save_application_statuses(application_statuses)
        except Exception as e:
            logger.error(f'Error saving application statuses for {ats.employer.employer_name}', exc_info=e)
            writer(f'Error saving application statuses for {ats.employer.employer_name}')
            writer(e)
        writer(f'Successfully saved application statuses for {ats.employer.employer_name}')
        
    writer(success_style(f'Updated data from ATS for {len(ats_cfgs)} employers'))


class Command(BaseCommand):
    help = 'Update JobVyne data with ATS jobs and application statuses'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--schedule_minutes',
            type=int,
            help='Minutes between when task is run',
        )
    
    def handle(self, *args, **options):
        writer = self.stdout.write
        success_style = self.style.SUCCESS
        schedule_minutes = options['schedule_minutes']
        if schedule_minutes:
            while True:
                save_ats_data(writer, success_style)
                writer(f'Waiting {schedule_minutes} minutes for next run')
                sleep(schedule_minutes*60)
        else:
            save_ats_data(writer, success_style)
