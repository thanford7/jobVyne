from collections import defaultdict
from string import Template

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count, Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.geocoding import LocationParser
from jvapp.models import Employer, EmployerAuthGroup
from jvapp.models.abstract import PermissionTypes
from jvapp.models.user import JobVyneUser, UserEmployeeProfileQuestion, UserEmployeeProfileResponse, UserFile, \
    UserSocialCredential, \
    UserUnknownEmployer
from jvapp.permissions.general import IsAuthenticatedOrPostOrRead
from jvapp.serializers.user import get_serialized_user, get_serialized_user_file, get_serialized_user_profile
from jvapp.utils.data import AttributeCfg, set_object_attributes
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT, get_attachment, get_encoded_file, send_email
from jvapp.utils.oauth import OAUTH_CFGS
from jvapp.utils.security import check_user_token, generate_user_token, get_uid_from_user, get_user_id_from_uid, \
    get_user_key_from_token

__all__ = ('UserView', 'UserEmailVerificationView', 'UserEmailVerificationGenerateView')


class UserView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrPostOrRead]
    
    def get(self, request, user_id=None):
        # This allows us to check authentication and conditionally grab user info in one request
        if not all((request.user, request.user.is_authenticated)):
            return Response(status=status.HTTP_200_OK, data=False)
        if user_id:
            user = self.get_user(self.user, user_id=user_id)
            return Response(status=status.HTTP_200_OK, data=get_serialized_user(user))

        employer_id = self.query_params.get('employer_id')
        search_text = self.query_params.get('search')
        if any([employer_id, search_text]):
            if employer_id:
                users = self.get_user(self.user, user_filter=Q(employer_id=employer_id))
            else:
                search_text = search_text[0]
                user_filter = Q(firstName__iregex=f'^.*{search_text}.*$')
                user_filter |= Q(lastName__iregex=f'^.*{search_text}.*$')
                user_filter |= Q(email__iregex=f'^.*{search_text}.*$')
                users = self.get_user(self.user, user_filter=user_filter)
                
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
        user = self.get_user(self.user, user_id=user_id)
        user.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        
        # Make sure business email is not a duplicate
        new_business_email = self.data.get('business_email')
        if new_business_email and new_business_email == user.email:
            return Response('Business email cannot be the same as your personal email', status=status.HTTP_400_BAD_REQUEST)
        
        # Reset email verification if this is a new email
        if new_business_email != user.business_email:
            user.is_business_email_verified = False
        
        set_object_attributes(user, self.data, {
            'first_name': AttributeCfg(is_ignore_excluded=True),
            'last_name': AttributeCfg(is_ignore_excluded=True),
            'business_email': AttributeCfg(is_ignore_excluded=True),
            'user_type_bits': None,
            'employer_id': AttributeCfg(is_ignore_excluded=True),
            'is_profile_viewable': AttributeCfg(is_ignore_excluded=True),
            'job_title': AttributeCfg(is_ignore_excluded=True),
            'employment_start_date': AttributeCfg(is_ignore_excluded=True)
        })
        
        if 'profile_picture_url' in self.data and not self.data['profile_picture_url']:
            user.profile_picture = None
        
        if profile_picture := self.files.get('profile_picture'):
            user.profile_picture = profile_picture[0]
            
        if home_location_text := self.data.get('home_location_text'):
            location_parser = LocationParser()
            location = location_parser.get_location(home_location_text)
            user.home_location = location

        user.save()
        
        if responses := self.data.get('profile_questions'):
            new_responses = []
            user.profile_response.all().delete()
            for response in responses:
                if not response['response']:
                    continue
                new_responses.append(UserEmployeeProfileResponse(
                    question_id=response['question_id'],
                    user_id=self.user.id,
                    answer=response['response']
                ))
            UserEmployeeProfileResponse.objects.bulk_create(new_responses)
        
        if unknown_employer_name := self.data.get('unknown_employer_name'):
            UserUnknownEmployer(user=user, employer_name=unknown_employer_name).save()
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'User updated successfully'
        })
    
    @staticmethod
    def get_user(user, user_id=None, user_email=None, user_filter=None, is_check_permission=True):
        if user_id:
            user_filter = Q(id=user_id)
        elif user_email:
            user_filter = Q(email=user_email)
        
        users = JobVyneUser.objects \
            .select_related('employer') \
            .prefetch_related(
                'application_template',
                'employer_permission_group',
                'employer_permission_group__employer',
                'employer_permission_group__permission_group',
                'employer_permission_group__permission_group__permissions',
                'profile_response',
                'profile_response__question'
            ) \
            .annotate(is_approval_required=Count(
                'employer_permission_group',
                # Note this does not differentiate between different employers
                # It's possible that a user needs permission from one employer, but not another
                filter=Q(employer_permission_group__is_employer_approved=False)
            )) \
            .filter(user_filter)
        
        if is_check_permission:
            JobVyneUser.jv_filter_perm(user, users)
        
        if user_id or user_email:
            if not users:
                raise JobVyneUser.DoesNotExist
            return users[0]
        
        return users
    
    @staticmethod
    def get_or_create_user(user, data):
        """
            :return {tuple}: (user, is_new)
        """
        try:
            return UserView.get_user(user, user_email=data['email']), False
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
                'token': generate_user_token(user, email_key),
                'is_exclude_final_message': False
            }
        )
        
        
