# Generated by Django 4.2.1 on 2023-09-13 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0255_merge_20230912_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUnsubscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('unsubscribe_dt', models.DateTimeField()),
            ],
        ),
    ]
