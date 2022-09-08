import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobVyne.settings')
app = Celery('cron-jobs')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app = Celery('cron-jobs',
#              broker='amqp://',
#              backend='rpc://',
#              include=['cron-jobs.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# if __name__ == '__main__':
#     app.start()
