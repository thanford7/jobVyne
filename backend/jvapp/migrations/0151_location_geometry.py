# Generated by Django 4.0.7 on 2023-05-21 23:07

from django.contrib.gis.geos import Point
from django.db import migrations

from jvapp.models.location import SridGeometryField


def lon_lat_to_geom(apps, _):
    Location = apps.get_model('jvapp', 'Location')
    to_update = Location.objects.filter(latitude__isnull=False, longitude__isnull=False)
    for location in to_update:
        lon, lat = map(float, (location.longitude, location.latitude))
        location.geometry = Point(lat, lon, srid=4326)
    Location.objects.bulk_update(to_update, fields=('geometry',))


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0150_employer_days_after_hire_payout'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='geometry',
            field=SridGeometryField(null=True, srid=4326),
        ),
        migrations.RunSQL(
            'alter table jvapp_location modify column geometry geometry srid 4326',
            reverse_sql='',
        ),
        migrations.RunPython(
            code=lon_lat_to_geom, reverse_code=lambda *args: None,
        ),
    ]
