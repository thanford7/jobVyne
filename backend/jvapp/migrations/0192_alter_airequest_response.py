# Generated by Django 4.0.7 on 2023-07-03 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0191_rename_prompt_tracker_employerjob_qualifications_prompt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airequest',
            name='response',
            field=models.JSONField(null=True),
        ),
    ]
