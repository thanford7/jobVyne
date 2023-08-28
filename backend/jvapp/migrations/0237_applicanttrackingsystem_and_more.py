# Generated by Django 4.2.1 on 2023-08-26 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0236_employerslack_modal_cfg_is_salary_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantTrackingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos')),
            ],
        ),
        migrations.AddField(
            model_name='employer',
            name='applicant_tracking_system',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jvapp.applicanttrackingsystem'),
        ),
    ]