# Generated by Django 4.2.1 on 2023-08-07 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0217_remove_employerjobconnection_is_job_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobvyneuser',
            name='job_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jvapp.taxonomy'),
        ),
    ]
