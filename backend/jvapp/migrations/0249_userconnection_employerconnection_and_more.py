# Generated by Django 4.2.1 on 2023-09-02 23:18

from django.conf import settings
from django.db import IntegrityError, migrations, models
import django.db.models.deletion

from jvapp.models.employer import ConnectionTypeBit, EmployerConnection, EmployerJobConnection


def add_employer_connections(apps, schema_editor):
    job_connections = EmployerJobConnection.objects.select_related('job').all()
    for job_connection in job_connections:
        employer_connection = EmployerConnection(
            user=job_connection.user,
            employer_id=job_connection.job.employer_id,
            connection_type=job_connection.connection_type,
            is_allow_contact=job_connection.is_allow_contact
        )
        try:
            employer_connection.save()
        except IntegrityError:
            employer_connection = EmployerConnection.objects.get(
                user=job_connection.user,
                employer_id=job_connection.job.employer_id,
                connection_type=job_connection.connection_type
            )
        if employer_connection.connection_type == ConnectionTypeBit.HIRING_MEMBER.value:
            employer_connection.hiring_jobs.add(job_connection.job)


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0248_jobvyneuser_user_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField()),
                ('modified_dt', models.DateTimeField()),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('linkedin_handle', models.CharField(blank=True, max_length=100, null=True)),
                ('employer_raw', models.CharField(blank=True, max_length=200, null=True)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('connection_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_connection', to=settings.AUTH_USER_MODEL)),
                ('employer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='connection', to='jvapp.employer')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_connection', to=settings.AUTH_USER_MODEL)),
                ('profession', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jvapp.taxonomy')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField()),
                ('modified_dt', models.DateTimeField()),
                ('connection_type', models.SmallIntegerField()),
                ('is_allow_contact', models.BooleanField()),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_connection', to='jvapp.employer')),
                ('hiring_jobs', models.ManyToManyField(to='jvapp.employerjob')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer_connection', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='userconnection',
            constraint=models.UniqueConstraint(condition=models.Q(('connection_user__isnull', False)), fields=('owner', 'connection_user', 'employer_raw'), name='unique_user_connection'),
        ),
        migrations.AddConstraint(
            model_name='userconnection',
            constraint=models.UniqueConstraint(fields=('owner', 'first_name', 'last_name', 'employer_raw'), name='unique_user_connection_name'),
        ),
        migrations.AddConstraint(
            model_name='userconnection',
            constraint=models.UniqueConstraint(condition=models.Q(('email__isnull', False)), fields=('owner', 'email', 'employer_raw'), name='unique_user_connection_email'),
        ),
        migrations.AddConstraint(
            model_name='userconnection',
            constraint=models.UniqueConstraint(fields=('owner', 'linkedin_handle', 'employer_raw'), name='unique_user_connection_linkedin'),
        ),
        migrations.AddConstraint(
            model_name='employerconnection',
            constraint=models.UniqueConstraint(fields=('user', 'employer', 'connection_type'), name='unique_employer_connection'),
        ),
        migrations.RunPython(add_employer_connections, atomic=False)
    ]