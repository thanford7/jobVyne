# Generated by Django 4.0.7 on 2023-01-15 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0104_salesinquiry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerats',
            name='access_token',
            field=models.CharField(blank=True, max_length=1400, null=True),
        ),
        migrations.AddField(
            model_name='employerats',
            name='access_token_expire_dt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employerats',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=1400, null=True),
        ),
        migrations.AddField(
            model_name='employerats',
            name='refresh_token_expire_dt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employerats',
            name='api_key',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employerats',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]