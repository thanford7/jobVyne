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
    if is_best_result:
        results = results[:1]

    parsed_results = []
    for result in results:
        address = result['address_components']
        location_data = {
            'formatted_address': result['formatted_address']
        }
        for component in address:
            val = component['long_name']
            short_val = component['short_name']
            comp_types = component['types']
            if 'locality' in comp_types:
                location_data['city'] = val
            elif 'administrative_area_level_1' in comp_types:
                location_data['state'] = val
            elif 'country' in comp_types:
                location_data['country'] = val
                location_data['country_short'] = short_val
            elif 'postal_code' in comp_types:
                location_data['postal_code'] = val
        lat_long = result['geometry']['location']
        location_data['latitude'] = lat_long['lat']
        location_data['longitude'] = lat_long['lng']
        parsed_results.append(location_data)

    if is_best_result:
        return parsed_results[0]

    return parsed_results


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
        city_name = data.get('city')
        state_name = data.get('state')
        country_name = data.get('country')
        if not any([city_name, state_name, country_name]):
            try:
                location = Location.objects.get(text__iexact=location_text)
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
                    city__name=city_name,
                    state__name=state_name,
                    country__name=country_name
                )
            except Location.DoesNotExist:
                latitude = data.get('latitude')
                longitude = data.get('longitude')
                location = Location(
                    text=location_text,
                    is_remote=is_remote,
                    city=get_or_create_city(data.get('city')),
                    state=get_or_create_state(data.get('state')),
                    country=get_or_create_country(data.get('country')),
                    latitude=str(latitude)[:15] if latitude else None,
                    longitude=str(longitude)[:15] if longitude else None
                )
                location.save()
        
        try:
            LocationLookup(
                text=location_text,
                location=location,
                raw_result=raw_data
            ).save()
        except IntegrityError:
            pass
        
        self.location_lookups[location_text] = location
        return location
    
    
class LocationSearchView(JobVyneAPIView):
    
    def get(self, request):
        if not (search_text := self.query_params.get('search_text')):
            return Response(status=status.HTTP_200_OK, data=[])
        
        locations = get_raw_location(search_text, is_best_result=False) or []
        return Response(status=status.HTTP_200_OK, data=locations)
    