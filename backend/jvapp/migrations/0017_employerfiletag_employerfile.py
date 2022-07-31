# Generated by Django 4.0.5 on 2022-07-25 20:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jvapp.models._customDjangoField
import jvapp.models.employer


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0016_remove_pageview_filter_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployerFileTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', jvapp.models._customDjangoField.LowercaseCharField(max_length=100)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_tag', to='jvapp.employer')),
            ],
            options={
                'unique_together': {('employer', 'name')},
            },
        ),
        migrations.CreateModel(
            name='EmployerFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField()),
                ('modified_dt', models.DateTimeField()),
                ('file', models.FileField(upload_to=jvapp.models.employer.getEmployerUploadLocation, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'gif', 'mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg', 'webm', 'doc', 'docx', 'pdf', 'pages', 'gdoc'])])),
                ('title', models.CharField(max_length=100)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='jvapp.employer')),
                ('tags', models.ManyToManyField(to='jvapp.employerfiletag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]