class UserProfileView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, user_id):
        user = UserView.get_user(self.user, user_id=user_id, is_check_permission=False)
        return Response(status=status.HTTP_200_OK, data=get_serialized_user_profile(user))
        
        
class UserFileView(JobVyneAPIView):
    
    def get(self, request):
        if not (user_id := self.query_params.get('user_id')):
            return Response('A user ID is required', status=status.HTTP_400_BAD_REQUEST)
        files = self.get_user_files(user_id)
        return Response(
            status=status.HTTP_200_OK,
            data=[get_serialized_user_file(f) for f in files]
        )
    
    @atomic
    def post(self, request):
        user_file = UserFile()
        file = self.files['file'][0] if self.files.get('file') else None
        self.update_user_file(user_file, self.data, self.user, file=file)
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: f'Created a new file titled {user_file.title}'
            }
        )
    
    @atomic
    def put(self, request, file_id):
        user_file = UserFile.objects.get(id=file_id)
        self.update_user_file(user_file, self.data, self.user)
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: f'Updated file titled {user_file.title}'
            }
        )
    
    @atomic
    def delete(self, request, file_id):
        user_file = UserFile.objects.get(id=file_id)
        user_file.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        user_file.delete()
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: 'File deleted'
            }
        )
    
    @staticmethod
    def get_user_files(user_id):
        return UserFile.objects.filter(user_id=user_id)

    @staticmethod
    @atomic
    def update_user_file(user_file, data, user, file=None):
        set_object_attributes(user_file, data, {
            'user_id': None,
            'title': None
        })
    
        if file:
            user_file.file = file
    
        user_file.title = (
                user_file.title
                or getattr(file, 'name', None)
                or user_file.file.name.split('/')[-1]
        )
    
        permission_type = PermissionTypes.EDIT.value if user_file.id else PermissionTypes.CREATE.value
        user_file.jv_check_permission(permission_type, user)
        user_file.save()
        
        
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
        user = UserView.get_user(self.user, user_id=user_id, is_check_permission=False)
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
    
    
class UserSocialCredentialsView(JobVyneAPIView):
    
    def get(self, request):
        social_credentials = UserSocialCredential.objects.filter(user_id=self.user.id)
        data = defaultdict(list)
        for cred in social_credentials:
            # Google is only used for authentication, not for social sharing
            if cred.provider == 'google-oauth2':
                continue
            name = OAUTH_CFGS[cred.provider]['name']
            data[name].append({
                'email': cred.email,
                'platform_name': name,
                'provider': cred.provider
            })
        return Response(status=status.HTTP_200_OK, data=data)
    
    
class UserEmployeeProfileQuestionsView(JobVyneAPIView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        employer = Employer.objects.get(id=employer_id)
        formatted_questions = []
        user_responses = {
            response.question_id: response.answer
            for response in UserEmployeeProfileResponse.objects.filter(user_id=self.user.id)
        }
        for question in UserEmployeeProfileQuestion.objects.all():
            question_template = Template(question.text)
            formatted_questions.append({
                'question_id': question.id,
                'question': question_template.substitute(employer_name=employer.employer_name),
                'response': user_responses.get(question.id)
            })
        return Response(status=status.HTTP_200_OK, data=formatted_questions)
    
    
class FeedbackView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Send email to JobVyne support team
        if self.user:
            user = {
                'name': f'{self.user.first_name} {self.user.last_name}',
                'email': self.user.email
            }
        else:
            user = self.data

        send_email(
            'JobVyne | User Feedback', EMAIL_ADDRESS_SUPPORT,
            django_email_body_template='emails/support_email.html',
            django_context={
                'is_exclude_final_message': True,
                'user': user,
                'message': self.data['message']
            },
            attachments=[
                get_attachment(file.name, get_encoded_file(file.file), file.content_type, file.name) for file in self.files.get('files')
            ] if self.files.get('files') else None
        )
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Thanks for your message. An email has been sent to our support team and we will follow up with you if necessary.'
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
            django_email_body_template='emails/base_reset_password_email.html'
        )
