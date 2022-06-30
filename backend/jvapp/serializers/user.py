from jvapp.models.user import JobVineUser
from . import get_datetime_format_or_none


def get_serialized_user(user: JobVineUser):
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type_bits': user.user_type_bits,
        'is_staff': user.is_staff,
        'created_dt': get_datetime_format_or_none(user.created_dt),
        'modified_dt': get_datetime_format_or_none(user.modified_dt)
    }
