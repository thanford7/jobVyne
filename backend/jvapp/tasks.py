import logging

from celery import shared_task
from celery.schedules import crontab

from jobVyne.celery import app
from scrape.scraper import run_job_scrapers

logger = logging.getLogger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    logger.info(arg)
    
    
@shared_task
def task_run_job_scrapers(employer_names=None):
    run_job_scrapers(employer_names=employer_names)


@shared_task
def add(x, y):
    logger.info('Starting add task')
    return x + y
