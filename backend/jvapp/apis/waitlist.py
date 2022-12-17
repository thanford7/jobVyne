from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.apis._apiBase import SUCCESS_MESSAGE_KEY
from jvapp.models import Waitlist
from jvapp.utils.email import send_django_email, EMAIL_ADDRESS_SALES

__all__ = ('WaitlistView', )


class WaitlistView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data['email']
        Waitlist(email=email).save()
        send_django_email(
            'Thanks for your interest!',
            'emails/waitlist_email.html',
            to_email=[email],
            from_email=EMAIL_ADDRESS_SALES,
            cc_email=EMAIL_ADDRESS_SALES,
            django_context={
                'is_exclude_final_message': False
            },
            is_tracked=False
        )
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Thanks for your interest! You\'re on the waitlist.'
        })
        