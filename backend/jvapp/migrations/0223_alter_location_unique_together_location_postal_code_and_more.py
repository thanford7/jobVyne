# Generated by Django 4.2.1 on 2023-08-11 22:00
from collections import defaultdict

from django.db import migrations, models
import django.db.models.functions.text

from jvapp.apis.geocoding import get_raw_location, get_raw_location_from_latlong, parse_location_resp
from jvapp.models import JobVyneUser
from jvapp.models.employer import EmployerJob
from jvapp.models.job_subscription import JobSubscription
from jvapp.models.location import Location, LocationLookup


def dedup_location_groups(grouped_locations):
    for location_group in grouped_locations.values():
        if len(location_group) == 1:
            continue
        location_group.sort(key=lambda x: (x.city_id or 0, x.state_id or 0), reverse=True)
        keep_location = location_group[0]
        locations_to_delete = location_group[1:]
        for location in locations_to_delete:
            jobs = EmployerJob.objects.filter(locations__in=[location])
            for job in jobs:
                job.locations.add(keep_location)
            job_subscriptions = JobSubscription.objects.filter(filter_location__in=[location])
            for sub in job_subscriptions:
                sub.filter_location.add(keep_location)
            users = JobVyneUser.objects.filter(home_location=location)
            for user in users:
                user.home_location = keep_location
                user.save()
            location.delete()


def remove_duplicate_locations(apps, schema_editor):
    # Dedup locations for each unique constraint
    locations = Location.objects.all()
    grouped_locations = defaultdict(list)
    for location in locations:
        grouped_locations[(location.text.lower(), location.is_remote)].append(location)
    dedup_location_groups(grouped_locations)
    
    locations = Location.objects.all()
    grouped_locations = defaultdict(list)
    for location in locations:
        grouped_locations[(location.latitude, location.longitude, location.is_remote)].append(location)
    dedup_location_groups(grouped_locations)
    
    
def update_locations(apps, schema_editor):
    raw_locations = {l.text: parse_location_resp(l.raw_result) for l in LocationLookup.objects.all()}
    locations = Location.objects.all()
    locations_to_update = []
    for idx, location in enumerate(locations):
        raw_location = raw_locations.get(location.text) or {}
        if postal_code := raw_location.get('postal_code'):
            location.postal_code = postal_code
            location.text = raw_location['text']
        else:
            location_data, _ = get_raw_location(location.text)
            location_data = location_data or {}
            postal_code = location_data.get('postal_code')
            city = location_data.get('city')
            if postal_code and city:
                location.postal_code = postal_code
            if location_text := location_data.get('text'):
                location.text = location_text
        
        locations_to_update.append(location)
        if idx and (idx % 1000 == 0):
            Location.objects.bulk_update(locations_to_update, ['postal_code'])
            locations_to_update = []
    if locations_to_update:
        Location.objects.bulk_update(locations_to_update, ['postal_code', 'text'])


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0222_alter_employerjob_is_job_approved'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='location',
            name='postal_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='text',
            field=models.CharField(default='unknown', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='is_remote',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(remove_duplicate_locations, atomic=True),
        migrations.AddConstraint(
            model_name='location',
            constraint=models.UniqueConstraint(models.F('is_remote'), django.db.models.functions.text.Lower('text'),
                                               name='unique_location'),
        ),
        migrations.AddConstraint(
            model_name='location',
            constraint=models.UniqueConstraint(fields=('is_remote', 'latitude', 'longitude'), name='unique_latlong'),
        ),
        migrations.RunPython(update_locations, atomic=True)
    ]
