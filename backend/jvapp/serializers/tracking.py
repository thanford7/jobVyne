from jvapp.models.tracking import Message
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.file import get_file_name


def get_serialized_message(message: Message):
    return {
        'id': message.id,
        'type': message.type,
        'subject': message.subject,
        'body': message.body,
        'body_html': message.body_html,
        'from_address': message.from_address,
        'created_dt': get_datetime_format_or_none(message.created_dt),
        'recipients': [
            {
                'address': recipient.recipient_address,
                'type': recipient.recipient_type,
                'delivered_dt': get_datetime_format_or_none(recipient.delivered_dt),
                'opened_dt': get_datetime_format_or_none(recipient.opened_dt),
                'error_dt': get_datetime_format_or_none(recipient.error_dt),
                'error_reason': recipient.error_reason
            } for recipient in message.recipient.all()
        ],
        'attachments': [
            {
                'name': get_file_name(attachment.file.name),
                'url': attachment.file.url
            } for attachment in message.attachment.all()
        ]
    }
