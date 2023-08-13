from django.db import migrations, models

from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.models.employer import Employer


def fix_referral_links(apps, schema_editor):
    employer_model = apps.get_model('jvapp', 'Employer')
    social_link_model = apps.get_model('jvapp', 'SocialLink')
    for employer in employer_model.objects.filter(organization_type=Employer.ORG_TYPE_EMPLOYER):
        employer_subscription = JobSubscriptionView.get_or_create_employer_own_subscription(employer.id)
        employer_links = social_link_model.objects.prefetch_related('job_subscriptions').filter(employer_id=employer.id)
        for link in employer_links:
            if not link.job_subscriptions.all():
                link.job_subscriptions.add(employer_subscription.id)


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0174_alter_sociallink_employer'),
    ]

    operations = [
        migrations.RunPython(
            fix_referral_links, atomic=True
        ),
    ]
