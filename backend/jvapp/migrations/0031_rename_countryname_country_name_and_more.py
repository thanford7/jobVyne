# Generated by Django 4.0.5 on 2022-08-11 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0030_alter_employerjob_unique_together_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='countryName',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='closeDate',
            new_name='close_date',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='isFullTime',
            new_name='is_full_time',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='jobDepartment',
            new_name='job_department',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='jobDescription',
            new_name='job_description',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='jobTitle',
            new_name='job_title',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='openDate',
            new_name='open_date',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='referralBonus',
            new_name='referral_bonus',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='salaryCeiling',
            new_name='salary_ceiling',
        ),
        migrations.RenameField(
            model_name='employerjob',
            old_name='salaryFloor',
            new_name='salary_floor',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='stateName',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='employerjob',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employer_job', to='jvapp.employer'),
        ),
    ]
