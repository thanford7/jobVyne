# Generated by Django 4.2.1 on 2023-08-28 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0240_alter_employerjob_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSlackProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_key', models.CharField(db_index=True, max_length=20, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
