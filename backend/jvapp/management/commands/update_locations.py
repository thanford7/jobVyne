from django.core.management import BaseCommand

from jvapp.apis.geocoding import get_raw_location, parse_location_resp
from jvapp.models.location import Location, LocationLookup


class Command(BaseCommand):
    help = 'Update postal code and text for all locations'
    
    def handle(self, *args, **options):
        writer = self.stdout.write
        raw_locations = {l.text: parse_location_resp(l.raw_result) for l in LocationLookup.objects.all()}
        locations = Location.objects.all()
        locations_to_update = []
        writer('Starting location update')
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
                writer(f'({idx}) 1000 locations updated')
                Location.objects.bulk_update(locations_to_update, ['postal_code'])
                locations_to_update = []
        if locations_to_update:
            Location.objects.bulk_update(locations_to_update, ['postal_code', 'text'])
        writer('Finished location update')
