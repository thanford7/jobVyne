import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobVyne.settings')
app = Celery('jobVyne')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
