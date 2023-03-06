from celery import shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from jobVyne.celery import app as celery_app
from scrape.scraper import run_job_scrapers

logger = get_task_logger(__name__)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    #
    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)
    #
    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


@celery_app.task
def test(arg):
    logger.info(arg)
    print(arg)
    
    
@shared_task
def task_run_job_scrapers(employer_names=None):
    logger.info('Starting job scraper task')
    run_job_scrapers(employer_names=employer_names)


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
