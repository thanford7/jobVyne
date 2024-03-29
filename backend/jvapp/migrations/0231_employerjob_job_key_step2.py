# Generated by Django 4.2.1 on 2023-08-18 21:42

from django.db import migrations, models
import uuid


def gen_uuid(apps, schema_editor):
    employer_job_model = apps.get_model('jvapp', 'EmployerJob')
    for job in employer_job_model.objects.filter():
        job.job_key = uuid.uuid4()
        job.save(update_fields=['job_key'])


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0230_employerjob_job_key_step1'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
