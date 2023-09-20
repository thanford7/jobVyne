# Generated by Django 4.2.1 on 2023-07-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0209_externalcompanydata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='linkedin_url',
        ),
        migrations.AddField(
            model_name='employer',
            name='linkedin_handle',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='industry',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='ownership_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='size_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='size_min',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='year_founded',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
