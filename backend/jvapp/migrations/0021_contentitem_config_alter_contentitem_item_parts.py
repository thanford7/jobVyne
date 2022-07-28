# Generated by Django 4.0.5 on 2022-07-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0020_add_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentitem',
            name='config',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='item_parts',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
