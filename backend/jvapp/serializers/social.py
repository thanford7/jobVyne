from jvapp.models.social import *

__all__ = ['get_serialized_social_platform', 'get_serialized_social_link_filter']

from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_social_platform(social_platform: SocialPlatform):
    return {
        'id': social_platform.id,
        'name': social_platform.name,
        'logo': social_platform.logo.url if social_platform.logo else None
    }


def get_serialized_social_link_filter(link_filter: SocialLinkFilter, is_include_performance=False):
    data = {
        'id': link_filter.id,
        'owner_id': link_filter.owner_id,
        'employer_name': link_filter.employer.employer_name,
        'employer_id': link_filter.employer_id,
        'platform_name': link_filter.platform.name if link_filter.platform else None,
        'platform_id': link_filter.platform_id,
        'departments': [{'name': d.name, 'id': d.id} for d in link_filter.departments.all()],
        'cities': link_filter.cities,
        'states': [{'name': s.stateName, 'id': s.id} for s in link_filter.states.all()],
        'countries': [{'name': c.countryName, 'id': c.id} for c in link_filter.countries.all()],
        'jobs': [{'title': j.jobTitle, 'id': j.id} for j in link_filter.jobs.all()]
    }
    
    if is_include_performance:
        views = link_filter.page_view.all()
        unique_views = {view.ip_address for view in views}
        data['performance'] = {
            'views': {
                'total': len(views),
                'unique': len(unique_views)
            },
            'applications': [{
                'id': app.id,
                'first_name': app.first_name,
                'last_name': app.last_name,
                'job_title': app.employer_job.jobTitle,
                'apply_dt': get_datetime_format_or_none(app.created_dt)
            } for app in link_filter.job_application.all()]
        }
    
    return data
