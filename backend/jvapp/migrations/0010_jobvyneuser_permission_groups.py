# Generated by Django 4.0.5 on 2022-07-14 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0008_employerauthgroup_employer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobvyneuser',
            name='permission_groups',
            field=models.ManyToManyField(related_name='user', to='jvapp.employerauthgroup'),
        ),
    ]