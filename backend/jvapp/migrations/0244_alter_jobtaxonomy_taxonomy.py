# Generated by Django 4.2.1 on 2023-08-31 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0243_userslackprofile_job_seeker_post_dt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobtaxonomy',
            name='taxonomy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job', to='jvapp.taxonomy'),
        ),
    ]
