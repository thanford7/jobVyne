# Generated by Django 4.0.5 on 2022-08-04 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0027_alter_jobvyneuser_user_type_bits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobvyneuser',
            name='permission_groups',
        ),
        migrations.CreateModel(
            name='UserEmployerPermissionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jvapp.employer')),
                ('permission_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jvapp.employerauthgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer_permission_group', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'employer', 'permission_group')},
            },
        ),
    ]