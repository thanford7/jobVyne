from jvapp.models import Location


def get_serialized_location(location: Location):
    return {
        'id': location.id,
        'is_remote': location.is_remote,
        'text': location.text,
        'city': location.city.name if location.city else None,
        'city_id': location.city_id,
        'state': location.state.name if location.state else None,
        'state_id': location.state_id,
        'country': location.country.name if location.country else None,
        'country_id': location.country_id
    }
