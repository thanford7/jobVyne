from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.apis._apiBase import SUCCESS_MESSAGE_KEY
from jvapp.permissions.general import IsAdmin
from jvapp.utils.email import send_django_email


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
            to_email=[settings.EMAIL_ADDRESS_TEST],
            django_context={
                'is_exclude_final_message': True
            },
            html_body_content='''
                <p>Julia Styles (jstyles@hooli.com) is owed a referral bonus of $2,000 for the following new hire.</p>
                <p>
                    <table class="bordered" width="100%" cellpadding="0" cellspacing="0" style="min-width:100%; border-collapse: collapse;">
                        <tbody>
                            <tr>
                                <td style="border: 1px solid black; font-weight: bold; padding: 5px;">Hire name</td>
                                <td style="border: 1px solid black; padding: 5px;">Dwayne Johnson</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid black; font-weight: bold; padding: 5px;">Hire date</td>
                                <td style="border: 1px solid black; padding: 5px;">April 3, 2023</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid black; font-weight: bold; padding: 5px;">Job title</td>
                                <td style="border: 1px solid black; padding: 5px;">Customer Success Manager</td>
                            </tr>
                        </tbody>
                    </table>
                </p>
            ''',
            is_tracked=False,
            is_include_jobvyne_subject=False
        )
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Test email sent'
        })
