# Generated by Django 4.0.7 on 2023-06-02 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0161_userrequest_connection_donation_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobvyneuser',
            name='linkedin_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]