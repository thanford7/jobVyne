from jvapp.models.employer import *
from jvapp.models.employer import is_default_auth_group
from jvapp.serializers.content import get_serialized_content_item
from jvapp.serializers.user import reduce_user_type_bits
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_employer(employer: Employer, is_include_employees: bool = False):
    data = {
        'id': employer.id,
        'name': employer.employer_name,
        'logo_url': employer.logo.url if employer.logo else None,
        'size': employer.employer_size.size if employer.employer_size else None,
        'email_domains': employer.email_domains,
        'color_primary': employer.color_primary,
        'color_secondary': employer.color_secondary,
        'color_accent': employer.color_accent
    }
    
    def get_permission_groups(employee):
        return [
            p.permission_group
            for p in employee.get_employer_permission_groups_by_employer(True)[employer.id]
        ]
    
    if is_include_employees:
        data['employees'] = [{
            'id': e.id,
            'email': e.email,
            'first_name': e.first_name,
            'last_name': e.last_name,
            'user_type_bits': reduce_user_type_bits(get_permission_groups(e)),
            'is_employer_deactivated': e.is_employer_deactivated,
            'permission_groups': [{
                'id': epg.permission_group.id,
                'name': epg.permission_group.name,
                'user_type_bit': epg.permission_group.user_type_bit,
                'is_approved': epg.is_employer_approved
            } for epg in e.get_employer_permission_groups_by_employer(True)[employer.id]],
            'created_dt': get_datetime_format_or_none(e.created_dt),
        } for e in employer.employee.all().order_by('-id')]
    
    return data


def get_serialized_employer_job(employer_job: EmployerJob):
    return {
        'id': employer_job.id,
        'employer_id': employer_job.employer_id,
        'job_title': employer_job.jobTitle,
        'job_description': employer_job.jobDescription,
        'job_department': employer_job.jobDepartment.name if employer_job.jobDepartment else None,
        'job_department_id': employer_job.jobDepartment_id,
        'open_date': get_datetime_format_or_none(employer_job.openDate),
        'close_date': get_datetime_format_or_none(employer_job.closeDate),
        'salary_floor': employer_job.salaryFloor,
        'salary_ceiling': employer_job.salaryCeiling,
        'referral_bonus': employer_job.referralBonus,
        'is_full_time': employer_job.isFullTime,
        'is_remote': employer_job.isRemote,
        'location': employer_job.location,
        'city': employer_job.city,
        'state': employer_job.state.stateName,
        'state_id': employer_job.state_id,
        'country': employer_job.country.countryName,
        'country_id': employer_job.country_id
    }


def get_serialized_auth_group(auth_group: EmployerAuthGroup, all_permissions, auth_groups, user):
    employer_permissions = {ag.id: ag for ag in auth_group.permissions.all()}
    return {
        'id': auth_group.id,
        'name': auth_group.name,
        'is_default': is_default_auth_group(auth_group, auth_groups),
        'employer_id': auth_group.employer_id,
        'user_type_bit': auth_group.user_type_bit,
        'can_edit': auth_group.jv_can_update_permissions(user),
        'permissions': [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'user_type_bits': p.user_type_bits,
            'is_permitted': p.id in employer_permissions
        } for p in all_permissions]
    }


def get_serialized_employer_file(employer_file: EmployerFile):
    return {
        'id': employer_file.id,
        'employer_id': employer_file.employer_id,
        'url': employer_file.file.url,
        'title': employer_file.title,
        'tags': [get_serialized_employer_file_tag(t) for t in employer_file.tags.all()]
    }


def get_serialized_employer_file_tag(tag: EmployerFileTag):
    return {
        'id': tag.id,
        'employer_id': tag.employer_id,
        'name': tag.name
    }


def get_serialized_employer_page(page: EmployerPage):
    return {
        'id': page.id,
        'employer_id': page.employer_id,
        'is_viewable': page.is_viewable,
        'sections': [
            get_serialized_content_item(ci) for ci in page.content_item.all()
        ]
    }
