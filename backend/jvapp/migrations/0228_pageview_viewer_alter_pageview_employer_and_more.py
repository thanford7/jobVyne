# Generated by Django 4.2.1 on 2023-08-16 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0227_employer_description_long_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='viewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_view', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pageview',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employer_page_view', to='jvapp.employer'),
        ),
        migrations.AlterField(
            model_name='pageview',
            name='page_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_page_view', to=settings.AUTH_USER_MODEL),
        ),
    ]