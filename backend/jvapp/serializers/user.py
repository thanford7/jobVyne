import functools

from jvapp.models.user import JobVyneUser
from jvapp.serializers.job_seeker import base_application_serializer
from jvapp.utils.datetime import get_datetime_format_or_none


def reduce_user_type_bits(permission_groups):
    return functools.reduce(
        lambda user_type_bits, group: group.user_type_bit | user_type_bits,
        permission_groups, 0
    )


def get_serialized_user(user: JobVyneUser, isIncludePersonalInfo=False):
    data = {
        'id': user.id,
        'profile_picture_url': user.profile_picture.url if user.profile_picture else None,
        'email': user.email,
        'business_email': user.business_email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type_bits': user.user_type_bits,
        'employer_id': user.employer_id,
        'is_employer_deactivated': user.is_employer_deactivated,
        'created_dt': get_datetime_format_or_none(user.created_dt),
        'modified_dt': get_datetime_format_or_none(user.modified_dt),
        'permissions_by_employer': {
            employer_id: [p.name for p in permissions]
            for employer_id, permissions in user.permissions_by_employer.items()
        },
        'permission_groups_by_employer': {
            employer_id: [{
                'id': pg.id,
                'name': pg.name,
                'user_type_bit': pg.user_type_bit
            } for pg in permission_groups]
            for employer_id, permission_groups in user.permission_groups_by_employer.items()
        },
        'user_type_bits_by_employer': {
            employer_id: reduce_user_type_bits(permission_groups)
            for employer_id, permission_groups in user.permission_groups_by_employer.items()
        }
    }
    
    if isIncludePersonalInfo:
        application_template = next((at for at in user.application_template.all()), None)
        data['application_template'] = base_application_serializer(application_template) if application_template else None
        data['is_email_verified'] = user.is_email_verified
        data['is_email_employer_permitted'] = user.is_email_employer_permitted
        data['is_business_email_verified'] = user.is_business_email_verified
        data['is_business_email_employer_permitted'] = user.is_business_email_employer_permitted
        data['is_employer_verified'] = user.is_employer_verified
        
    return data
