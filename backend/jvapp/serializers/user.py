import functools
from string import Template

from jvapp.models.user import JobVyneUser, UserFile
from jvapp.serializers.job_seeker import base_application_serializer
from jvapp.serializers.location import get_serialized_location
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.oauth import OauthProviders


def reduce_user_type_bits(permission_groups):
    return functools.reduce(
        lambda user_type_bits, group: group.user_type_bit | user_type_bits,
        permission_groups, 0
    )


def get_serialized_user(user: JobVyneUser, is_include_employer_info=False, is_include_personal_info=False):
    data = get_serialized_user_profile(user, is_get_profile=True)
    
    if is_include_employer_info:
        data['email'] = user.email
        data['business_email'] = user.business_email
        data['user_type_bits'] = user.user_type_bits
        data['employer_id'] = user.employer_id
        data['employer_name'] = user.employer.employer_name if user.employer else None
        data['employer_org_type'] = user.employer.organization_type if user.employer else 0
        data['is_employer_deactivated'] = user.is_employer_deactivated
        data['has_employee_seat'] = user.has_employee_seat
        data['created_dt'] = get_datetime_format_or_none(user.created_dt)
        data['modified_dt'] = get_datetime_format_or_none(user.modified_dt)
        
        data['is_approval_required'] = user.is_approval_required
        approved_permission_groups = [p for p in user.employer_permission_group.all() if p.is_employer_approved]
        data['permissions_by_employer'] = {
            employer_id: [p.name for p in permissions]
            for employer_id, permissions in
            user.get_permissions_by_employer(permission_groups=approved_permission_groups).items()
        }
        data['permission_groups_by_employer'] = {
            employer_id: [{
                'id': epg.permission_group.id,
                'name': epg.permission_group.name,
                'user_type_bit': epg.permission_group.user_type_bit,
                'is_approved': epg.is_employer_approved,
                'employer_name': epg.employer.employer_name
            } for epg in employer_permission_groups]
            for employer_id, employer_permission_groups in user.get_employer_permission_groups_by_employer(
                permission_groups=user.employer_permission_group.all()).items()
        }
        data['user_type_bits_by_employer'] = {
            employer_id: reduce_user_type_bits([epg.permission_group for epg in employer_permission_groups])
            for employer_id, employer_permission_groups in
            user.get_employer_permission_groups_by_employer(permission_groups=approved_permission_groups).items()
        }
    
    if is_include_personal_info:
        application_template = next((at for at in user.application_template.all()), None)
        data['application_template'] = base_application_serializer(
            application_template) if application_template else None
        data['is_email_verified'] = user.is_email_verified
        data['is_email_employer_permitted'] = user.is_email_employer_permitted
        data['is_business_email_verified'] = user.is_business_email_verified
        data['is_business_email_employer_permitted'] = user.is_business_email_employer_permitted
        data['is_employer_verified'] = user.is_employer_verified
        data['connected_emails'] = [
            cred.email for cred in user.social_credential.all() if
            (cred.provider == OauthProviders.google.value) and cred.refresh_token
        ]
    
    return data


def get_serialized_user_profile(user: JobVyneUser, is_get_profile=False):
    data = {
        'id': user.id,
        'profile_picture_url': user.profile_picture.url if user.profile_picture else None,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'job_title': user.job_title,
        'profession_id': user.profession.id if user.profession else None,
        'profession_name': user.profession.name if user.profession else None,
        'employment_start_date': user.employment_start_date,
        'home_location': get_serialized_location(user.home_location) if user.home_location else None,
        'is_profile_viewable': user.is_profile_viewable
    }
    
    if (is_get_profile or user.is_profile_viewable) and user.employer:
        data['profile_responses'] = [
            {
                'question_id': response.question_id,
                'question': Template(response.question.text).substitute(employer_name=user.employer.employer_name),
                'response': response.answer
            } for response in user.profile_response.all()
        ]
    
    return data


def get_serialized_user_file(user_file: UserFile):
    return {
        'id': user_file.id,
        'user_id': user_file.user_id,
        'url': user_file.file.url,
        'title': user_file.title
    }
