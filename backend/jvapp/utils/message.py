import os

from django.conf import settings
from django.utils import timezone
from twilio.rest import Client

from jvapp.models import Message, MessageRecipient

JOBVYNE_PHONE_NUMBER = '+19896584695'
JOBVYNE_TEST_NUMBER = '+13032493165'
IS_PRODUCTION = os.getenv('DB') == 'prod'

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def send_sms_message(message_body, to_number, message_thread=None, is_tracked=True):
    if not IS_PRODUCTION:
        to_number = JOBVYNE_TEST_NUMBER

    message = client.messages.create(
        body=message_body,
        from_=JOBVYNE_PHONE_NUMBER,
        to=to_number,
        # For testing
        # status_callback='https://45fe-71-196-128-60.ngrok.io/api/v1/twilio/webhooks/'
        status_callback=f'{settings.BASE_URL}/api/v1/twilio/webhooks/'
    )
    
    if is_tracked:
        jv_message = Message(
            type=Message.MessageType.SMS.value,
            body=message_body,
            from_address=message.from_,
            created_dt=timezone.now(),
            message_thread=message_thread
        )
        jv_message.save()
        
        recipient = MessageRecipient(
            message=jv_message,
            recipient_address=to_number,
            recipient_type=MessageRecipient.RecipientType.TO.value,
            provider_message_key=message.sid,
            processed_dt=message.date_sent,
        )
        if message.error_code:
            recipient.error_dt = message.date_updated
            recipient.error_reason = f'({message.error_code}) {message.error_message}'
        
        recipient.save()
        