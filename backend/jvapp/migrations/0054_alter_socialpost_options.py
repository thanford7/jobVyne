# Generated by Django 4.0.5 on 2022-08-29 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0053_alter_socialpost_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialpost',
            options={'ordering': ('-created_dt',)},
        ),
    ]
