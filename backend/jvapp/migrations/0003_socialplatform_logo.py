# Generated by Django 4.0.5 on 2022-07-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0002_alter_employer_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialplatform',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos'),
        ),
    ]
