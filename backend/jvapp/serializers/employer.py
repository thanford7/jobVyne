import re
from enum import Enum

from django.utils import timezone

from jvapp.models.currency import Currency
from jvapp.models.employer import *
from jvapp.models.employer import is_default_auth_group
from jvapp.models.user import JobVyneUser
from jvapp.serializers.location import get_serialized_location
from jvapp.serializers.user import reduce_user_type_bits
from jvapp.utils.data import get_list_intersection, obfuscate_string
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_currency(currency: Currency, is_allow_none=True):
    if is_allow_none and not currency:
        return {}
    
    return {
        'id': currency.id,
        'name': currency.name,
        'symbol': currency.symbol
    }


def get_serialized_employer(employer: Employer, is_employer: bool = False):
    data = {
        'id': employer.id,
        'organization_type': employer.organization_type,
        'name': employer.employer_name,
        'key': employer.employer_key,
        'description': employer.description,
        'industry': employer.industry,
        'employee_count_min': employer.size_min,
        'employee_count_max': employer.size_max,
        'year_founded': employer.year_founded,
        'logo_url': employer.logo.url if employer.logo else None,
        'logo_square_88_url': employer.logo_square_88.url if employer.logo_square_88 else None,
        'email_domains': employer.email_domains,
        'website': employer.website_domain,
        'ats_name': employer.applicant_tracking_system.name if employer.applicant_tracking_system else None,
        'is_use_job_url': employer.is_use_job_url,
        'company_jobs_page_url': employer.company_jobs_page_url,
        'color_primary': employer.color_primary,
        'color_secondary': employer.color_secondary,
        'color_accent': employer.color_accent,
        'default_bonus_amount': employer.default_bonus_amount or 0,
        'default_bonus_currency': get_serialized_currency(employer.default_bonus_currency),
        'days_after_hire_payout': employer.days_after_hire_payout
    }
    
    def get_permission_groups(employee):
        return [
            p.permission_group
            for p in employee.get_employer_permission_groups_by_employer(
                permission_groups=employee.employer_permission_group.all())[employer.id]
        ]
    
    if is_employer:
        from jvapp.apis.ats import LeverOauthTokenView  # Avoid circular import
        ats_cfg = next((c for c in employer.ats_cfg.all()), None)
        data['ats_cfg'] = {
            'id': ats_cfg.id,
            'name': ats_cfg.name,
            'email': ats_cfg.email,
            'api_key': obfuscate_string(ats_cfg.api_key),
            'has_access_token': bool(ats_cfg.refresh_token),
            'is_token_expired': LeverOauthTokenView.has_refresh_token_expired(ats_cfg),
            'is_webhook_enabled': ats_cfg.is_webhook_enabled,
            'job_stage_name': ats_cfg.job_stage_name,
            'employment_type_field_key': ats_cfg.employment_type_field_key,
            'salary_range_field_key': ats_cfg.salary_range_field_key
        } if ats_cfg else None

        slack_cfg = next((c for c in employer.slack_cfg.all()), None)
        data['slack_cfg'] = {
            'id': slack_cfg.id,
            'oauth_key': slack_cfg.oauth_key,
            'is_enabled': slack_cfg.is_enabled,
            'jobs_post_channel': slack_cfg.jobs_post_channel,
            'jobs_post_dow_bits': slack_cfg.jobs_post_dow_bits,
            'jobs_post_tod_minutes': slack_cfg.jobs_post_tod_minutes,
            'jobs_post_max_jobs': slack_cfg.jobs_post_max_jobs,
            'referrals_post_channel': slack_cfg.referrals_post_channel,
            'modal_cfg_is_salary_required': slack_cfg.modal_cfg_is_salary_required,
        } if slack_cfg else None
        
        employees = employer.employee.all()
        data['employee_count_total'] = len(employees)
        data['employee_count_active'] = len([
            e for e in employees if
            (not e.is_employer_deactivated)
            and (reduce_user_type_bits(get_permission_groups(e)) & JobVyneUser.USER_TYPE_EMPLOYEE)
            and e.has_employee_seat
        ])
        data['notification_email'] = employer.notification_email
        data['is_manual_job_entry'] = employer.is_manual_job_entry
    
    return data


