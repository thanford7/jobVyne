# Generated by Django 4.2.1 on 2023-06-07 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0166_remove_sociallinkfilter_jobs_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SocialLinkFilter',
            new_name='SocialLink',
        ),
    ]
