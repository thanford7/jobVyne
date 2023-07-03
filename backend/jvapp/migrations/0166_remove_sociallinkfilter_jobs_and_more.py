# Generated by Django 4.2.1 on 2023-06-07 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0165_jobsubscription_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sociallinkfilter',
            name='jobs',
        ),
        migrations.RemoveField(
            model_name='sociallinkfilter',
            name='remote_type_bit',
        ),
        migrations.AddField(
            model_name='sociallinkfilter',
            name='job_subscriptions',
            field=models.ManyToManyField(to='jvapp.jobsubscription'),
        ),
    ]