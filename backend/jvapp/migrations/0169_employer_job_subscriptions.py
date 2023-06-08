from django.db import migrations, models

from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.models.employer import Employer


def add_employer_job_subscriptions(apps, schema_editor):
    employer_model = apps.get_model('jvapp', 'Employer')
    employers = employer_model.objects.filter(organization_type=Employer.ORG_TYPE_EMPLOYER)
    for employer in employers:
        JobSubscriptionView.create_employer_subscription(employer.id)


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0168_jobsubscription_is_single_employer_and_more'),
    ]

    operations = [
        migrations.RunPython(
            add_employer_job_subscriptions, atomic=True
        ),
    ]
