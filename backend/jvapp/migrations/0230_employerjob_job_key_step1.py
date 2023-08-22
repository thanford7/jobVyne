# Generated by Django 4.2.1 on 2023-08-18 21:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0229_employerjob_open_date_id_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerjob',
            name='job_key',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]