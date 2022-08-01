from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.user import JobVyneUser
from jvapp.serializers.user import get_serialized_user

__all__ = ('UserView',)

from jvapp.utils.email import send_email


class UserView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, user_id=None):
        # This allows use to check authentication and conditionally grab user info in one request
        if not all((request.user, request.user.is_authenticated)):
            return Response(status=status.HTTP_200_OK, data=False)
        data = request.data
        if user_id:
            user = self.get_user(user_id=user_id)
            return Response(status=status.HTTP_200_OK, data=get_serialized_user(user))
        elif search_text := data.get('search'):
            search_text = search_text[0]
            user_filter = Q(firstName__iregex=f'^.*{search_text}.*$')
            user_filter |= Q(lastName__iregex=f'^.*{search_text}.*$')
            user_filter |= Q(email__iregex=f'^.*{search_text}.*$')
            users = self.get_user(user_filter=user_filter)
            return Response(status=status.HTTP_200_OK, data=[get_serialized_user(u) for u in users])
        
        return Response('Please provide a user ID or search text', status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get_user(user_id=None, user_email=None, user_filter=None):
        if user_id:
            user_filter = Q(id=user_id)
        elif user_email:
            user_filter = Q(email=user_email)
        
        users = JobVyneUser.objects \
            .prefetch_related('application_template', 'permission_groups') \
            .filter(user_filter)
        
        if user_id or user_email:
            if not users:
                raise JobVyneUser.DoesNotExist
            return users[0]
        
        return users
    
    @staticmethod
    def get_or_create_user(data):
        """
            :return {tuple}: (user, is_new)
        """
        try:
            return UserView.get_user(user_email=data['email']), False
        except JobVyneUser.DoesNotExist:
            return JobVyneUser.objects.create_user(
                data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                employer_id=data['employer_id'],
            ), True

    @staticmethod
    def send_password_reset_email(request, email, email_cfg):
        reset_form = JobVynePasswordResetForm({'email': email})
        assert reset_form.is_valid()
        reset_form.save(
            request=request,
            **email_cfg
        )


class JobVynePasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = context.get('subject', 'JobVyne | Reset Password')
        subject = ''.join(subject.splitlines())
        context['protocol'] = 'https'  # Overwrite protocol to always use https
        send_email(
            subject,
            to_email,
            django_context=context,
            django_email_body_template='emails/new_user_set_password_email.html'
        )
