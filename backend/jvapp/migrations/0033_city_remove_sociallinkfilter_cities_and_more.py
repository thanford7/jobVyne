# Generated by Django 4.0.5 on 2022-08-11 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0032_alter_sociallinkfilter_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('napme', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sociallinkfilter',
            name='cities',
        ),
        migrations.RemoveField(
            model_name='location',
            name='city',
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jvapp.city'),
        ),
        migrations.AddField(
            model_name='sociallinkfilter',
            name='cities',
            field=models.ManyToManyField(to='jvapp.city'),
        ),
    ]