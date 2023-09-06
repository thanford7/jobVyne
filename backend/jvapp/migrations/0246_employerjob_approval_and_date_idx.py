# Generated by Django 4.2.1 on 2023-09-01 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0245_alter_taxonomy_name'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='employerjob',
            index=models.Index(models.F('is_job_approved'), models.F('close_date'), models.F('open_date'), name='approval_and_date_idx'),
        ),
    ]