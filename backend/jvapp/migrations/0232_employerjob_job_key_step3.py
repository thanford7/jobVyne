# Generated by Django 4.2.1 on 2023-08-18 21:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0231_employerjob_job_key_step2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerjob',
            name='job_key',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
        ),
    ]