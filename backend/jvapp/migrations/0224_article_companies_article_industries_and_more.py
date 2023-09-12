# Generated by Django 4.2.1 on 2023-08-16 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0223_merge_20230816_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='companies',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='industries',
            field=models.ManyToManyField(related_name='industry_articles', to='jvapp.taxonomy'),
        ),
        migrations.AlterField(
            model_name='article',
            name='professions',
            field=models.ManyToManyField(related_name='profession_articles', to='jvapp.taxonomy'),
        ),
    ]
