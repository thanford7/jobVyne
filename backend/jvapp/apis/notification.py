from dataclasses import asdict, dataclass
from enum import Enum

from django.db.models import F, Q
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.models import Employer, JobApplication, JobVyneUser, MessageThread, UserNotificationPreference
from jvapp.models.abstract import PermissionTypes
from jvapp.models.tracking import Message, MessageGroup, MessageThreadContext
from jvapp.permissions.employer import IsAdminOrEmployerPermission, IsAdminPermission
from jvapp.utils.email import ContentPlaceholders, send_django_email
from jvapp.utils.gmail import GmailException
from jvapp.utils.sanitize import sanitize_html


@dataclass
class NotificationPreference:
    title: str
    description: str
    key: str
    user_type_bits: int
    default_is_enabled: bool


class NotificationPreferenceKey(Enum):
    NEW_APPLICATION = 'new_application'
    SOCIAL_ACCOUNT_EXPIRATION = 'social_account_expiration'
    PRODUCT_HELP = 'product_help'


notification_preferences = [
    NotificationPreference(
        'New application',
        'Receive an email when a candidate applies to a job from one of your links',
        NotificationPreferenceKey.NEW_APPLICATION.value,
        JobVyneUser.USER_TYPE_EMPLOYEE,
        True
    ),
    NotificationPreference(
        'Social account expiration',
        'Receive email notifications when one or more of your social accounts is about to expire (typically every 2 months)',
        NotificationPreferenceKey.SOCIAL_ACCOUNT_EXPIRATION.value,
        JobVyneUser.USER_TYPE_EMPLOYEE,
        True
    ),
    NotificationPreference(
        'Product updates and helpful hints',
        'Receive emails about new product features and ways you can maximize your referrals',
        NotificationPreferenceKey.PRODUCT_HELP.value,
        JobVyneUser.USER_TYPE_EMPLOYEE,
        True
    )
]


class UserNotificationPreferenceView(JobVyneAPIView):
    
    def get(self, request):
        if not (user_id := self.query_params.get('user_id')):
            return Response('A user ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = JobVyneUser.objects.get(id=user_id)
        except JobVyneUser.DoesNotExist:
            return Response('This user ID does not exist', status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            status=status.HTTP_200_OK,
            data=self.get_combined_user_notification_preferences(self.user, user_id, user.user_type_bits)
        )
    
    def put(self, request):
        if not (user_id := self.data.get('user_id')):
            return Response('A user ID is required', status=status.HTTP_400_BAD_REQUEST)
        if not (user_notification_preferences := self.data.get('notification_preferences')):
            return Response('Notification preferences are required', status=status.HTTP_400_BAD_REQUEST)
        
        current_user_notification_preferences = {
            unp.notification_key: unp for unp in self.get_user_notification_preferences(self.user, user_id)
        }
        new_preferences = []
        update_preferences = []
        for preference in user_notification_preferences:
            current_preference = current_user_notification_preferences.get(preference['key'])
            if not current_preference:
                new_preferences.append(UserNotificationPreference(
                    user_id=user_id,
                    notification_key=preference['key'],
                    is_enabled=preference['is_enabled']
                ))
            else:
                current_preference.is_enabled = preference['is_enabled']
                update_preferences.append(current_preference)
        
        if new_preferences:
            new_preferences[0].jv_check_permission(PermissionTypes.CREATE.value, self.user)
            UserNotificationPreference.objects.bulk_create(new_preferences)
        if update_preferences:
            update_preferences[0].jv_check_permission(PermissionTypes.EDIT.value, self.user)
            UserNotificationPreference.objects.bulk_update(update_preferences, ['is_enabled'])
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'User notification preferences updated'
        })
    
    @staticmethod
    def get_user_notification_preferences(user, user_id, is_check_permissions=True):
        user_notification_preferences = UserNotificationPreference.objects.filter(user_id=user_id)
        if is_check_permissions:
            return UserNotificationPreference.jv_filter_perm(user, user_notification_preferences)
        return user_notification_preferences
    
    @staticmethod
    def get_combined_user_notification_preferences(user, user_id, user_type_bits=None, is_check_permissions=True):
        """
        :param user: The user making the request
        :param user_id: The user_id to get user preferences
        :param user_type_bits: The bits indicating which user preferences should be included (e.g. employee notifications)
        :return {dict}: Serialized user notification preferences
        """
        assert (not is_check_permissions) or user
        user_notification_preferences = {
            unp.notification_key: unp
            for unp in UserNotificationPreferenceView.get_user_notification_preferences(user, user_id,
                                                                                        is_check_permissions=is_check_permissions)
        }
        
        # Get all of the notifications relevant to this user
        combined_notification_preferences = [asdict(np) for np in notification_preferences if
                                             user_type_bits is None or (np.user_type_bits & user_type_bits)]
        for notification_preference in combined_notification_preferences:
            user_preference = user_notification_preferences.get(notification_preference['key'])
            notification_preference['is_enabled'] = user_preference.is_enabled if user_preference else \
                notification_preference['default_is_enabled']
        
        return combined_notification_preferences
    
    @staticmethod
    def get_is_notification_enabled(user, notification_key):
        combined_notification_preferences = UserNotificationPreferenceView.get_combined_user_notification_preferences(
            None, user.id, is_check_permissions=False)
        notification_preference = next(
            (cnp for cnp in combined_notification_preferences if cnp['key'] == notification_key), None)
        return bool(not notification_preference) or notification_preference['is_enabled']


