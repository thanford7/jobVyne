from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.apis._apiBase import SUCCESS_MESSAGE_KEY
from jvapp.models import SalesInquiry, Waitlist
from jvapp.utils.data import set_object_attributes
from jvapp.utils.email import EMAIL_ADDRESS_SEND, send_django_email, EMAIL_ADDRESS_SALES

__all__ = ('WaitlistView', 'SalesInquiryView')


class SalesInquiryView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        inquiry = SalesInquiry(created_dt=timezone.now())
        set_object_attributes(inquiry, request.data, {
            'first_name': None,
            'last_name': None,
            'company_name': None,
            'email': None
        })
        inquiry.save()
        send_django_email(
            'New sales inquiry',
            'emails/sales_inquiry_email.html',
            to_email=[EMAIL_ADDRESS_SALES],
            from_email=EMAIL_ADDRESS_SEND,
            django_context={
                'inquiry': inquiry,
                'is_exclude_final_message': True
            },
            is_tracked=False
        )
        return Response(status=status.HTTP_200_OK)


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
        