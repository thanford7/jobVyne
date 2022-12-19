from dataclasses import asdict, dataclass
from enum import Enum

from django.db.models import F, Q
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models import Employer, JobVyneUser, MessageThread, UserNotificationPreference
from jvapp.models.abstract import PermissionTypes
from jvapp.models.tracking import Message, MessageGroup
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.email import send_django_email
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
            for unp in UserNotificationPreferenceView.get_user_notification_preferences(user, user_id, is_check_permissions=is_check_permissions)
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
        combined_notification_preferences = UserNotificationPreferenceView.get_combined_user_notification_preferences(None, user.id, is_check_permissions=False)
        notification_preference = next((cnp for cnp in combined_notification_preferences if cnp['key'] == notification_key), None)
        return bool(not notification_preference) or notification_preference['is_enabled']
    
    
class MessageView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def post(self, request):
        filter_data = self.data['userFilters']
        email_user_filter = Q()
        employer_id = self.data.get('employer_id')
        employer = None
        if not (email_subject := self.data.get('emailSubject')):
            return Response('An email subject is required', status=status.HTTP_400_BAD_REQUEST)
        if not (email_body := self.data.get('emailBody')):
            return Response('An email body is required', status=status.HTTP_400_BAD_REQUEST)
        email_body = sanitize_html(email_body)
        
        if not self.user.is_admin or employer_id:
            if not employer_id:
                return Response('You must include an employer ID', status=status.HTTP_400_BAD_REQUEST)
            employer_id = int(employer_id)
            if employer_id != self.user.employer_id:
                return Response('You do not have permission to post for this employer', status=status.HTTP_400_BAD_REQUEST)
            
            employer = Employer.objects.get(id=employer_id)
            
            email_user_filter &= Q(employer_id=employer_id)
            if user_ids := filter_data.get('userIds'):
                email_user_filter &= Q(id__in=user_ids)
        else:
            if employer_ids := filter_data.get('userEmployers'):
                email_user_filter &= Q(employer_id__in=employer_ids)
        
        if user_type_bits := filter_data.get('userTypes'):
            email_user_filter &= Q(
                user_type_bits__lt=F('user_type_bits') + (1 * F('user_type_bits').bitand(user_type_bits))
            )
        
        # Get full list of emails to send notification to
        email_users = JobVyneUser.objects.filter(email_user_filter)
        user_count = 0
        user_emails = set()
        for user in email_users:
            # Don't email users that have turned off notifications
            if not UserNotificationPreferenceView.get_is_notification_enabled(
                user, NotificationPreferenceKey.PRODUCT_HELP.value
            ):
                continue
            user_emails.add(user.email)
            user_count += 1
            if user.business_email:
                user_emails.add(user.business_email)
        
        message_thread = None
        if employer:
            all_message_groups = MessageGroupView.get_message_groups()
            message_group = MessageGroupView.get_or_create_message_group({
                'employer_id': employer.id,
                'user_type_bits': JobVyneUser.USER_TYPE_EMPLOYER
            }, all_message_groups)
            message_thread = MessageThread()
            message_thread.save()
            message_thread.message_groups.add(message_group)
        
        send_django_email(
            email_subject,
            'emails/base_general_email.html',
            bcc_email=list(user_emails),
            django_context={
                'employer_name': employer.employer_name if employer else None,
                'is_exclude_final_message': True,
                'is_unsubscribe': True
            },
            html_body_content=email_body,
            message_thread=message_thread
        )
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'Sent email to {user_count} users at {len(user_emails)} different email addresses'
        })
    
    @staticmethod
    def get_message_threads(message_thread_filter):
        return MessageThread.objects\
            .select_related(
                'message_thread_context', 'message_thread_context__job', 'message_thread_context__applicant',
                'message_thread_context__job_application'
            )\
            .prefetch_related(
                'message', 'message__message_parent', 'message__attachment', 'message__recipient',
                'message_groups'
            )\
            .filter(message_thread_filter)
    
    @staticmethod
    def get_messages(message_filter, is_include_threads=False):
        if not is_include_threads:
            message_filter &= Q(message_thread__isnull=True)
        
        return Message.objects\
            .select_related('message_parent')\
            .prefetch_related('attachment', 'recipient')\
            .filter(message_filter)


class MessageGroupView(JobVyneAPIView):
    
    @staticmethod
    def get_message_groups(message_group_filter=None):
        message_group_filter = message_group_filter or Q()
        return MessageGroup.objects \
            .select_related('employer') \
            .prefetch_related('users') \
            .filter(message_group_filter)
    
    @staticmethod
    def get_or_create_message_group(data, message_groups):
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
