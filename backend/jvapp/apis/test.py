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
        send_django_email('TEST EMAIL', [EMAIL_ADDRESS_TEST], html_content='<p>This is a test email</p>')
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Test email sent'
        })
