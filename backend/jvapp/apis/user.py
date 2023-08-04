from collections import defaultdict
from string import Template

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Q
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, WARNING_MESSAGES_KEY, get_error_response, \
    get_success_response, get_warning_response
from jvapp.apis.geocoding import LocationParser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.content import SocialPost
from jvapp.models.employer import Employer, EmployerJob
from jvapp.models.social import SocialLink
from jvapp.models.user import JobVyneUser, UserApplicationReview, UserEmployeeProfileQuestion, \
    UserEmployeeProfileResponse, UserFile, \
    UserSocialCredential, \
    UserUnknownEmployer
from jvapp.permissions.general import IsAuthenticatedOrPostOrRead
from jvapp.serializers.employer import get_serialized_currency
from jvapp.serializers.location import get_serialized_location
from jvapp.serializers.user import get_serialized_user, get_serialized_user_file, get_serialized_user_profile
from jvapp.utils.data import AttributeCfg, coerce_bool, coerce_int, set_object_attributes
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT, send_django_email
from jvapp.utils.oauth import OAUTH_CFGS, OauthProviders
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
        
        return get_error_response('Please provide a user ID or search text')
    
    @atomic
    def post(self, request):
        email = self.data.get('email')
        password = self.data.get('password')
        if not email or not password:
            return get_error_response('Email and password are required')
        
        extra_user_props = {}
        for prop in ('user_type_bits', 'first_name', 'last_name'):
            prop_val = self.data.get(prop)
            if prop_val is not None:
                extra_user_props[prop] = prop_val
        
        try:
            user = JobVyneUser.objects.create_user(email, password=password, **extra_user_props)
        except IntegrityError:
            return get_warning_response(f'User with email address <{email}> already exists. Login or reset your password.')
        except ValidationError as e:
            return get_warning_response(str(e))
        
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
            return get_error_response('Business email cannot be the same as your personal email')
        
        # Reset email verification if this is a new email
        if new_business_email != user.business_email:
            user.is_business_email_verified = False
        
        set_object_attributes(user, self.data, {
            'first_name': AttributeCfg(is_ignore_excluded=True),
            'last_name': AttributeCfg(is_ignore_excluded=True),
            'business_email': AttributeCfg(is_ignore_excluded=True),
            'user_type_bits': AttributeCfg(is_ignore_excluded=True),
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
        
        try:
            user.save()
        except IntegrityError as e:
            return get_error_response(str(e))
        
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
            user_filter = Q(email=user_email) | Q(business_email=user_email)
        
        users = JobVyneUser.objects \
            .select_related('employer') \
            .prefetch_related(
                'application_template',
                'employer_permission_group',
                'employer_permission_group__employer',
                'employer_permission_group__permission_group',
                'employer_permission_group__permission_group__permissions',
                'profile_response',
                'profile_response__question',
                'social_credential'
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
    def get_or_create_user(user, data, is_check_permission=True):
        """
        :return {tuple}: (user, is_new)
        """
        try:
            return UserView.get_user(user, user_email=data['email'], is_check_permission=is_check_permission), False
        except JobVyneUser.DoesNotExist:
            return JobVyneUser.objects.create_user(
                data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                employer_id=data.get('employer_id'),
            ), True
    
    @staticmethod
    def send_password_reset_email(user, is_new=False):
        
        uid = get_uid_from_user(user)
        token = generate_user_token(user, 'email')
        reset_password_url = f'{settings.BASE_URL}/password-reset/{uid}/{token}'
        send_django_email(
            'Reset Password',
            'emails/base_reset_password_email.html',
            to_email=user.email,
            django_context={
                'supportEmail': EMAIL_ADDRESS_SUPPORT,
                'reset_password_url': reset_password_url,
                'is_new': is_new,
                'user': user
            },
            is_tracked=False
        )

    @staticmethod
    def send_email_verification_email(request, user, email_key):
        current_site = get_current_site(request)
        send_django_email(
            'Email Verification',
            'emails/verify_email_email.html',
            to_email=getattr(user, email_key),
            django_context={
                'user': user,
                'domain': current_site.domain,
                'uid': get_uid_from_user(user),
                'token': generate_user_token(user, email_key),
                'is_exclude_final_message': False
            },
            is_tracked=False
        )


class UserProfileView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        user_id = self.query_params.get('user_id')
        social_link_id = self.query_params.get('social_link_id')
        assert any((user_id, social_link_id))
        if social_link_id:
            try:
                user_id = SocialLink.objects.get(id=social_link_id).owner_id
            except SocialLink.DoesNotExist:
                return Response(status=status.HTTP_200_OK, data=None)
        if not user_id:
            return Response(status=status.HTTP_200_OK, data=None)
        
        user = UserView.get_user(self.user, user_id=user_id, is_check_permission=False)
        return Response(status=status.HTTP_200_OK, data=get_serialized_user_profile(user))
    
    
class UserCreatedJobView(JobVyneAPIView):
    
    def get(self, request):
        user_id = self.query_params.get('user_id')
        is_approved = self.query_params.get('is_approved')
        if is_approved is not None:
            is_approved = coerce_bool(is_approved)
        is_closed = self.query_params.get('is_closed')
        if is_closed is not None:
            is_closed = coerce_bool(is_closed)
        page_count = coerce_int(self.query_params.get('page_count', 1))
        jobs = self.get_user_jobs(self.user, user_id=user_id, is_approved=is_approved, is_closed=is_closed)
        paged_jobs = Paginator(jobs, per_page=25)
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                'total_page_count': paged_jobs.num_pages,
                'total_job_count': paged_jobs.count,
                'jobs': [
                    self.get_serialized_user_job(job, self.user)
                    for job in paged_jobs.get_page(page_count)
                ],
            }
        )
    
    def delete(self, request):
        job_id = self.data['job_id']
        try:
            job = EmployerJob.objects.get(id=job_id)
        except EmployerJob.DoesNotExist:
            return get_error_response('This job does not exist')
        
        # We allow user created jobs to be deleted because they may have been created by mistake
        job.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        if not job.is_user_created:
            return get_error_response('This job cannot be deleted. Instead you can edit it and set the "close date"')
        
        return get_success_response('Job was deleted')
    
    @staticmethod
    def get_user_jobs(user, user_id=None, is_approved=None, is_closed=None, job_filter=None):
        if (not user.is_admin) and (user.id != user_id or user_id is None):
            raise PermissionError('You do not have permission to access these jobs')
        
        if not job_filter:
            job_filter = Q()
        job_filter &= Q(job_connection__is_job_creator=True)
        if user_id:
            job_filter &= Q(created_user_id=user_id)
        if is_approved is not None:
            job_filter &= Q(is_job_approved=is_approved)
        if is_closed is not None:
            if is_closed:
                job_filter &= (Q(close_date__isnull=False) & Q(close_date__lt=timezone.now().date()))
            else:
                job_filter &= (Q(close_date__isnull=True) | Q(close_date__gt=timezone.now().date()))
            
        return (
            EmployerJob.objects
            .select_related('employer', 'created_user')
            .prefetch_related(
                'job_connection',
                'locations',
                'locations__city',
                'locations__state',
                'locations__country'
            )
            .filter(job_filter)
            .order_by('created_dt', 'id')
        )
    
    @staticmethod
    def get_serialized_user_job(job: EmployerJob, user: JobVyneUser):
        user_job = {
            'id': job.id,
            'job_title': job.job_title,
            'open_date': get_datetime_format_or_none(job.open_date),
            'close_date': get_datetime_format_or_none(job.close_date),
            'salary_currency': get_serialized_currency(job.salary_currency),
            'salary_floor': job.salary_floor,
            'salary_ceiling': job.salary_ceiling,
            'salary_interval': job.salary_interval,
            'salary_text': job.salary_text,
            'locations': [get_serialized_location(l) for l in job.locations.all()],
            'locations_text': job.locations_text,
            'employer_id': job.employer_id,
            'employer_name': job.employer.employer_name,
            'employer_logo': job.employer.logo.url if job.employer.logo else None,
            'employment_type': job.employment_type,
            'is_remote': job.is_remote,
            'is_approved': job.is_job_approved,
            'can_edit': job.jv_check_permission(PermissionTypes.EDIT.value, user)
        }
        
        if user.is_admin:
            user_job['created_by'] = f'{job.created_user.full_name} ({job.created_user.id})'
            user_job['created_by_email'] = job.created_user.email
        
        return user_job


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
        
        
class UserJobApplicationReviewView(JobVyneAPIView):
    
    def post(self, request):
        application_review = self.get_job_application_reviews(
            self.user, job_application_id=self.data['application_id'], user_id=self.data['user_id']
        )
        application_review = application_review[0] if application_review else UserApplicationReview()
        is_new = self.update_job_application_review(self.user, application_review, self.data)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{"Created" if is_new else "Updated"} job application review'
        })
        
    def put(self, request):
        application_review = self.get_job_application_reviews(self.user, application_review_id=self.data['application_review_id'])
        self.update_job_application_review(self.user, application_review, self.data)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Updated job application review'
        })
    
    @staticmethod
    def update_job_application_review(user, application_review, data):
        is_new = False
        if not application_review.id:
            set_object_attributes(application_review, data, {
                'user_id': None,
                'application_id': None,
            })
            is_new = True
        application_review.rating = data['rating']

        permission_type = PermissionTypes.EDIT.value if application_review.id else PermissionTypes.CREATE.value
        application_review.jv_check_permission(permission_type, user)
        application_review.save()
        return is_new
        
    @staticmethod
    def get_job_application_reviews(user, application_review_id=None, job_application_id=None, user_id=None):
        review_filter = Q(id=application_review_id) if application_review_id else Q(application_id=job_application_id)
        if user_id:
            review_filter &= Q(user_id=user_id)
        reviews = UserApplicationReview.objects\
            .select_related('application', 'application__employer_job', 'application__social_link')\
            .filter(review_filter)
        reviews = UserApplicationReview.jv_filter_perm(user, reviews)
        if application_review_id:
            if reviews:
                return reviews[0]
            else:
                raise UserApplicationReview.DoesNotExist
        
        return reviews


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
        is_valid_token = check_user_token(user, token)
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
            name = OAUTH_CFGS[cred.provider]['name']
            data[name].append({
                'id': cred.id,
                'email': cred.email,
                'platform_name': name,
                'provider': cred.provider,
                'expiration_dt': get_datetime_format_or_none(cred.expiration_dt)
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


class UserEmployeeChecklistView(JobVyneAPIView):
    
    def get(self, request, user_id):
        user = UserView.get_user(self.user, user_id=user_id)
        auto_posts = SocialPost.objects.filter(user_id=user.id, is_auto_post=True)
        data = {
            'is_email_verified': user.is_email_verified,
            'is_business_email_verified': user.is_business_email_verified,
            'is_email_employer_permitted': user.is_email_employer_permitted,
            'has_secondary_email': bool(user.business_email),
            'has_updated_profile': bool(user.profile_response.all()),
            'has_scheduled_auto_post': bool(auto_posts)
        }
        
        social_credentials = UserSocialCredential.objects.filter(user_id=user_id).values_list('provider', flat=True)
        data['has_connected_linkedin'] = OauthProviders.linkedin.value in social_credentials
        return Response(status=status.HTTP_200_OK, data=data)


class FeedbackView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Send email to JobVyne support team
        if self.user:
            user = {
                'name': self.user.full_name,
                'email': self.user.email
            }
        else:
            user = self.data
        
        send_django_email(
            'User Feedback', 'emails/support_email.html',
            to_email=EMAIL_ADDRESS_SUPPORT,
            django_context={
                'is_exclude_final_message': True,
                'user': user,
                'message': self.data['message']
            },
            files=self.files.get('files'),
            is_include_jobvyne_subject=False
        )
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Thanks for your message. An email has been sent to our support team and we will follow up with you if necessary.'
        })
