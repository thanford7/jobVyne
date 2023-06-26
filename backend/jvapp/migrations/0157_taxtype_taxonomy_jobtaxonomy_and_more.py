# Generated by Django 4.0.7 on 2023-06-03 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0156_delete_employerpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tax_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jvapp.taxtype')),
            ],
            options={
                'unique_together': {('tax_type', 'name')},
            },
        ),
        migrations.CreateModel(
            name='JobTaxonomy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField()),
                ('modified_dt', models.DateTimeField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jvapp.employerjob')),
                ('taxonomy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jvapp.taxonomy')),
            ],
        ),
        migrations.AddConstraint(
            model_name='jobtaxonomy',
            constraint=models.UniqueConstraint(fields=('job', 'taxonomy'), name='job_unique_taxonomy'),
        ),
    ]