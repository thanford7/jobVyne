import functools

from jvapp.models.user import JobVyneUser, UserFile
from jvapp.serializers.job_seeker import base_application_serializer
from jvapp.serializers.location import get_serialized_location
from jvapp.utils.datetime import get_datetime_format_or_none


def reduce_user_type_bits(permission_groups):
    return functools.reduce(
        lambda user_type_bits, group: group.user_type_bit | user_type_bits,
        permission_groups, 0
    )


def get_serialized_user(user: JobVyneUser, isIncludeEmployerInfo=False, isIncludePersonalInfo=False):
    data = {
        'id': user.id,
        'profile_picture_url': user.profile_picture.url if user.profile_picture else None,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'job_title': user.job_title,
        'employment_start_date': user.employment_start_date,
        'home_location': get_serialized_location(user.home_location) if user.home_location else None
    }
    
    if isIncludeEmployerInfo:
        data['email'] = user.email
        data['business_email'] = user.business_email
        data['user_type_bits'] = user.user_type_bits
        data['employer_id'] = user.employer_id
        data['is_employer_deactivated'] = user.is_employer_deactivated
        data['created_dt'] = get_datetime_format_or_none(user.created_dt)
        data['modified_dt'] = get_datetime_format_or_none(user.modified_dt)
        
        approved_permission_groups = [p for p in user.employer_permission_group.all() if p.is_employer_approved]
        data['permissions_by_employer'] = {
            employer_id: [p.name for p in permissions]
            for employer_id, permissions in user.get_permissions_by_employer(permission_groups=approved_permission_groups).items()
        }
        data['permission_groups_by_employer'] = {
            employer_id: [{
                'id': epg.permission_group.id,
                'name': epg.permission_group.name,
                'user_type_bit': epg.permission_group.user_type_bit,
                'is_approved': epg.is_employer_approved
            } for epg in employer_permission_groups]
            for employer_id, employer_permission_groups in user.get_employer_permission_groups_by_employer(permission_groups=user.employer_permission_group.all()).items()
        }
        data['user_type_bits_by_employer'] = {
            employer_id: reduce_user_type_bits([epg.permission_group for epg in employer_permission_groups])
            for employer_id, employer_permission_groups in user.get_employer_permission_groups_by_employer(permission_groups=approved_permission_groups).items()
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


def get_serialized_user_file(user_file: UserFile):
    return {
        'id': user_file.id,
        'user_id': user_file.user_id,
        'url': user_file.file.url,
        'title': user_file.title
    }
