# Generated by Django 4.0.7 on 2023-03-09 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0126_alter_jobapplication_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerjob',
            name='job_title',
            field=models.CharField(max_length=200),
        ),
    ]
