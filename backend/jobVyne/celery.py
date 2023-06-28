import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobVyne.settings')
app = Celery('jobVyne')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# app.conf.task_routes = {'jvapp.tasks.*': {'queue': 'feeds'}}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
