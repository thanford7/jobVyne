# Generated by Django 4.0.7 on 2022-09-23 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0069_jobvyneuser_is_employer_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='billing_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='street_address',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='street_address_2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='stripe_customer_key',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]