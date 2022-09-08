from time import sleep

from django.core.management import BaseCommand

from jvapp.apis.ats import get_ats_api
from jvapp.models import EmployerAts


def save_jobs(writer, success_style):
    ats_cfgs = EmployerAts.objects.select_related('employer').all()
    for ats in ats_cfgs:
        writer(f'Starting to save jobs for {ats.employer.employer_name}')
        ats_api = get_ats_api(ats)
        try:
            jobs = ats_api.get_jobs()
            ats_api.save_jobs(ats.employer_id, jobs)
        except Exception as e:
            writer(f'Error saving jobs for {ats.employer.employer_name}')
            writer(e)
        writer(f'Successfully saved jobs for {ats.employer.employer_name}')
    writer(success_style(f'Updated jobs data from ATS for {len(ats_cfgs)} employers'))


class Command(BaseCommand):
    help = 'Saves jobs from ATS to database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--schedule_minutes',
            type=int,
            help='Include ancillary data',
        )
    
    def handle(self, *args, **options):
        writer = self.stdout.write
        success_style = self.style.SUCCESS
        schedule_minutes = options['schedule_minutes']
        if schedule_minutes:
            while True:
                save_jobs(writer, success_style)
                writer(f'Waiting {schedule_minutes} minutes for next run')
                sleep(schedule_minutes*60)
        else:
            save_jobs(writer, success_style)
