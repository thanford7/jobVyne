# Generated by Django 4.0.7 on 2023-02-05 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0109_employer_has_job_scrape_failure_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='is_manual_job_entry',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
