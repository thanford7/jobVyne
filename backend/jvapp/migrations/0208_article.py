# Generated by Django 4.2.1 on 2023-08-12 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0207_employer_description_employer_industry_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField()),
                ('modified_dt', models.DateTimeField()),
                ('source', models.CharField(max_length=40)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=1000)),
                ('professions', models.ManyToManyField(to='jvapp.taxonomy')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
