import json
import re

import requests
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
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


def get_raw_location(location_text, is_best_result=True, zip_code=None):
    params = {'address': location_text, 'key': settings.GOOGLE_MAPS_KEY}
    if zip_code:
        params['components'] = f'postal_code:{zip_code}'
    resp = requests.get(BASE_URL, params=params)
    raw_data = json.loads(resp.content)
    return parse_location_resp(raw_data, is_best_result=is_best_result), raw_data


def get_raw_location_from_latlong(latitude, longitude, is_best_result=True):
    params = {'latlong': f'{latitude},{longitude}', 'key': settings.GOOGLE_MAPS_KEY}
    resp = requests.get(BASE_URL, params=params)
    raw_data = json.loads(resp.content)
    return parse_location_resp(raw_data, is_best_result=is_best_result), raw_data


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

    if is_best_result and parsed_results:
        return parsed_results[0]

    return parsed_results


def save_raw_location(location_dict: dict, is_remote: bool, raw_location_text=None, raw_data=None, is_save_location_lookup=True):
    city_name = location_dict.get('city')
    state_name = location_dict.get('state')
    country_name = location_dict.get('country')
    latitude = location_dict.get('latitude')
    latitude_text = str(latitude)[:15] if latitude else None
    longitude = location_dict.get('longitude')
    longitude_text = str(longitude)[:15] if longitude else None
    if not any([city_name, state_name, country_name]):
        if is_remote:
            try:
                location = Location.objects.get(text__iexact='Remote', is_remote=True)
            except Location.DoesNotExist:
                location = Location(
                    text='Remote',
                    is_remote=True
                )
                location.save()
        else:
            try:
                location = Location.objects.get(text__iexact='Unknown')
            except Location.DoesNotExist:
                location = Location(
                    text='Unknown',
                    is_remote=False
                )
                location.save()
    else:
        location_filter = (
                Q(is_remote=is_remote, text__iexact=location_dict['text']) |
                Q(is_remote=is_remote, latitude=latitude_text, longitude=longitude_text)
        )
        locations = Location.objects.filter(location_filter)
        if locations:
            location = locations[0]
        else:
            location = Location(
                text=location_dict['text'],
                is_remote=is_remote,
                city=get_or_create_city(location_dict.get('city')),
                state=get_or_create_state(location_dict.get('state')),
                country=get_or_create_country(location_dict.get('country')),
                postal_code=location_dict.get('postal_code'),
                latitude=latitude_text,
                longitude=longitude_text,
                geometry=Location.get_geometry_point(latitude, longitude)
            )
            try:
                location.save()
            except IntegrityError as e:
                raise e
    
    if is_save_location_lookup and raw_location_text:
        raw_text = raw_location_text[:200]
        try:
            LocationLookup(
                text=raw_text,
                location=location,
                raw_result=raw_data
            ).save()
        except IntegrityError:
            location_lookup = LocationLookup.objects.get(text=raw_text)
            location_lookup.location = location
            location_lookup.raw_result = raw_data
            location_lookup.save()
    
    return location


class LocationParser:
    
    def __init__(self, is_use_location_caching=True):
        self.is_use_location_caching = is_use_location_caching
        self.location_lookups = {}
        if is_use_location_caching:
            self.location_lookups = {l.text.lower(): l.location for l in LocationLookup.objects.select_related('location').all()}

    def get_location(self, location_text, is_zip_code=False):
        location_text = location_text.lower()
        is_remote = bool(re.match('^.*?(remote|anywhere|virtual).*?$', location_text, re.IGNORECASE))
        if location := self.location_lookups.get(location_text):
            if location.is_remote == is_remote:
                return location
        
        address = re.sub('remote|anywhere|virtual|:', '', location_text, flags=re.IGNORECASE).strip()
        zip_code = None
        if is_zip_code:
            zip_code = address
        location, raw_data = get_raw_location(address, zip_code=zip_code)
        location = location or {}
        location = save_raw_location(location, is_remote, raw_location_text=location_text, raw_data=raw_data, is_save_location_lookup=self.is_use_location_caching)
        self.location_lookups[location_text] = location
        return location
    
    @classmethod
    def get_is_remote(cls, location_text):
        return bool(re.match('^.*?(remote|anywhere|virtual).*?$', location_text, re.IGNORECASE))
        
    
class LocationSearchView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        if not (search_text := self.query_params.get('search_text')):
            return Response(status=status.HTTP_200_OK, data=[])
        
        locations, _ = get_raw_location(search_text, is_best_result=False) or []
        return Response(status=status.HTTP_200_OK, data=locations)
    