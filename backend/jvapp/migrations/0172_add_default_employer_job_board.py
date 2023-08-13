from django.db import migrations, models

from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.models.employer import Employer


def create_default_job_board(apps, schema_editor):
    employer_model = apps.get_model('jvapp', 'Employer')
    social_link_model = apps.get_model('jvapp', 'SocialLink')
    current_default_job_boards = {
        sl.employer_id: sl for sl in
        social_link_model.objects.filter(employer_id__isnull=False, owner_id__isnull=True, is_default=True)
    }
    for employer in employer_model.objects.all():
        # Already have a default job board
        if current_default_job_boards.get(employer.id):
            continue
        link = social_link_model(
            is_default=True, name='Main Job Board', employer_id=employer.id
        )
        link.save()
        # If this is an employer then, they should only be subscribed to their jobs
        if employer.organization_type & Employer.ORG_TYPE_EMPLOYER:
            employer_subscription = JobSubscriptionView.get_or_create_employer_own_subscription(employer.id)
            link.job_subscriptions.add(employer_subscription.id)


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0171_remove_sociallink_is_primary_and_more'),
    ]

    operations = [
        migrations.RunPython(
            create_default_job_board, atomic=True
        ),
    ]