def get_serialized_employer_billing(employer: Employer):
    return {
        'street_address': employer.street_address,
        'street_address_2': employer.street_address_2,
        'city': employer.city,
        'state': employer.state,
        'country': employer.country,
        'postal_code': employer.postal_code,
        'billing_email': employer.billing_email
    }


class BONUS_TYPES(Enum):
    DIRECT = 'DIRECT'  # Bonus set directly on job
    DEFAULT = 'DEFAULT'  # No bonus rule - bonus is the default
    RULE = 'RULE'


def calculate_bonus_amount(employer_job, bonus_rule=None):
    if employer_job.referral_bonus is not None:
        return {
            'amount': employer_job.referral_bonus,
            'currency': get_serialized_currency(employer_job.referral_bonus_currency),
            'type': BONUS_TYPES.DIRECT.value
        }
    
    if not bonus_rule:
        return {
            'amount': employer_job.employer.default_bonus_amount,
            'currency': get_serialized_currency(employer_job.employer.default_bonus_currency),
            'type': BONUS_TYPES.DEFAULT.value
        }
    
    # Find the latest bonus modifier if it exists
    active_modifier = None
    if employer_job.open_date:
        days_since_post = (timezone.now().date() - employer_job.open_date).days
        for modifier in bonus_rule['modifiers']:
            if (
                    modifier['start_days_after_post'] <= days_since_post and
                    ((not active_modifier) or active_modifier['start_days_after_post'] < modifier[
                        'start_days_after_post'])
            ):
                active_modifier = modifier
    
    if not active_modifier:
        bonus_amount = bonus_rule['base_bonus_amount']
    elif active_modifier['type'] == EmployerReferralBonusRuleModifier.ModifierType.PERCENT.value:
        bonus_amount = bonus_rule['base_bonus_amount'] * (1 + (active_modifier['amount'] / 100))
    else:
        bonus_amount = bonus_rule['base_bonus_amount'] + active_modifier['amount']
    
    return {
        'amount': bonus_amount,
        'currency': bonus_rule['bonus_currency'],
        'type': BONUS_TYPES.RULE.value
    }


def get_serialized_employer_job(employer_job: EmployerJob, is_include_bonus=False, rules=None):
    data = {
        'id': employer_job.id,
        'ats_job_key': employer_job.ats_job_key,
        'is_use_job_url': employer_job.employer.is_use_job_url,
        'application_url': employer_job.application_url,
        'job_title': employer_job.job_title,
        'job_description': employer_job.job_description,
        'job_description_summary': employer_job.job_description_summary,
        'responsibilities': employer_job.responsibilities,
        'qualifications': employer_job.qualifications,
        'technical_qualifications': employer_job.technical_qualifications,
        'job_department': employer_job.job_department.name if employer_job.job_department else None,
        'job_department_id': employer_job.job_department_id,
        'is_remote': employer_job.is_remote,
        'open_date': get_datetime_format_or_none(employer_job.open_date),
        'close_date': get_datetime_format_or_none(employer_job.close_date),
        'salary_currency': get_serialized_currency(employer_job.salary_currency),
        'salary_floor': employer_job.salary_floor,
        'salary_ceiling': employer_job.salary_ceiling,
        'salary_interval': employer_job.salary_interval,
        'salary_text': employer_job.salary_text,
        'referral_bonus': employer_job.referral_bonus,
        'referral_bonus_currency': get_serialized_currency(employer_job.referral_bonus_currency),
        'employment_type': employer_job.employment_type,
        'locations': [get_serialized_location(l) for l in employer_job.locations.all()],
        'locations_text': employer_job.locations_text,
        'job_source': 'website' if employer_job.is_scraped else ('ats' if employer_job.ats_job_key else 'manual')
    }
    
    if is_include_bonus and rules:
        # Serialize the rules so inclusion/exclusion criteria are grouped
        rules = [get_serialized_employer_bonus_rule(r, is_ids_only=True) for r in rules]
        rules.sort(key=lambda x: x['order_idx'])
        job_props = {
            'cities': [l.city_id for l in employer_job.locations.all()],
            'states': [l.state_id for l in employer_job.locations.all()],
            'countries': [l.country_id for l in employer_job.locations.all()]
        }
        
        # Loop through each rule in order (order_idx) and find the first rule
        # that applies to this job
        data['bonus_rule'] = None
        for rule in rules:
            is_match = True
            for ruleKey, negateFn in (
                    ('inclusion_criteria', lambda x: not x),
                    ('exclusion_criteria', lambda x: x),
            ):
                for criteriaKey, criteriaVal in rule[ruleKey].items():
                    if not criteriaVal:
                        continue
                    
                    if criteriaKey == 'departments' and negateFn(int(employer_job.job_department_id) in criteriaVal):
                        is_match = False
                        break
                    
                    if (
                            criteriaKey in ['cities', 'states', 'countries']
                            and negateFn(get_list_intersection(job_props[criteriaKey], criteriaVal))
                    ):
                        is_match = False
                        break
                    
                    if (
                            criteriaKey == 'job_titles_regex'
                            and negateFn(re.search(criteriaVal, employer_job.job_title, flags=re.IGNORECASE))
                    ):
                        is_match = False
                        break
                
                if not is_match:
                    break
            
            if is_match:
                data['bonus_rule'] = {
                    'id': rule['id'],
                    'base_bonus_amount': rule['base_bonus_amount'],
                    'bonus_currency': rule['bonus_currency'],
                    'days_after_hire_payout': rule['days_after_hire_payout']
                }
                data['bonus'] = calculate_bonus_amount(employer_job, bonus_rule=rule)
                break
    
    if is_include_bonus and not data.get('bonus'):
        data['bonus'] = calculate_bonus_amount(employer_job)
    
    return data


