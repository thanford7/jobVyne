# Generated by Django 4.0.7 on 2022-12-20 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0099_jobapplication_feedback_know_applicant_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobapplication',
            old_name='feedback_notes',
            new_name='feedback_note',
        ),
    ]
