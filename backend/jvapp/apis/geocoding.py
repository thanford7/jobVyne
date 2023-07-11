import json

import requests
from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.location import City, Country, Location, LocationLookup, State


def _get_or_create_obj(objClass, name):
    if not name:
        return None
    try:
        return objClass.objects.get(name=name)
    except objClass.DoesNotExist:
        obj = objClass(name=name)
        obj.save()
        return obj


def get_or_create_city(city_name):
    return _get_or_create_obj(City, city_name)


def get_or_create_state(state_name):
    return _get_or_create_obj(State, state_name)


def get_or_create_country(country_name):
    return _get_or_create_obj(Country, country_name)


BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


def get_raw_location(location_text, is_best_result=True):
    resp = requests.get(BASE_URL, params={'address': location_text, 'key': settings.GOOGLE_MAPS_KEY})
    raw_data = json.loads(resp.content)
    return parse_location_resp(raw_data, is_best_result=is_best_result)


def parse_location_resp(raw_data, is_best_result=True):
    results = raw_data.get('results')
    if (not results) or (not results[0]):
        return None

    parsed_results = []
    for result in results:
        address = result['address_components']
        location_data = {
            'text': result['formatted_address']
        }
        has_address_component = False
        for component in address:
            val = component['long_name']
            short_val = component['short_name']
            comp_types = component['types']
            if 'locality' in comp_types:
                location_data['city'] = val
                has_address_component = True
            elif 'administrative_area_level_1' in comp_types:
                location_data['state'] = val
                has_address_component = True
            elif 'country' in comp_types:
                location_data['country'] = val
                location_data['country_short'] = short_val
                has_address_component = True
            elif 'postal_code' in comp_types:
                location_data['postal_code'] = val
                has_address_component = True
        if not has_address_component:
            continue
        lat_long = result['geometry']['location']
        location_data['latitude'] = lat_long['lat']
        location_data['longitude'] = lat_long['lng']
        parsed_results.append(location_data)

    if is_best_result:
        return parsed_results[0]

    return parsed_results


def save_raw_location(location_dict: dict, is_remote: bool, raw_location_text=None, raw_data=None):
    city_name = location_dict.get('city')
    state_name = location_dict.get('state')
    country_name = location_dict.get('country')
    if not any([city_name, state_name, country_name]):
        try:
            location = Location.objects.get(text__iexact='Unknown')
        except Location.DoesNotExist:
            location = Location(
                text='Unknown',
                is_remote=is_remote
            )
            location.save()
    else:
        try:
            location = Location.objects.get(
                is_remote=is_remote,
                city__name=city_name,
                state__name=state_name,
                country__name=country_name
            )
        except Location.DoesNotExist:
            latitude = location_dict.get('latitude')
            longitude = location_dict.get('longitude')
            location = Location(
                text=location_dict.get('text'),
                is_remote=is_remote,
                city=get_or_create_city(location_dict.get('city')),
                state=get_or_create_state(location_dict.get('state')),
                country=get_or_create_country(location_dict.get('country')),
                latitude=str(latitude)[:15] if latitude else None,
                longitude=str(longitude)[:15] if longitude else None,
                geometry=Location.get_geometry_point(latitude, longitude)
            )
            location.save()

    try:
        LocationLookup(
            text=raw_location_text,
            location=location,
            raw_result=raw_data
        ).save()
    except IntegrityError:
        pass

    return location


class LocationParser:
    
    def __init__(self):
        self.location_lookups = {l.text.lower(): l.location for l in LocationLookup.objects.select_related('location').all()}

    def get_location(self, location_text):
        location_text = location_text.lower()
        if location := self.location_lookups.get(location_text):
            return location

        is_remote = 'remote' in location_text
        resp = requests.get(BASE_URL, params={
            'address': location_text.replace('remote', '').replace(':', '').strip(),
            'key': settings.GOOGLE_MAPS_KEY
        })
        raw_data = json.loads(resp.content)
        data = parse_location_resp(raw_data) or {}
        location = save_raw_location(data, is_remote, raw_location_text=location_text, raw_data=raw_data)
        self.location_lookups[location_text] = location
        return location
        
    
class LocationSearchView(JobVyneAPIView):
    
    def get(self, request):
        if not (search_text := self.query_params.get('search_text')):
            return Response(status=status.HTTP_200_OK, data=[])
        
        locations = get_raw_location(search_text, is_best_result=False) or []
        return Response(status=status.HTTP_200_OK, data=locations)
    