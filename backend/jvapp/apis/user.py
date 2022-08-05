from collections import defaultdict

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models.abstract import PermissionTypes
from jvapp.models.user import JobVyneUser, UserUnknownEmployer
from jvapp.permissions.general import IsAuthenticatedOrPostOrRead
from jvapp.serializers.user import get_serialized_user
from jvapp.utils.data import AttributeCfg, set_object_attributes
from jvapp.utils.email import send_email
from jvapp.utils.security import check_user_token, generate_user_token, get_uid_from_user, get_user_id_from_uid, \
    get_user_key_from_token

__all__ = ('UserView', 'UserEmailVerificationView', 'UserEmailVerificationGenerateView')


class UserView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrPostOrRead]
    
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
    
    @atomic
    def post(self, request):
        email = self.data.get('email')
        password = self.data.get('password')
        if not email or not password:
            return Response('Email and password are required', status=status.HTTP_400_BAD_REQUEST)

        user = JobVyneUser.objects.create_user(email, password=password)

        # User wasn't created through social auth so we need to verify their email
        self.send_email_verification_email(request, user, 'email')
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'User with email address <{user.email}> successfully created'
        })
    
    @atomic
    def put(self, request, user_id):
        user = self.get_user(user_id=user_id)
        user.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        set_object_attributes(user, self.data, {
            'first_name': AttributeCfg(is_protect_existing=True),
            'last_name': AttributeCfg(is_protect_existing=True),
            'business_email': AttributeCfg(is_protect_existing=True),
            'user_type_bits': None,
            'employer_id': AttributeCfg(is_protect_existing=True),
        })
        
        if 'profile_picture_url' in self.data and not self.data['profile_picture_url']:
            user.profile_picture = None
        
        if profile_picture := self.files.get('profile_picture'):
            user.profile_picture = profile_picture[0]
        
        user.save()
        
        if unknown_employer_name := self.data.get('unknown_employer_name'):
            UserUnknownEmployer(user=user, employer_name=unknown_employer_name).save()
        
        return Response(status=status.HTTP_200_OK)
    
    @staticmethod
    def get_user(user_id=None, user_email=None, user_filter=None):
        if user_id:
            user_filter = Q(id=user_id)
        elif user_email:
            user_filter = Q(email=user_email)
        
        users = JobVyneUser.objects \
            .select_related('employer') \
            .prefetch_related(
                'application_template',
                'employer_permission_group',
                'employer_permission_group__permission_group',
                'employer_permission_group__permission_group__permissions'
            ) \
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
        
    @staticmethod
    def send_email_verification_email(request, user, email_key):
        current_site = get_current_site(request)
        send_email(
            'JobVyne | Email Verification',
            getattr(user, email_key),
            django_email_body_template='emails/verify_email_email.html',
            django_context={
                'user': user,
                'domain': current_site.domain,
                'uid': get_uid_from_user(user),
                'token': generate_user_token(user, email_key)
            }
        )
        
        
class UserEmailVerificationGenerateView(JobVyneAPIView):
    
    @atomic
    def post(self, request):
        if not (email := self.data.get('email')):
            return Response('An email is required', status=status.HTTP_400_BAD_REQUEST)
        
        if email == self.user.email:
            email_key = 'email'
        elif email == self.user.business_email:
            email_key = 'business_email'
        else:
            return Response('Unrecognized email for this user', status=status.HTTP_400_BAD_REQUEST)
        
        UserView.send_email_verification_email(request, self.user, email_key)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'Verification email sent to {email}'
        })
        
        
class UserEmailVerificationView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    @atomic
    def post(self, request):
        uid = self.data.get('uid')
        token = self.data.get('token')
        if not uid or not token:
            return Response('A UID and token are required', status=status.HTTP_400_BAD_REQUEST)
        
        user_id = get_user_id_from_uid(uid)
        email_key = get_user_key_from_token(token)
        user = UserView.get_user(user_id=user_id)
        is_valid_token = check_user_token(user, email_key, token)
        if not is_valid_token:
            return Response('This email verification link is no longer valid', status=status.HTTP_400_BAD_REQUEST)
        
        if email_key == 'email':
            user.is_email_verified = True
        elif email_key == 'business_email':
            user.is_business_email_verified = True
        else:
            return Response(f'Unknown email key: {email_key}', status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{getattr(user, email_key)} successfully verified'
        })


class JobVynePasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = context.get('subject', 'JobVyne | Reset Password')
        subject = ''.join(subject.splitlines())
        send_email(
            subject,
            to_email,
            django_context=context,
            django_email_body_template='emails/new_user_set_password_email.html'
        )
