# Generated by Django 4.0.5 on 2022-08-23 20:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0047_usersocialcredential_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialContentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_content_item', to='jvapp.employer')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_content_item', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]