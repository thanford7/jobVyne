# Generated by Django 4.0.7 on 2023-06-02 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0160_remove_donationorganization_url_donation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='connection_donation_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jvapp.donationorganization'),
        ),
    ]