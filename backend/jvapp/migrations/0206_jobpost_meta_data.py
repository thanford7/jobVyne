# Generated by Django 4.2.1 on 2023-07-19 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0205_remove_employerjobconnection_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='meta_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]