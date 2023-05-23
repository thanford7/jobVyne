# Generated by Django 4.0.7 on 2023-05-22 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0154_alter_userdonation_donation_amount_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdonation',
            name='donation_amount_currency',
            field=models.ForeignKey(default='USD', on_delete=django.db.models.deletion.PROTECT, to='jvapp.currency', to_field='name'),
        ),
    ]
