# Generated by Django 4.2.1 on 2023-07-09 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0198_pageview_employer_pageview_page_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referral', to=settings.AUTH_USER_MODEL),
        ),
    ]
