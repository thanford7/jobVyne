# Generated by Django 4.0.7 on 2023-04-06 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0136_alter_useremployercandidate_ats_candidate_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagethread',
            name='external_thread_key',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
