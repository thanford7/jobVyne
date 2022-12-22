from jvapp.models import Message, MessageRecipient, MessageThread
from jvapp.models.social import *

__all__ = ['get_serialized_social_platform', 'get_serialized_social_link_filter']

from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_social_platform(social_platform: SocialPlatform):
    return {
        'id': social_platform.id,
        'sort_order': social_platform.sort_order,
        'is_displayed': social_platform.is_displayed,
        'name': social_platform.name,
        'logo': social_platform.logo.url if social_platform.logo else None
    }


def get_serialized_social_link_filter(link_filter: SocialLinkFilter, is_include_performance=False):
    data = {
        'id': link_filter.id,
        'owner_id': link_filter.owner_id,
        'employer_name': link_filter.employer.employer_name,
        'employer_id': link_filter.employer_id,
        'is_default': link_filter.is_default,
        'departments': [{'name': d.name, 'id': d.id} for d in link_filter.departments.all()],
        'cities': [{'name': c.name, 'id': c.id} for c in link_filter.cities.all()],
        'states': [{'name': s.name, 'id': s.id} for s in link_filter.states.all()],
        'countries': [{'name': c.name, 'id': c.id} for c in link_filter.countries.all()],
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
                'job_title': app.employer_job.job_title,
                'apply_dt': get_datetime_format_or_none(app.created_dt)
            } for app in link_filter.job_application.all()]
        }
    
    return data


def get_serialized_message(message: Message, is_include_recipients=True):
    data = {
        'type': message.type,
        'subject': message.subject,
        'from_address': message.from_address,
        'created_dt': get_datetime_format_or_none(message.created_dt)
    }
    if is_include_recipients:
        data['recipients'] = [get_serialized_message_recipient(r) for r in message.recipient.all()]
    return data
    
    
def get_serialized_message_recipient(recipient: MessageRecipient):
    data = {
        'address': recipient.recipient_address,
        'processed_dt': get_datetime_format_or_none(recipient.processed_dt),
        'error_dt': get_datetime_format_or_none(recipient.error_dt),
        'delivered_dt': get_datetime_format_or_none(recipient.delivered_dt),
        'opened_dt': get_datetime_format_or_none(recipient.opened_dt),
        'clicked_dt': get_datetime_format_or_none(recipient.clicked_dt),
        'error_reason': recipient.error_reason
    }
    return data


def get_serialized_message_thread(msg_thread: MessageThread):
    return [get_serialized_message(m) for m in msg_thread.message.all()]
