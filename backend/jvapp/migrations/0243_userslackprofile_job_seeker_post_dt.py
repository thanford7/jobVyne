# Generated by Django 4.2.1 on 2023-08-29 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0242_userslackprofile_team_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userslackprofile',
            name='job_seeker_post_dt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
