from jvapp.models.user import JobVyneUser
from jvapp.serializers.job_seeker import base_application_serializer
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_user(user: JobVyneUser):
    application_template = next((at for at in user.application_template.all()), None)
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type_bits': user.user_type_bits,
        'employer_id': user.employer_id,
        'is_employer_deactivated': user.is_employer_deactivated,
        'created_dt': get_datetime_format_or_none(user.created_dt),
        'modified_dt': get_datetime_format_or_none(user.modified_dt),
        'application_template': base_application_serializer(application_template) if application_template else None,
        'permissions': list(user.permissions.keys()),
        'permission_groups': [{
            'id': pg.id,
            'name': pg.name,
            'user_type_bit': pg.user_type_bit,
            'employer_id': pg.employer_id
        } for pg in user.permission_groups.all()]
    }