class BaseMessageView(JobVyneAPIView):
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.email_subject = self.data.get('emailSubject')
        if not self.email_subject:
            return get_error_response('An email subject is required')
        self.email_body = self.data.get('emailBody')
        if not self.email_body:
            return get_error_response('An email body is required')
        self.email_body = sanitize_html(self.email_body)
        
        self.filter_data = self.data.get('userFilters') or {}
    
    def send_email(self, user_emails, employer=None, message_thread=None, message_context=None):
        message_context = message_context or {}
        send_django_email(
            self.email_subject,
            'emails/base_general_email.html',
            bcc_email=list(user_emails),
            django_context={
                'employer_name': employer.employer_name if employer else None,
                'is_exclude_final_message': True,
                'is_unsubscribe': True,
                **message_context
            },
            employer=employer,
            html_body_content=self.email_body,
            message_thread=message_thread
        )
    
    @staticmethod
    def get_user_emails(email_user_filter, notification_preference=None):
        # Get full list of emails to send notification to
        email_users = JobVyneUser.objects.filter(email_user_filter)
        user_count = 0
        user_emails = set()
        for user in email_users:
            # Don't email users that have turned off notifications
            if notification_preference and (
                    not UserNotificationPreferenceView.get_is_notification_enabled(
                        user, notification_preference
                    )
            ):
                continue
            user_emails.add(user.email)
            user_count += 1
            if user.business_email:
                user_emails.add(user.business_email)
        
        return user_emails, user_count

    @staticmethod
    def get_message_threads(message_thread_filter):
        return MessageThread.objects \
            .select_related(
            'message_thread_context', 'message_thread_context__job', 'message_thread_context__applicant',
            'message_thread_context__job_application'
        ) \
            .prefetch_related(
            'message', 'message__message_parent', 'message__attachment', 'message__recipient',
            'message_groups'
        ) \
            .filter(message_thread_filter)

    @staticmethod
    def get_messages(message_filter, is_include_threads=False):
        if not is_include_threads:
            message_filter &= Q(message_thread__isnull=True)
    
        return Message.objects \
            .select_related('message_parent') \
            .prefetch_related('attachment', 'recipient') \
            .filter(message_filter)
    
    @staticmethod
    def get_success_response(user_count, user_emails, user_term='user'):
        pluralized_user_term = user_term if user_count == 1 else f'{user_term}s'
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'Sent email to {user_count} {pluralized_user_term} at {len(user_emails)} different email addresses'
        })


class MessageAdminView(BaseMessageView):
    permission_classes = [IsAdminPermission]
    
    def post(self, request):
        email_user_filter = Q()
        if employer_ids := self.filter_data.get('userEmployers'):
            email_user_filter &= Q(employer_id__in=employer_ids)
        if user_type_bits := self.filter_data.get('userTypes'):
            email_user_filter &= Q(
                user_type_bits__lt=F('user_type_bits') + (1 * F('user_type_bits').bitand(user_type_bits))
            )
        
        user_emails, user_count = self.get_user_emails(
            email_user_filter, notification_preference=NotificationPreferenceKey.PRODUCT_HELP.value
        )
        
        self.send_email(user_emails)
        return self.get_success_response(user_count, user_emails)
    
    
