# Generated by Django 4.0.7 on 2023-04-24 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0141_jobpost_jobpost_unique_employer_job_channel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employerslack',
            name='jobs_post_tod',
        ),
        migrations.AddField(
            model_name='employerslack',
            name='jobs_post_tod_minutes',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
