# Generated by Django 4.2.1 on 2023-08-25 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0235_jobsubscription_filter_is_salary_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerslack',
            name='modal_cfg_is_salary_required',
            field=models.BooleanField(default=False),
        ),
    ]
