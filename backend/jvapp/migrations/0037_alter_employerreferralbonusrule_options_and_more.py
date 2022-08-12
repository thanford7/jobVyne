# Generated by Django 4.0.5 on 2022-08-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0036_employerreferralbonusrule_order_idx_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employerreferralbonusrule',
            options={'ordering': ('employer_id', 'order_idx')},
        ),
        migrations.AlterUniqueTogether(
            name='employerreferralbonusrule',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='employerreferralbonusrule',
            name='days_after_hire_payout',
            field=models.SmallIntegerField(default=90),
            preserve_default=False,
        ),
    ]
