# Generated by Django 4.0.5 on 2022-08-11 22:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_currencies(apps, schema_editor):
    Currency = apps.get_model('jvapp', 'Currency')
    currencies_to_create = []
    for name, symbol in [
        ('USD', '$'),
        ('CAD', '$'),  # Canada
        ('EUR', '€'),  # Euro
        ('GBP', '£'),  # UK
        ('AED', 'د.إ'),  # UAE
        ('ARS', '$'),  # Argentina
        ('AUD', '$'),  # Australia
        ('BRL', 'R$'),  # Brazil
        ('CHF', 'Fr.'),  # Switzerland
        ('CLP', '$'),  # Chile
        ('CNY', '¥'),  # China
        ('COP', '$'),  # Colombia
        ('CZK', 'Kč'),  # Czech Republic
        ('DKK', 'kr'),  # Denmark
        ('HKD', '$'),  # Hong Kong
        ('HRK', 'kn'),  # Croatia
        ('HUF', 'Ft'),  # Hungary
        ('IDR', 'Rp'),  # Indonesia
        ('ILS', '₪'),  # Israel
        ('INR', '₹'),  # India
        ('ISK', 'kr'),  # Iceland
        ('JPY', '¥'),  # Japan
        ('KRW', '₩'),  # South Korea
        ('MXN', '$'),  # Mexico
        ('MYR', 'RM'),  # Malaysia
        ('NOK', 'kr'),  # Norway
        ('NZD', '$'),  # New Zealand
        ('PEN', 'S/.'),  # Peru
        ('PHP', '₱'),  # Philippines
        ('PLN', 'zł'),  # Poland
        ('PYG', '₲'),  # Paraguay
        ('RON', 'lei'),  # Romania
        ('SAR', '﷼'),  # Saudi Arabia
        ('SEK', 'kr'),  # Sweden
        ('SGD', '$'),  # Singapore
        ('THB', '฿'),  # Thailand
        ('TRY', '₺'),  # Turkey
        ('TWD', '$'),  # Taiwan
        ('UAH', '₴'),  # Ukraine
        ('UYU', '$'),  # Uruguay
        ('VND', '₫'),  # Vietnam
        ('ZAR', 'R'),  # South Africa
    ]:
        currencies_to_create.append(Currency(name=name, symbol=symbol))
        
    Currency.objects.bulk_create(currencies_to_create)


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0034_rename_napme_city_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('symbol', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='EmployerReferralBonusRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField()),
                ('modified_dt', models.DateTimeField()),
                ('include_job_titles_regex', models.CharField(blank=True, max_length=500, null=True)),
                ('exclude_job_titles_regex', models.CharField(blank=True, max_length=500, null=True)),
                ('base_bonus_amount', models.FloatField()),
                ('bonus_currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jvapp.currency')),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_user', to=settings.AUTH_USER_MODEL)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='referral_bonus_rule', to='jvapp.employer')),
                ('exclude_cities', models.ManyToManyField(related_name='exclude_bonus', to='jvapp.city')),
                ('exclude_countries', models.ManyToManyField(related_name='exclude_bonus', to='jvapp.country')),
                ('exclude_departments', models.ManyToManyField(related_name='exclude_bonus', to='jvapp.jobdepartment')),
                ('exclude_states', models.ManyToManyField(related_name='exclude_bonus', to='jvapp.state')),
                ('include_cities', models.ManyToManyField(related_name='include_bonus', to='jvapp.city')),
                ('include_countries', models.ManyToManyField(related_name='include_bonus', to='jvapp.country')),
                ('include_departments', models.ManyToManyField(related_name='include_bonus', to='jvapp.jobdepartment')),
                ('include_states', models.ManyToManyField(related_name='include_bonus', to='jvapp.state')),
                ('modified_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modified_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(create_currencies, atomic=True)
    ]
