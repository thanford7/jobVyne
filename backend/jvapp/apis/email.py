import json
import logging
import tempfile

from django.conf import settings
from django.core.files import File
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendgrid import EventWebhook

from jvapp.models.tracking import Message, MessageAttachment, MessageRecipient, MessageThread
from jvapp.utils.datetime import get_datetime_from_unix
from jvapp.utils.email import MESSAGE_ENVIRONMENT_KEY, MESSAGE_ID_KEY
from jvapp.utils.gmail import GmailAPIService

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
            
            # Sendgrid only allows one webhook url at a time. All messages are saved
            # with their base url to identify which environment the message came from
            # i.e. local, dev, production
            # If the webhook is sending to a mismatched environment, we don't want to process the event
            # Once we upgrade to a higher tier sendgrid account it's possible to create subaccounts to allow
            # multiple webhook urls
            if not (message_base_url := event.get(MESSAGE_ENVIRONMENT_KEY)):
                logger.info('Sendgrid webhook delivered an event without a web environment identifier')
                continue
            if message_base_url != settings.BASE_URL:
                break
                
            if not (message_id := event.get(MESSAGE_ID_KEY)):
                logger.warning('Sendgrid webhook delivered an event without a unique message ID')
                continue
            message_id = int(message_id)
            if (not message) or message_id != message.id:
                try:
                    message = Message.objects\
                        .select_related(
                            'message_thread',
                            'message_thread__message_thread_context',
                            'message_thread__message_thread_context__job_application',
                            'message_thread__message_thread_context__job_application__employer_job__employer'
                        )\
                        .prefetch_related('recipient')\
                        .get(id=message_id)
                except Message.DoesNotExist:
                    logger.warning(f'Sendgrid webhook delivered an event with unique message ID = {message_id}. Unable to locate a message with this ID.')
                    continue
            
            job_application = None
            if message.message_thread and message.message_thread.message_thread_context:
                job_application = message.message_thread.message_thread_context.job_application
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
            elif event_type in ('dropped', 'deferred', 'bounce'):
                recipient.error_dt = event_datetime
                recipient.error_reason = self.get_error_reason_msg(event, event_type)
                recipients_to_save.append(recipient)

                # Update job application notifications if this event is related
                if job_application and event['email'] in (job_application.employer_job.employer.notification_email, settings.EMAIL_ADDRESS_TEST):
                    job_application.notification_email_failure_dt = event_datetime
                    job_application.save()
            elif event_type == 'delivered':
                if not recipient.delivered_dt:
                    recipient.delivered_dt = event_datetime
                    recipients_to_save.append(recipient)
                    
                    # Update job application notifications if this event is related
                    if job_application and event['email'] in (job_application.employer_job.employer.notification_email, settings.EMAIL_ADDRESS_TEST):
                        job_application.notification_email_dt = event_datetime
                        job_application.save()
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
    
    @staticmethod
    def get_error_reason_msg(event, event_type):
        if event_type == 'dropped':
            return f'{event.get("status")} {event.get("reason")}'
        if event_type == 'deferred':
            return f'Attempts ({event.get("attempt")}) {event.get("response")}'
        if event_type == 'bounce':
            return f'{event.get("status")} | Type: {event.get("type")} | Classification: {event.get("bounce_classification")} | Reason: {event.get("reason")}'


class SendgridWebhooksInboundView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    @method_decorator(csrf_exempt)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        to_email = request.data.get('to')
        # Don't use "from" data field because it can contain text other than the email e.g. "todd <todd@jobvyne.com>"
        from_email = json.loads(request.data['envelope'])['from']
        
        # gmail_api = GmailAPIService()
        # if to_email == DEFAULT_GMAIL_EMAIL and (received_emails := gmail_api.get_gmail_messages(from_email)):
        #     message_thread_keys = {e['threadId'] for e in received_emails}
        #     message_keys = {e['id'] for e in received_emails}
        #     existing_message_keys = Message.objects.filter(
        #         external_message_key__in=message_keys,
        #         type=Message.MessageType.EMAIL.value
        #     ).values_list('external_message_key', flat=True)
        #     message_threads = {
        #         mt.external_thread_key: mt for mt in
        #         MessageThread.objects.filter(external_thread_key__in=message_thread_keys)
        #     }
        #
        #     messages_to_save = []
        #     for received_email in received_emails:
        #         # This email has already been saved
        #         if received_email['id'] in existing_message_keys:
        #             continue
            
        return Response(status=status.HTTP_200_OK)


class GmailInboundView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(csrf_exempt)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        gmail_api = GmailAPIService()
        
        # Check new messages against ones already saved in the database
        message_keys = gmail_api.get_new_message_ids_from_pub_sub(request)
        if not message_keys:
            return Response(status=status.HTTP_200_OK)
        
        existing_message_keys = Message.objects.filter(
            external_message_key__in=message_keys,
            type=Message.MessageType.EMAIL.value
        ).values_list('external_message_key', flat=True)
        new_message_keys = [mk for mk in message_keys if mk not in existing_message_keys]
        
        full_gmail_messages = []
        for message_key in new_message_keys:
            raw_email = gmail_api.get_gmail_message(message_key)
            full_gmail_messages.append(gmail_api.get_normalized_email(raw_email))
        
        message_thread_keys = {m.thread_key for m in full_gmail_messages}
        message_threads = {
            mt.external_thread_key: mt for mt in
            MessageThread.objects.filter(external_thread_key__in=message_thread_keys)
        }
        
        for gmail_message in full_gmail_messages:
            message_thread = message_threads.get(gmail_message.thread_key)
            if not message_thread:
                continue
            
            # Don't save a message without any content
            if not any((gmail_message.body_text, gmail_message.attachment_files)):
                continue

            message = Message(
                type=Message.MessageType.EMAIL.value,
                subject=gmail_message.subject,
                body=gmail_message.body_text,
                body_html=gmail_message.body_html,
                from_address=gmail_message.from_email,
                created_dt=gmail_message.created_dt,
                message_thread=message_thread,
                external_message_key=gmail_message.message_key
            )
            message.save()
            recipients = []
            for recipient_email in gmail_message.to_emails:
                recipients.append(MessageRecipient(
                    message=message,
                    recipient_address=recipient_email,
                    recipient_type=MessageRecipient.RecipientType.TO.value,
                    delivered_dt=gmail_message.created_dt,
                    processed_dt=gmail_message.created_dt
                ))
            MessageRecipient.objects.bulk_create(recipients)
            
            if gmail_message.attachment_files:
                attachments = []
                attachment_files = []
                for attachment_file_data in gmail_message.attachment_files:
                    attachment_data = gmail_api.get_message_attachment(
                        gmail_message.message_key, attachment_file_data['id']
                    )
                    if not attachment_data:
                        continue
                    attachment_file = tempfile.NamedTemporaryFile()
                    attachment_file.write(attachment_data)
                    attachment_file.flush()
                    attachment_files.append(attachment_file)
                    attachments.append(MessageAttachment(
                        message_id=message.id,
                        file=File(attachment_file, name=attachment_file_data['name'])
                    ))
                MessageAttachment.objects.bulk_create(attachments)
                for attachment_file in attachment_files:
                    attachment_file.close()
        
        return Response(status=status.HTTP_200_OK)
