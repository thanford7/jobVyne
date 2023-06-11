from django.db import migrations, models

from jvapp.models.employer import Employer


def add_employer_job_subscriptions(apps, schema_editor):
    employer_model = apps.get_model('jvapp', 'Employer')
    job_subscription_model = apps.get_model('jvapp', 'JobSubscription')
    
    def create_employer_subscription(employer_id):
        employer = Employer.objects.get(id=employer_id)
        employer_subscription = job_subscription_model(
            employer_id=employer_id,
            is_single_employer=True,
            title=employer.employer_name
        )
        employer_subscription.save()
        employer_subscription.filter_employer.add(employer_id)
        return employer_subscription
    
    employers = employer_model.objects.filter(organization_type=Employer.ORG_TYPE_EMPLOYER)
    for employer in employers:
        create_employer_subscription(employer.id)


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0168_jobsubscription_is_single_employer_and_more'),
    ]

    operations = [
        migrations.RunPython(
            add_employer_job_subscriptions, atomic=True
        ),
    ]