class BaseMessageEmployerView(BaseMessageView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        
        if not (employer_id := self.data.get('employer_id')):
            return get_error_response('An employer ID is required')
        self.employer_id = int(employer_id)
        if self.employer_id != self.user.employer_id:
            return get_error_response('You do not have permission to post for this employer')
        self.employer = Employer.objects.get(id=employer_id)
        employer_message_groups = MessageGroupView.get_message_groups(Q(employer_id=self.employer_id))
        
        # All messages in this group will be accessible to users with employer type access
        self.employer_message_group = MessageGroupView.get_or_create_message_group({
            'employer_id': self.employer_id,
            'user_type_bits': JobVyneUser.USER_TYPE_EMPLOYER
        }, message_groups=employer_message_groups)
    
    
class MessageEmployerApplicantView(BaseMessageEmployerView):
    
    def post(self, request):
        if not (application_ids := self.data.get('application_ids')):
            return get_error_response('At least one application ID is required')

        job_applications = JobApplication.objects\
            .select_related('employer_job')\
            .prefetch_related(
                'message_thread_context',
                'message_thread_context__message_thread'
            )\
            .filter(
                employer_job__employer_id=self.employer_id,
                id__in=application_ids
            )
        for job_application in job_applications:
            if message_thread_context := job_application.message_thread_context.all():
                message_thread_context = message_thread_context[0]
                message_thread = message_thread_context.message_thread
            else:
                message_thread = MessageThread()
                message_thread.save()
                message_thread_context = MessageThreadContext(
                    message_thread=message_thread,
                    job_application=job_application
                )
                message_thread_context.save()

            message_thread.message_groups.add(self.employer_message_group)
            
            formatted_email_subject = self.get_formatted_text(self.email_subject, job_application)
            formatted_email_body = self.get_formatted_text(self.email_body, job_application)
            try:
                send_django_email(
                    formatted_email_subject,
                    'emails/base_general_email.html',
                    to_email=job_application.email,
                    from_email=self.data.get('from_email'),
                    is_include_jobvyne_subject=False,
                    django_context={
                        'employer_name': self.employer.employer_name,
                        'is_exclude_final_message': True,
                        'is_unsubscribe': True
                    },
                    employer=self.employer,
                    html_body_content=formatted_email_body,
                    message_thread=message_thread,
                    is_gmail=True
                )
            except GmailException as e:
                return get_error_response(str(e))
        
        return self.get_success_response(len(job_applications), job_applications, 'applicant')
    
    @staticmethod
    def get_formatted_text(raw_text, job_application):
        formatted_text = raw_text.replace(
            ContentPlaceholders.APPLICANT_FIRST_NAME.value,
            job_application.first_name
        )
        formatted_text = formatted_text.replace(
            ContentPlaceholders.APPLICANT_LAST_NAME.value,
            job_application.last_name
        )
        formatted_text = formatted_text.replace(
            ContentPlaceholders.JOB_TITLE.value,
            job_application.employer_job.job_title
        )
        return formatted_text


class MessageEmployerEmployeeView(BaseMessageEmployerView):
    
    def post(self, request):
        email_user_filter = Q(employer_id=self.employer_id)
        if user_ids := self.filter_data.get('userIds'):
            email_user_filter &= Q(id__in=user_ids)
        
        if user_type_bits := self.filter_data.get('userTypes'):
            email_user_filter &= Q(
                user_type_bits__lt=F('user_type_bits') + (1 * F('user_type_bits').bitand(user_type_bits))
            )
        
        user_emails, user_count = self.get_user_emails(email_user_filter)
        message_thread = MessageThread()
        message_thread.save()
        message_thread.message_groups.add(self.employer_message_group)
        
        self.send_email(user_emails, employer=self.employer, message_thread=message_thread)
        return self.get_success_response(user_count, user_emails, user_term='employee')


class MessageGroupView(JobVyneAPIView):
    
    @staticmethod
    def get_message_groups(message_group_filter=None):
        message_group_filter = message_group_filter or Q()
        return MessageGroup.objects \
            .select_related('employer') \
            .prefetch_related('users') \
            .filter(message_group_filter)
    
    @staticmethod
    def get_or_create_message_group(data, message_groups=None):
        message_groups = message_groups or MessageGroupView.get_message_groups()
        user_ids = data.get('user_ids')
        employer_id = data.get('employer_id')
        user_type_bits = data.get('user_type_bits')
        
        if not MessageGroup.is_valid_instance(user_ids, employer_id):
            raise ValueError('At least one user ID or employer ID is required')
        
        distinct_message_groups = {
            mg.get_key(): mg for mg in message_groups
        }
        
        message_group_key = MessageGroup.get_key_from_data(
            user_ids, employer_id, user_type_bits
        )
        
        existing_message_group = distinct_message_groups.get(message_group_key)
        if existing_message_group:
            return existing_message_group
        
        new_message_group = MessageGroup(
            employer_id=employer_id,
            user_type_bits=user_type_bits
        )
        new_message_group.save()
        
        if user_ids:
            group_users_through_model = MessageGroup.users.through
            group_users_through_model.objects.bulk_create([
                group_users_through_model(message_group=new_message_group, jobvyneuser=user_id)
                for user_id in user_ids
            ])
        
        return new_message_group
    
    @staticmethod
    def get_or_create_employer_message_group(employer_id, message_groups=None):
        message_groups = message_groups or MessageGroupView.get_message_groups(Q(employer_id=employer_id))
        return MessageGroupView.get_or_create_message_group({
            'employer_id': employer_id,
            'user_type_bits': JobVyneUser.USER_TYPE_EMPLOYER
        }, message_groups=message_groups)
