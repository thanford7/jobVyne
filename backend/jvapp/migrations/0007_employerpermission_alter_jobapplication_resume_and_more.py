# Generated by Django 4.0.5 on 2022-07-13 03:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jvapp.models.job_seeker


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0006_jobapplicationtemplate_jobapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployerPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='resume',
            field=models.FileField(upload_to=jvapp.models.job_seeker.get_user_upload_location, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'pages', 'gdoc'])]),
        ),
        migrations.AlterField(
            model_name='jobapplicationtemplate',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_template', to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='jobapplicationtemplate',
            name='resume',
            field=models.FileField(upload_to=jvapp.models.job_seeker.get_user_upload_location, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'pages', 'gdoc'])]),
        ),
        migrations.AlterField(
            model_name='jobvyneuser',
            name='employer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee', to='jvapp.employer'),
        ),
        migrations.CreateModel(
            name='EmployerAuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('is_default', models.BooleanField(default=False)),
                ('permissions', models.ManyToManyField(to='jvapp.employerpermission')),
            ],
        ),
    ]
