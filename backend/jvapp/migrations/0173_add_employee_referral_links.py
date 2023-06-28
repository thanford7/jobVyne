from django.db import migrations, models

from jvapp.apis.social import SocialLinkView
from jvapp.models.employer import Employer


def create_referral_links(apps, schema_editor):
    employer_model = apps.get_model('jvapp', 'Employer')
    for employer in employer_model.objects.prefetch_related('employee').filter(organization_type=Employer.ORG_TYPE_EMPLOYER):
        SocialLinkView.get_or_create_employee_referral_links(employer.employee.all(), employer)


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0172_add_default_employer_job_board'),
    ]

    operations = [
        migrations.RunPython(
            create_referral_links, atomic=True
        ),
    ]
