__all__ = ['get_serialized_social_platform', 'get_serialized_social_link']

from jvapp.models.social import *
from jvapp.models.tracking import Message, MessageRecipient, MessageThread
from jvapp.serializers.job_subscription import get_serialized_job_subscription
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_social_platform(social_platform: SocialPlatform):
    return {
        'id': social_platform.id,
        'sort_order': social_platform.sort_order,
        'is_displayed': social_platform.is_displayed,
        'name': social_platform.name,
        'logo': social_platform.logo.url if social_platform.logo else None
    }


def get_serialized_social_link(link: SocialLink):
    data = {
        'id': link.id,
        'url': link.get_link_url(),
        'owner_id': link.owner_id,
        'employer_name': link.employer.employer_name if link.employer else None,
        'employer_key': link.employer.employer_key if link.employer else None,
        'employer_id': link.employer_id,
        'employer_org_type': link.employer.organization_type if link.employer else None,
        'link_name': link.name,
        'is_default': link.is_default,
        'is_employee_referral': link.is_employee_referral,
        'job_subscriptions': [get_serialized_job_subscription(js) for js in link.job_subscriptions.all()],
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
