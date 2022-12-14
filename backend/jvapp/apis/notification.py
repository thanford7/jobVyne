from dataclasses import asdict, dataclass
from enum import Enum

from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models import JobVyneUser, UserNotificationPreference


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
        
        user_notification_preferences = {
            unp.notification_key: unp for unp in self.get_user_notification_preferences(self.user, user_id)
        }
        try:
            user = JobVyneUser.objects.get(id=user_id)
        except JobVyneUser.DoesNotExist:
            return Response('This user ID does not exist', status=status.HTTP_400_BAD_REQUEST)
        
        # Get all of the notifications relevant to this user
        combined_notification_preferences = [asdict(np) for np in notification_preferences if np.user_type_bits & user.user_type_bits]
        for notification_preference in combined_notification_preferences:
            user_preference = user_notification_preferences.get(notification_preference['key'])
            notification_preference['is_enabled'] = user_preference.is_enabled if user_preference else notification_preference['default_is_enabled']
        
        return Response(status=status.HTTP_200_OK, data=combined_notification_preferences)
    
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
        
        UserNotificationPreference.objects.bulk_create(new_preferences)
        UserNotificationPreference.objects.bulk_update(update_preferences, ['is_enabled'])
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'User notification preferences updated'
        })
    
    @staticmethod
    def get_user_notification_preferences(user, user_id):
        user_notification_preferences = UserNotificationPreference.objects.filter(user_id=user_id)
        return UserNotificationPreference.jv_filter_perm(user, user_notification_preferences)
