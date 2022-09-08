import json

import requests
from django.conf import settings

from jvapp.models.location import City, Country, Location, LocationLookup, State

BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


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


def get_location(location_text):
    try:
        location_lookup = LocationLookup.objects.select_related('location').get(text=location_text)
        return location_lookup.location
    except LocationLookup.DoesNotExist:
        resp = requests.get(BASE_URL, params={'address': location_text, 'key': settings.GOOGLE_MAPS_KEY})
        raw_data = json.loads(resp.content)
        data = parse_location_resp(raw_data)
        is_remote = 'remote' in location_text.lower()
        if not data:
            try:
                location = Location.objects.get(text=location_text)
            except Location.DoesNotExist:
                location = Location(
                    text=location_text,
                    is_remote=is_remote
                )
                location.save()
        else:
            try:
                location = Location.objects.get(
                    is_remote=is_remote,
                    city__name=data['city'],
                    state__name=data['state'],
                    country__name=data['country']
                )
            except Location.DoesNotExist:
                location = Location(
                    text=location_text,
                    is_remote=is_remote,
                    city=get_or_create_city(data.get('city')),
                    state=get_or_create_state(data.get('state')),
                    country=get_or_create_country(data.get('country')),
                    latitude=data.get('latitude'),
                    longitude=data.get('longitude')
                )
                location.save()
            
        LocationLookup(
            text=location_text,
            location=location,
            raw_result=raw_data
        ).save()
        return location
    

def parse_location_resp(raw_data):
    if not raw_data.get('results'):
        return None
    best_address = raw_data['results'][0] if raw_data['results'] else None
    if not best_address:
        return None
    address = best_address['address_components']
    location_data = {}
    for component in address:
        val = component['long_name']
        comp_types = component['types']
        if 'locality' in comp_types:
            location_data['city'] = val
        elif 'administrative_area_level_1' in comp_types:
            location_data['state'] = val
        elif 'country' in comp_types:
            location_data['country'] = val
    lat_long = best_address['geometry']['location']
    location_data['latitude'] = lat_long['lat']
    location_data['longitude'] = lat_long['lng']
    return location_data
    