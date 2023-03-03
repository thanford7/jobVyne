from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.apis._apiBase import SUCCESS_MESSAGE_KEY
from jvapp.permissions.general import IsAdmin
from jvapp.utils.email import EMAIL_ADDRESS_TEST, send_django_email


class TestErrorView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        raise ValueError('This is a test error message')
    

class TestEmailView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        send_django_email(
            'TEST EMAIL',
            'emails/base_general_email.html',
            to_email=[EMAIL_ADDRESS_TEST],
            django_context={
                'is_exclude_final_message': True
            },
            html_body_content='<p>This is a test email</p>',
            is_tracked=False,
            is_include_jobvyne_subject=False
        )
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Test email sent'
        })
