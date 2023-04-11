# Generated by Django 4.0.7 on 2023-03-23 20:36

from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


def add_application_requirements(apps, schema_editor):
    EmployerJobApplicationRequirement = apps.get_model('jvapp', 'EmployerJobApplicationRequirement')
    Employer = apps.get_model('jvapp', 'Employer')
    employers = Employer.objects.all()
    for employer in employers:
        requirements = [
            EmployerJobApplicationRequirement(
                created_dt=timezone.now(), modified_dt=timezone.now(),
                application_field='first_name', is_required=True, is_optional=False, is_hidden=False, is_locked=True
            ),
            EmployerJobApplicationRequirement(
                created_dt=timezone.now(), modified_dt=timezone.now(),
                application_field='last_name', is_required=True, is_optional=False, is_hidden=False, is_locked=True
            ),
            EmployerJobApplicationRequirement(
                created_dt=timezone.now(), modified_dt=timezone.now(),
                application_field='email', is_required=True, is_optional=False, is_hidden=False, is_locked=True
            ),
            EmployerJobApplicationRequirement(
                created_dt=timezone.now(), modified_dt=timezone.now(),
                application_field='phone_number', is_required=False, is_optional=True, is_hidden=False, is_locked=False
            ),
            EmployerJobApplicationRequirement(
                created_dt=timezone.now(), modified_dt=timezone.now(),
                application_field='linkedin_url', is_required=False, is_optional=True, is_hidden=False, is_locked=False
            ),
            EmployerJobApplicationRequirement(
                created_dt=timezone.now(), modified_dt=timezone.now(),
                application_field='resume', is_required=True, is_optional=False, is_hidden=False, is_locked=False
            ),
            EmployerJobApplicationRequirement(
                created_dt=timezone.now(), modified_dt=timezone.now(),
                application_field='academic_transcript', is_required=False, is_optional=False, is_hidden=True,
                is_locked=False
            )
        ]
        for application_requirement in requirements:
            application_requirement.employer = employer
        
        EmployerJobApplicationRequirement.objects.bulk_create(requirements)


class Migration(migrations.Migration):
    dependencies = [
        ('jvapp', '0129_employerjobapplicationrequirement'),
    ]
    
    operations = [
        migrations.RunPython(add_application_requirements, atomic=True)
    ]