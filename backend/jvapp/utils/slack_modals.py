import json

from jvapp.models.user import UserSocialSubscription
from jvapp.utils.data import coerce_int
from jvapp.utils.oauth import OauthProviders
from jvapp.utils.slack_blocks import Divider, InputCheckbox, InputEmail, InputOption, InputText, InputUrl, Modal


class SlackMultiViewModal:
    BASE_CALLBACK_ID = None  # Subclass
    
    def __init__(self, *args, **kwargs):
        self.modal_views = self.get_modal_views(*args, **kwargs)
        self.set_modal_view_indexes()
    
    def get_modal_views(self, *args, **kwargs) -> list:
        raise NotImplementedError()
    
    def finalize_modal(self, form_data, user=None):
        raise NotImplementedError()
    
    def set_modal_view_indexes(self):
        for idx, mv in enumerate(self.modal_views):
            mv.set_modal_view_idx(idx)
    
    def get_modal_view_slack_object(self, modal_idx=None, callback_id=None, is_next=True):
        modal_idx = coerce_int(callback_id.split(Modal.MODAL_IDX_SEPARATOR)[-1]) if modal_idx is None else modal_idx
        if is_next:
            modal_idx += 1
        
        try:
            return self.modal_views[modal_idx].get_slack_object()
        except IndexError:
            return None
    
    @classmethod
    def is_modal_view(cls, callback_id):
        return cls.BASE_CALLBACK_ID in callback_id


class JobSeekerModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'job-seeker'
    SUBSCRIPTION_OPTIONS_KEY = 'job_seeker_subscription'
    
    def __init__(self, slack_user_profile, user, metadata):
        self.slack_user_profile = slack_user_profile
        self.user = user
        super().__init__(private_metadata=metadata)
    
    def get_modal_views(self, private_metadata: dict = None):
        private_metadata = private_metadata or {}
        
        # first modal
        profile_blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'Let JobVyne connect you to job opportunities and hiring managers!'
                }
            },
            Divider().get_slack_object(),
            InputText(
                'first_name',
                'First Name',
                'First Name',
                initial_value=self.user.first_name if self.user else self.slack_user_profile['first_name'],
            ).get_slack_object(),
            InputText(
                'last_name',
                'Last Name',
                'Last Name',
                initial_value=self.user.last_name if self.user else self.slack_user_profile['last_name'],
            ).get_slack_object(),
            InputUrl(
                'linkedin_url',
                'LinkedIn',
                'LinkedIn URL',
                initial_value=self.user.linkedin_url if self.user else None,
                help_text='https://www.linkedin.com/in/{your username}'
            ).get_slack_object(),
            InputEmail(
                'email',
                'Email',
                'Email',
                initial_value=self.slack_user_profile['email'],
            ).get_slack_object(),
        ]
        
        # second modal
        subscription_options = [
            InputOption(
                'Receive daily job recommendations',
                UserSocialSubscription.SubscriptionType.jobs.value,
                description='Up to 10 new job recommendations per day will be sent via direct Slack message'
            ),
            InputOption(
                'Connect with hiring managers (upcoming feature)',
                UserSocialSubscription.SubscriptionType.connect_managers.value,
                description='Your name, email, and LinkedIn will be shown to hiring managers'
            ),
        ]
        subscription_checkboxes = InputCheckbox(
            self.SUBSCRIPTION_OPTIONS_KEY,
            'Job seeker support options',
            [opt.get_slack_object() for opt in subscription_options],
            initial_option_values=[opt.value for opt in subscription_options],
            is_optional=True
        )
        subscription_blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'Let JobVyne connect you to job opportunities and hiring managers!'
                }
            },
            Divider().get_slack_object(),
            subscription_checkboxes.get_slack_object()
        ]
        
        return [
            Modal(
                'JobVyne for Job Seekers',
                self.BASE_CALLBACK_ID,
                'Continue to preferences',
                profile_blocks,
                private_metadata=private_metadata
            ),
            Modal(
                'JobVyne for Job Seekers',
                self.BASE_CALLBACK_ID,
                'Save preferences',
                subscription_blocks,
                private_metadata=private_metadata
            )
        ]
    
    def finalize_modal(self, form_data, user=None, slack_cfg=None, slack_user_profile=None):
        assert all((user, slack_cfg, slack_user_profile))
        selected_subscriptions = form_data[self.SUBSCRIPTION_OPTIONS_KEY]
        current_user_subscriptions = {
            sub.subscription_type: sub for sub in
            user.social_subscription.filter(provider=OauthProviders.slack.value)
        }
        current_job_sub = current_user_subscriptions.get(UserSocialSubscription.SubscriptionType.jobs.value)
        current_connection_sub = current_user_subscriptions.get(UserSocialSubscription.SubscriptionType.connect_managers.value)
        
        subscription_changes = []
        subscription_data = {
            'slack_cfg_id': slack_cfg.id,
            'slack_user_id': form_data['slack_user_id'],
            'user_id': user.id
        }
        if UserSocialSubscription.SubscriptionType.jobs.value in selected_subscriptions:
            if not current_job_sub:
                UserSocialSubscription(
                    user=user,
                    provider=OauthProviders.slack.value,
                    subscription_type=UserSocialSubscription.SubscriptionType.jobs.value,
                    subscription_data=subscription_data
                ).save()
                subscription_changes.append('➕ Added subscription to daily job recommendations')
        elif current_job_sub:
            current_job_sub.delete()
            subscription_changes.append('➖ Removed subscription to daily job recommendations')
            
        if UserSocialSubscription.SubscriptionType.connect_managers.value in selected_subscriptions:
            if not current_connection_sub:
                UserSocialSubscription(
                    user=user,
                    provider=OauthProviders.slack.value,
                    subscription_type=UserSocialSubscription.SubscriptionType.connect_managers.value,
                    subscription_data=subscription_data
                ).save()
                subscription_changes.append('➕ Added connection to hiring managers')
        elif current_connection_sub:
            current_connection_sub.delete()
            subscription_changes.append('➖ Removed connection to hiring managers')
            
        if subscription_changes:
            final_text = 'The following changes were made to your subscriptions:\n'
            for change in subscription_changes:
                final_text += f'\n{change}'
        else:
            final_text = 'Your subscriptions were already up-to-date. No changes were made.'
        
        final_text += '\n\nIf you want to make changes to your profile or subscriptions you can use the `/jv-job-seeker` command.'
        
        return Modal(
            'JobVyne for Job Seekers',
            f'{self.BASE_CALLBACK_ID}--final',
            None,
            [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': final_text
                    }
                }
            ]
        ).get_slack_object()
