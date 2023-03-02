from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import JobDepartment, Location
from jvapp.serializers.location import get_serialized_location


class JobDepartmentView(JobVyneAPIView):
    
    def get(self, request):
        JobDepartment.objects.all()
        return Response(status=status.HTTP_200_OK, data=[
            {'id': jd.id, 'name': jd.name} for jd in JobDepartment.objects.all()
        ])
    
    
class LocationView(JobVyneAPIView):
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=self.get_serialized_locations(self.get_locations()))
    
    @staticmethod
    def get_locations():
        return Location.objects.select_related('city', 'state', 'country').all()
    
    @staticmethod
    def get_serialized_locations(location_objects):
        cities, states, countries, locations = {}, {}, {}, {}
        for location in location_objects:
            if not locations.get(location.id):
                locations[location.id] = get_serialized_location(location)
            if location.city and not cities.get(location.city_id):
                cities[location.city_id] = {'name': location.city.name, 'id': location.city.id}
            if location.state and not states.get(location.state_id):
                states[location.state_id] = {'name': location.state.name, 'id': location.state.id}
            if location.country and not countries.get(location.country_id):
                countries[location.country_id] = {'name': location.country.name, 'id': location.country.id}

        return {
            'locations': sorted(list(locations.values()), key=lambda x: (x['is_remote'] or 0, x['city'] or '')),
            'cities': sorted(list(cities.values()), key=lambda x: x['name']),
            'states': sorted(list(states.values()), key=lambda x: x['name']),
            'countries': sorted(list(countries.values()), key=lambda x: x['name'])
        }