def get_serialized_employer_referral_request(referral_request: EmployerReferralRequest):
    return {
        'id': referral_request.id,
        'created_dt': get_datetime_format_or_none(referral_request.created_dt),
        'modified_dt': get_datetime_format_or_none(referral_request.modified_dt),
        'employer_id': referral_request.employer_id,
        'email_subject': referral_request.email_subject,
        'email_body': referral_request.email_body,
    }


def get_serialized_employer_bonus_rule(bonus_rule: EmployerReferralBonusRule, is_ids_only=False):
    return {
        'id': bonus_rule.id,
        'employer_id': bonus_rule.employer_id,
        'order_idx': bonus_rule.order_idx,
        'inclusion_criteria': {
            'departments': [d.id for d in bonus_rule.include_departments.all()] if is_ids_only else [
                {'id': d.id, 'name': d.name} for d in bonus_rule.include_departments.all()
            ],
            'cities': [c.id for c in bonus_rule.include_cities.all()] if is_ids_only else [
                {'id': c.id, 'name': c.name} for c in bonus_rule.include_cities.all()
            ],
            'states': [s.id for s in bonus_rule.include_states.all()] if is_ids_only else [
                {'id': s.id, 'name': s.name} for s in bonus_rule.include_states.all()
            ],
            'countries': [c.id for c in bonus_rule.include_countries.all()] if is_ids_only else [
                {'id': c.id, 'name': c.name} for c in bonus_rule.include_countries.all()
            ],
            'job_titles_regex': bonus_rule.include_job_titles_regex,
        },
        'exclusion_criteria': {
            'departments': [d.id for d in bonus_rule.exclude_departments.all()] if is_ids_only else [
                {'id': d.id, 'name': d.name} for d in bonus_rule.exclude_departments.all()
            ],
            'cities': [c.id for c in bonus_rule.exclude_cities.all()] if is_ids_only else [
                {'id': c.id, 'name': c.name} for c in bonus_rule.exclude_cities.all()
            ],
            'states': [s.id for s in bonus_rule.exclude_states.all()] if is_ids_only else [
                {'id': s.id, 'name': s.name} for s in bonus_rule.exclude_states.all()
            ],
            'countries': [c.id for c in bonus_rule.exclude_countries.all()] if is_ids_only else [
                {'id': c.id, 'name': c.name} for c in bonus_rule.exclude_countries.all()
            ],
            'job_titles_regex': bonus_rule.exclude_job_titles_regex,
        },
        'base_bonus_amount': bonus_rule.base_bonus_amount,
        'bonus_currency': get_serialized_currency(bonus_rule.bonus_currency),
        'days_after_hire_payout': bonus_rule.days_after_hire_payout,
        'modifiers': [
            {
                'id': modifier.id,
                'type': modifier.type,
                'amount': modifier.amount,
                'start_days_after_post': modifier.start_days_after_post
            } for modifier in bonus_rule.modifier.all()
        ]
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
