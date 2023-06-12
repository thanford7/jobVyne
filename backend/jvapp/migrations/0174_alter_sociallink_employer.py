# Generated by Django 4.2.1 on 2023-06-09 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0173_add_employee_referral_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jvapp.employer'),
        ),
    ]