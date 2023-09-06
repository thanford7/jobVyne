# Generated by Django 4.2.1 on 2023-09-04 16:04

import django.core.validators
from django.db import migrations, models
from django.utils import timezone

import jvapp.utils.file
from jvapp.models.employer import Employer, EmployerJobApplicationRequirement


def add_application_requirements(apps, schema_editor):
    employers = Employer.objects.all()
    for employer in employers:
        EmployerJobApplicationRequirement(
            employer=employer, created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='cover_letter', is_required=False, is_optional=False, is_hidden=True,
            is_locked=False
        ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0250_remove_employerconnection_unique_employer_connection_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='cover_letter',
            field=models.FileField(blank=True, null=True, upload_to=jvapp.utils.file.get_user_upload_location, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'txt', 'rtf'])]),
        ),
        migrations.RunPython(add_application_requirements, atomic=True)
    ]