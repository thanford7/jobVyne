import os

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from jvapp.models import MessageRecipient


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


class TwilioWebhooksView(APIView):
    permission_classes = [AllowAny]
    FAILURE_STATUSES = ['failed', 'undelivered']
    SUCCESS_STATUSES = ['sent', 'delivered', 'received']
    
    def post(self, request):
        # https://www.twilio.com/docs/sms/tutorials/how-to-confirm-delivery-python
        message_sid = request.data.get('MessageSid', None)
        message_status = request.data.get('MessageStatus', None)
        message_recipient = MessageRecipient.objects.get(provider_message_key=message_sid)
        if message_status in self.FAILURE_STATUSES:
            message = self.get_message(message_sid)
            message_recipient.error_dt = timezone.now()
            message_recipient.error_reason = f'({message.error_code}) {message.error_message}'
            message_recipient.save()
        elif message_status in self.SUCCESS_STATUSES:
            message_recipient.delivered_dt = timezone.now()
            message_recipient.error_dt = None
            message_recipient.error_reason = None
            message_recipient.save()
        
        return Response(status=status.HTTP_200_OK)
        
    @staticmethod
    def get_message(sid):
        return client.messages(sid).fetch()
        
