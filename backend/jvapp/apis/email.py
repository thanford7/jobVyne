import json
import logging

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendgrid import EventWebhook

from jvapp.models import Message, MessageRecipient
from jvapp.utils.datetime import get_datetime_from_unix
from jvapp.utils.email import MESSAGE_ID_KEY

logger = logging.getLogger(__name__)


sendgrid_webhook_verifier = EventWebhook(settings.SENDGRID_WEBHOOK_KEY)


class SendgridWebhooksView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(csrf_exempt)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        is_verified = sendgrid_webhook_verifier.verify_signature(
            request.body.decode('latin-1'),
            request.headers['X-Twilio-Email-Event-Webhook-Signature'],
            request.headers['X-Twilio-Email-Event-Webhook-Timestamp']
        )
        if not is_verified:
            logger.warning('Sendgrid webhook delivered a request with an invalid verification signature')
            return Response(status=status.HTTP_200_OK)
        
        event_data = request.data
        if not event_data:
            logger.error('Sendgrid webhook delivered a request with no data')
            return Response(status=status.HTTP_200_OK)
        
        message = None
        recipients_to_save = []
        for event in event_data:
            event_type = event['event']
            if not (message_id := event.get(MESSAGE_ID_KEY)):
                logger.warning('Sendgrid webhook delivered an event without a unique message ID')
                continue
            
            if (not message) or message_id != message.id:
                try:
                    message = Message.objects.prefetch_related('recipient').get(id=message_id)
                except Message.DoesNotExist:
                    logger.warning(f'Sendgrid webhook delivered an event with unique message ID = {message_id}. Unable to locate a message with this ID.')
                    continue
            
            recipient = next((r for r in message.recipient.all() if r.recipient_address == event['email']), None)
            if not recipient:
                logger.warning(f'Sendgrid webhook delivered an event for {event["email"]} for message ID = {message_id}. Unable to locate a recipient with this email.')
                continue
            
            recipient.provider_message_key = event.get('sg_message_id') or recipient.provider_message_key
            event_datetime = get_datetime_from_unix(event['timestamp'])
            
            # Delivery events
            if event_type == 'processed':
                if not recipient.processed_dt:
                    recipient.processed_dt = event_datetime
                    recipients_to_save.append(recipient)
            elif event_type == 'dropped':
                recipient.error_dt = event_datetime
                recipient.error_reason = f'{event.get("status")} {event.get("reason")}'
                recipients_to_save.append(recipient)
            elif event_type == 'delivered':
                if not recipient.delivered_dt:
                    recipient.delivered_dt = event_datetime
                    recipients_to_save.append(recipient)
            elif event_type == 'deferred':
                recipient.error_dt = event_datetime
                recipient.error_reason = f'Attempts ({event.get("attempt")}) {event.get("response")}'
                recipients_to_save.append(recipient)
            elif event_type == 'bounce':
                recipient.error_dt = event_datetime
                recipient.error_reason = f'{event.get("status")} | Type: {event.get("type")} | Classification: {event.get("bounce_classification")} | Reason: {event.get("reason")}'
                recipients_to_save.append(recipient)
            # Engagement events
            elif event_type == 'open':
                if not recipient.opened_dt:
                    recipient.opened_dt = event_datetime
                    recipients_to_save.append(recipient)
            elif event_type == 'click':
                if not recipient.clicked_dt:
                    recipient.clicked_dt = event_datetime
                    recipients_to_save.append(recipient)
            # Webhook is configured to send these events. We may do something with them in the future
            elif event_type == 'spamreport':
                pass
            elif event_type == 'unsubscribe':
                pass
        
        MessageRecipient.objects.bulk_update(recipients_to_save, [
            'provider_message_key', 'processed_dt', 'error_dt', 'delivered_dt',
            'opened_dt', 'clicked_dt', 'error_reason'
        ])
        
        return Response(status=status.HTTP_200_OK)
