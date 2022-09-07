from django.core.management import BaseCommand

from jvapp.apis.ats import get_ats_api
from jvapp.models import EmployerAts


class Command(BaseCommand):
    help = 'Saves jobs from ATS to database'
    
    def handle(self, *args, **options):
        ats_cfgs = EmployerAts.objects.select_related('employer').all()
        for ats in ats_cfgs:
            self.stdout.write(f'Starting to save jobs for {ats.employer.employer_name}')
            ats_api = get_ats_api(ats)
            try:
                jobs = ats_api.get_jobs()
                ats_api.save_jobs(ats.employer_id, jobs)
            except Exception as e:
                self.stdout.write(f'Error saving jobs for {ats.employer.employer_name}')
                self.stdout.write(e)
            self.stdout.write(f'Successfully saved jobs for {ats.employer.employer_name}')
        self.stdout.write(self.style.SUCCESS(f'Updated jobs data from ATS for {len(ats_cfgs)} employers'))
