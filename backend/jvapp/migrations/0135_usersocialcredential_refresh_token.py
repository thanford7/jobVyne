# Generated by Django 4.0.7 on 2023-04-04 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0134_alter_userapplicationreview_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersocialcredential',
            name='refresh_token',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
