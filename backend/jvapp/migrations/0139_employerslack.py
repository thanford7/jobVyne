# Generated by Django 4.0.7 on 2023-04-20 21:05

from django.db import migrations, models
import django.db.models.deletion
import jvapp.models.abstract


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0138_message_external_message_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployerSlack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oauth_key', models.CharField(max_length=75, unique=True)),
                ('is_enabled', models.BooleanField(default=True)),
                ('jobs_post_channel', models.CharField(blank=True, max_length=75, null=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_cfg', to='jvapp.employer', unique=True)),
            ],
            bases=(models.Model, jvapp.models.abstract.JobVynePermissionsMixin),
        ),
    ]