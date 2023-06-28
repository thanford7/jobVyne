from celery import shared_task
from celery.utils.log import get_task_logger

from jobVyne.celery import app as celery_app
from jvapp.apis.ats import get_ats_api
from jvapp.models.employer import EmployerAts
from scrape.scraper import run_job_scrapers

logger = get_task_logger(__name__)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # No longer needed - periodic tasks are managed through django admin
    pass
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    
    
@shared_task
def task_run_job_scrapers(employer_names=None):
    logger.info('Starting job scraper task')
    run_job_scrapers(employer_names=employer_names)
    
    
@shared_task
def refresh_all_ats_credentials():
    ats_cfgs = EmployerAts.objects.select_related('employer').all()
    for ats_cfg in ats_cfgs:
        ats_api = get_ats_api(ats_cfg)
        ats_api.refresh_ats_credentials()


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
