from django.conf import settings

from jvapp.apis.employer import EmployerJobConnectionView
from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.content import JobPost
from jvapp.models.currency import Currency
from jvapp.models.employer import Employer, EmployerJob, EmployerJobConnection, Taxonomy
from jvapp.models.location import REMOTE_TYPES
from jvapp.models.user import JobVyneUser, UserSocialSubscription
from jvapp.utils.data import capitalize, coerce_float, coerce_int
from jvapp.utils.oauth import OauthProviders
from jvapp.slack.slack_blocks import Divider, InputCheckbox, InputEmail, InputNumber, InputOption, InputText, InputUrl, \
    Modal, \
    SectionText, Select, SelectEmployer, SelectMulti
from scrape.job_processor import JobItem, UserCreatedJobProcessor


CANCEL_ACTION_ID = 'cancel'


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
    
    def get_modal_view(self, modal_idx=None, callback_id=None, is_next=True, is_slack_object_only=True):
        modal_idx = coerce_int(callback_id.split(Modal.MODAL_IDX_SEPARATOR)[-1]) if modal_idx is None else modal_idx
        if is_next:
            modal_idx += 1
        
        try:
            modal_view = self.modal_views[modal_idx]
            if is_slack_object_only:
                return modal_view.get_slack_object()
            return modal_view
        except IndexError:
            return None
    
    @classmethod
    def is_modal_view(cls, callback_id):
        return cls.BASE_CALLBACK_ID in callback_id


class JobSeekerModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'job-seeker'
    SUBSCRIPTION_OPTIONS_KEY = 'job_seeker_subscription'
    CONNECT_WITH_MANAGERS_KEY = 'CONNECT'
    
    def __init__(self, slack_user_profile, user, metadata):
        self.slack_user_profile = slack_user_profile
        self.user = user
        super().__init__(private_metadata=metadata)
        
    def save_job_seeker_preferences(self, user, meta_data):
        user.job_search_type_bit = coerce_int(meta_data['job_search_type_bit']['value'])
        user.work_remote_type_bit = coerce_int(meta_data['work_remote_type_bit']['value'])
        user.job_search_level_id = coerce_int(meta_data['job_search_level']['value'])
        
        job_search_professions = meta_data['job_search_professions'] or []
        user.job_search_professions.set([coerce_int(p['value']) for p in job_search_professions])
            
        job_search_industries = meta_data['job_search_industries'] or []
        user.job_search_industries.set([coerce_int(i['value']) for i in job_search_industries])
        
        user.job_search_qualifications = meta_data['job_search_qualifications']
        user.save()
    
    def get_modal_views(self, private_metadata: dict = None):
        private_metadata = private_metadata or {}
        
        # first modal (user info)
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
            InputText(
                'linkedin_url',
                'LinkedIn',
                'LinkedIn URL',
                initial_value=self.user.linkedin_url if self.user else None,
                help_text='https://www.linkedin.com/in/{your username}'
            ).get_slack_object(),
            InputText(
                'professional_site_url',
                'Professional Site',
                'Site URL',
                initial_value=self.user.professional_site_url if self.user else None,
                is_optional=True
            ).get_slack_object(),
            InputEmail(
                'email',
                'Email',
                'Email',
                initial_value=self.slack_user_profile['email'],
            ).get_slack_object(),
            InputText(
                'home_post_code',
                'Home Postal Code',
                'Postal Code',
                initial_value=self.user.home_post_code if self.user else None,
                help_text='This is used to find jobs and events close to your location'
            ).get_slack_object(),
        ]
        
        # second modal (job search preferences)
        default_remote_work_option = InputOption('Any',
                                                 REMOTE_TYPES.NO.value | REMOTE_TYPES.YES.value).get_slack_object()
        remote_work_options = [
            default_remote_work_option,
            InputOption('On-site Only', REMOTE_TYPES.NO.value).get_slack_object(),
            InputOption('Remote Only', REMOTE_TYPES.YES.value).get_slack_object()
        ]
        
        default_job_search_status = InputOption('Active', JobVyneUser.JOB_SEARCH_TYPE_ACTIVE).get_slack_object()
        job_search_status_options = [
            default_job_search_status,
            InputOption('Passive', JobVyneUser.JOB_SEARCH_TYPE_PASSIVE).get_slack_object(),
            InputOption('Not Looking', 0).get_slack_object(),
        ]
        
        user_job_level_selection = None
        if self.user.job_search_level:
            user_job_level_selection = InputOption(self.user.job_search_level.name, self.user.job_search_level.id).get_slack_object()
        job_level_options = [
            InputOption(tax.name, tax.id).get_slack_object() for tax in
            Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL).order_by('sort_order')
        ]
        
        user_industry_selections = None
        if selected_industries := self.user.job_search_industries.all():
            user_industry_selections = [
                InputOption(industry.name, industry.id).get_slack_object() for industry in
                selected_industries
            ]
        industry_options = [
            InputOption(tax.name, tax.id).get_slack_object() for tax in
            Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_INDUSTRY).order_by('name')
        ]
        
        user_profession_selections = None
        if selected_professions := self.user.job_search_professions.all():
            user_profession_selections = [
                InputOption(profession.name, profession.id).get_slack_object() for profession in
                selected_professions
            ]
        profession_options = [
            InputOption(tax.name, tax.id).get_slack_object() for tax in
            Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE).order_by('name')
        ]
        
        preference_blocks = [
            SectionText(
                'Let JobVyne connect you to job opportunities and hiring managers!'
            ).get_slack_object(),
            Divider().get_slack_object(),
            Select(
                'job_search_type_bit', 'Job Search Status', 'Status',
                job_search_status_options,
                initial_option=default_job_search_status
            ).get_slack_object(),
            Select(
                'work_remote_type_bit', 'Remote Work Preference', 'Preference',
                remote_work_options,
                initial_option=default_remote_work_option
            ).get_slack_object(),
            Select(
                'job_search_level', 'Job Level', 'Level',
                options=job_level_options, initial_option=user_job_level_selection
            ).get_slack_object(),
            SelectMulti(
                'job_search_professions', 'Professions', 'Professions',
                options=profession_options, max_selected_items=3, initial_option=user_profession_selections
            ).get_slack_object(),
            SelectMulti(
                'job_search_industries', 'Industries', 'Any Industry',
                options=industry_options, max_selected_items=5, initial_option=user_industry_selections, is_optional=True
            ).get_slack_object(),
            InputText(
                'job_search_qualifications', 'Qualifications',
                'Write a few sentences about your job qualifications',
                is_multiline=True, is_optional=True, max_length=1000,
                initial_value=self.user.job_search_qualifications
            ).get_slack_object()
        ]
        
        # third modal (subscriptions)
        subscription_options = [
            InputOption(
                'Receive daily job recommendations',
                UserSocialSubscription.SubscriptionType.jobs.value,
                description='Up to 10 new job recommendations per day will be sent via direct Slack message'
            ),
            InputOption(
                'Connect with hiring managers (upcoming feature)',
                self.CONNECT_WITH_MANAGERS_KEY,
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
            SectionText(
                'Let JobVyne connect you to job opportunities and hiring managers!'
            ).get_slack_object(),
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
                'Continue to options',
                preference_blocks,
                private_metadata=private_metadata
            ),
            Modal(
                'JobVyne for Job Seekers',
                self.BASE_CALLBACK_ID,
                'Save',
                subscription_blocks,
                private_metadata=private_metadata,
                process_data_fn=self.save_job_seeker_preferences
            )
        ]
    
    def finalize_modal(self, form_data, user=None, slack_cfg=None, slack_user_profile=None):
        assert all((user, slack_cfg, slack_user_profile))

        subscription_changes = []
        selected_subscriptions = form_data[self.SUBSCRIPTION_OPTIONS_KEY]
        if self.CONNECT_WITH_MANAGERS_KEY in selected_subscriptions:
            if not user.is_job_search_visible:
                user.is_job_search_visible = True
                subscription_changes.append('➕ Added connection to hiring managers')
        elif user.is_job_search_visible:
            user.is_job_search_visible = False
            subscription_changes.append('➖ Removed connection to hiring managers')
        user.save()
            
        current_user_subscriptions = {
            sub.subscription_type: sub for sub in
            user.social_subscription.filter(provider=OauthProviders.slack.value)
        }
        current_job_sub = current_user_subscriptions.get(UserSocialSubscription.SubscriptionType.jobs.value)
        
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


class JobModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'job-post'
    SUBSCRIPTION_OPTIONS_KEY = 'job-influencer-subscription'
    CONNECTION_OPTIONS_KEY = 'job-connection'
    CONTACT_OPTIONS_KEY = 'can-contact'
    
    def __init__(self, slack_user_profile, user, metadata):
        self.slack_user_profile = slack_user_profile
        self.user = user
        self.employer = self.get_or_create_employer(metadata)
        job = None
        is_new_job = True
        if self.employer:
            job, is_new_job = self.get_or_create_job(metadata, ignore_fields=['salary-currency', 'salary_floor', 'salary_ceiling', 'salary_interval'])
        self.job = job
        self.is_new_job = is_new_job
        self.can_edit = self.is_new_job or (
                    self.job and self.job.jv_check_permission(PermissionTypes.EDIT.value, self.user))
        
        if self.can_edit and self.job and ('salary-currency' in metadata):
            self.job.salary_currency_name = metadata['salary-currency']['value']
            self.job.salary_floor = coerce_float(metadata['salary-min'])
            self.job.salary_ceiling = coerce_float(metadata['salary-max'])
            self.job.salary_interval = metadata['salary-interval']['value']
            self.job.save()

        super().__init__(private_metadata=metadata)
    
    def get_modal_views(self, private_metadata: dict = None):
        private_metadata = private_metadata or {}
        modals = []
        
        if not (post_channel_name := private_metadata['post_channel_name']):
            return [
                Modal(
                    'JobVyne Jobs',
                    CANCEL_ACTION_ID,
                    'Cancel',
                    [
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': (
                                    f'The admin for {private_metadata["group_name"]} has not configured a channel to post jobs to.'
                                    ' Please message them to request they configure the jobs channel for JobVyne.'
                                )
                            }
                        }
                    ],
                    private_metadata=private_metadata
                )
            ]
        
        # first modal
        job_blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'Post a job and get connected to job seekers!\nJob will be posted to #{post_channel_name}'
                }
            },
            Divider().get_slack_object(),
            SelectEmployer().get_slack_object(),
            InputText(
                'job-title',
                'Job Title',
                'Job Title',
            ).get_slack_object(),
            InputText(
                'locations',
                'Locations',
                'Locations',
                help_text='Separate locations with a pipe (|). If remote is an option, include the word "Remote"'
            ).get_slack_object(),
            InputUrl(
                'job-application-url',
                'Job Application URL',
                'URL',
            ).get_slack_object()
        ]
        modals.append(
            Modal(
                'JobVyne Jobs',
                self.BASE_CALLBACK_ID,
                'Continue to details',
                job_blocks,
                private_metadata=private_metadata
            )
        )
        
        # Second modal
        if self.can_edit and self.job:
            currencies = {c.name: c for c in Currency.objects.all()}
            default_currency = currencies[self.job.salary_currency.name if self.job.salary_currency else 'USD']
            default_currency_option = InputOption(f'({default_currency.symbol}) {default_currency.name}',
                                                  default_currency.name).get_slack_object()
            currency_options = [
                InputOption(f'({c.symbol}) {c.name}', c.name).get_slack_object()
                for c in currencies.values()
            ]
            
            default_employment = self.job.employment_type or EmployerJob.EmploymentType.FULL_TIME.value
            default_employment_option = InputOption(capitalize(default_employment),
                                                    default_employment).get_slack_object()
            employment_options = [
                InputOption(capitalize(interval), interval).get_slack_object() for interval in (
                    EmployerJob.EmploymentType.FULL_TIME.value,
                    EmployerJob.EmploymentType.PART_TIME.value,
                    EmployerJob.EmploymentType.CONTRACT.value,
                    EmployerJob.EmploymentType.INTERNSHIP.value,
                )
            ]
            
            default_interval = self.job.salary_interval or EmployerJob.SalaryInterval.YEAR.value
            default_interval_option = InputOption(capitalize(default_interval), default_interval).get_slack_object()
            salary_interval_options = [
                InputOption(capitalize(interval), interval).get_slack_object() for interval in (
                    EmployerJob.SalaryInterval.YEAR.value,
                    EmployerJob.SalaryInterval.MONTH.value,
                    EmployerJob.SalaryInterval.WEEK.value,
                    EmployerJob.SalaryInterval.DAY.value,
                    EmployerJob.SalaryInterval.HOUR.value,
                    EmployerJob.SalaryInterval.ONCE.value,
                )
            ]
            
            job_detail_blocks = [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': 'Post a job and get connected to job seekers!'
                    }
                },
                Divider().get_slack_object(),
                Select(
                    'employment-type', 'Employment Type', 'Type',
                    options=employment_options,
                    initial_option=default_employment_option
                ).get_slack_object(),
                Select(
                    'salary-currency', 'Currency', 'Currency',
                    options=currency_options,
                    initial_option=default_currency_option
                ).get_slack_object(),
                InputNumber(
                    'salary-min', 'Minimum Salary', 'Amount',
                    is_optional=True, min_value=0, is_decimal_allowed=True,
                    initial_value=self.job.salary_floor
                ).get_slack_object(),
                InputNumber(
                    'salary-max', 'Maximum Salary', 'Amount',
                    is_optional=True, min_value=0, is_decimal_allowed=True,
                    initial_value=self.job.salary_ceiling
                ).get_slack_object(),
                Select(
                    'salary-interval', 'Salary Interval', 'Interval',
                    options=salary_interval_options,
                    initial_option=default_interval_option
                ).get_slack_object()
            ]
            modals.append(
                Modal(
                    'JobVyne Jobs',
                    self.BASE_CALLBACK_ID,
                    'Continue to preferences',
                    job_detail_blocks,
                    private_metadata=private_metadata
                )
            )
        
        # third modal
        connection_options = [
            InputOption(
                'I am hiring for this job',
                EmployerJobConnection.ConnectionTypeBit.HIRING_MEMBER.value,
            ).get_slack_object(),
            InputOption(
                'I work at this company',
                EmployerJobConnection.ConnectionTypeBit.CURRENT_EMPLOYEE.value,
            ).get_slack_object(),
            InputOption(
                'I previously worked at this company',
                EmployerJobConnection.ConnectionTypeBit.FORMER_EMPLOYEE.value,
            ).get_slack_object(),
            InputOption(
                'I know someone at this company',
                EmployerJobConnection.ConnectionTypeBit.KNOW_EMPLOYEE.value,
            ).get_slack_object(),
            InputOption(
                'I have no connection to this company',
                EmployerJobConnection.ConnectionTypeBit.NO_CONNECTION.value,
            ).get_slack_object(),
        ]
        
        subscription_options = [
            InputOption(
                'Job seekers can contact me about this job',
                self.CONTACT_OPTIONS_KEY,
                description=f'Job seekers will be shown your email ({self.user.email}). You can turn this off at any time'
            )
        ]
        subscription_checkboxes = InputCheckbox(
            self.SUBSCRIPTION_OPTIONS_KEY,
            'Contact option',
            [opt.get_slack_object() for opt in subscription_options],
            initial_option_values=[opt.value for opt in subscription_options],
            is_optional=True
        )
        subscription_blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'Let JobVyne connect you to active job seekers!'
                }
            },
            Divider().get_slack_object(),
            Select(
                self.CONNECTION_OPTIONS_KEY,
                'Job Connection',
                'Select Connection',
                options=connection_options
            ).get_slack_object(),
            subscription_checkboxes.get_slack_object()
        ]
        modals.append(
            Modal(
                'JobVyne Jobs',
                self.BASE_CALLBACK_ID,
                'Post job',
                subscription_blocks,
                private_metadata=private_metadata
            )
        )
        
        return modals
    
    def get_or_create_employer(self, form_data):
        if not (employer_field := form_data.get('options-employer')):
            return None
        employer_id = coerce_int(employer_field['value'])
        if employer_id:
            employer = Employer.objects.get(id=employer_id)
        else:
            employer_name = InputOption.parse_value_text(employer_field['text'])
            employer = Employer(
                organization_type=Employer.ORG_TYPE_EMPLOYER,
                employer_name=employer_name,
                is_employer_approved=False
            )
            employer.save()
        return employer
    
    def get_or_create_job(self, form_data, ignore_fields=None):
        job_processor = UserCreatedJobProcessor(self.employer, ignore_fields=ignore_fields)
        job_item = JobItem(
            job_title=form_data['job-title'],
            application_url=form_data['job-application-url'],
            locations=[x.strip() for x in form_data['locations'].split('|')],
            created_user_id=self.user.id
        )
        return job_processor.process_job(job_item, user=self.user)
    
    def finalize_modal(self, form_data, user=None, slack_cfg=None, slack_user_profile=None):
        assert all((user, slack_cfg, slack_user_profile))
        from jvapp.apis.slack import SlackUserGeneratedJobPoster  # Avoid circular import
        
        # Add job connection
        connection_type = coerce_int(form_data[self.CONNECTION_OPTIONS_KEY]['value'])
        is_employer_update = False
        if connection_type in (
                EmployerJobConnection.ConnectionTypeBit.HIRING_MEMBER.value,
                EmployerJobConnection.ConnectionTypeBit.CURRENT_EMPLOYEE.value
        ):
            user.user_type_bits |= JobVyneUser.USER_TYPE_EMPLOYEE
            is_employer_update = user.employer_id == self.employer.id
            user.employer_id = self.employer.id
            user.save()
        
        job_connection = EmployerJobConnection(user=user, job=self.job)
        is_allow_contact = self.CONTACT_OPTIONS_KEY in form_data[self.SUBSCRIPTION_OPTIONS_KEY]
        job_connection, is_new = EmployerJobConnectionView.get_and_update_job_connection(job_connection, {
            'connection_type': connection_type,
            'is_allow_contact': is_allow_contact,
            'is_job_creator': self.job.is_creator(user)
        })
        
        # Add job to group's subscription (this ensures it is displayed for this group)
        job_subscription = JobSubscriptionView.get_or_create_user_generated_subscription(self.employer.id)
        job_subscription.filter_job.add(self.job)
        
        # Summarize output
        updates = []
        if self.is_new_job:
            updates.append(f'✔️ Created new job for {self.job.job_title}')
        
        if is_employer_update:
            updates.append(f'✔️ Updated your user profile to be an employee of {self.employer.employer_name}')
        
        if connection_type == EmployerJobConnection.ConnectionTypeBit.HIRING_MEMBER.value:
            updates.append('✔️ Indicated that you are part of the hiring team for this job')
        elif connection_type == EmployerJobConnection.ConnectionTypeBit.CURRENT_EMPLOYEE.value:
            updates.append('✔️ Indicated that you work at the employer for this job')
        elif connection_type == EmployerJobConnection.ConnectionTypeBit.FORMER_EMPLOYEE.value:
            updates.append('✔️ Indicated that you previously worked at the employer for this job')
        elif connection_type == EmployerJobConnection.ConnectionTypeBit.KNOW_EMPLOYEE.value:
            updates.append('✔️ Indicated that you know someone who works at the employer for this job')
        elif connection_type == EmployerJobConnection.ConnectionTypeBit.NO_CONNECTION.value:
            updates.append('✔️ Indicated that you have no connection with the employer for this job')
        
        updates.append(
            f'✔️ Indicated that you are{"" if is_allow_contact else " NOT"} open to job seekers contacting you about this job')
        
        # TODO: Ability to edit post?
        job_poster = SlackUserGeneratedJobPoster(
            slack_cfg, JobPost.PostChannel.SLACK_JOB.value,
            employer_id=form_data['group_id'],
            message_data={
                'slack_user_profile': slack_user_profile,
                'job_connection': job_connection
            }
        )
        is_not_sent = job_poster.send_slack_job_post(self.job)
        if is_not_sent:
            updates.append(f'➖ This job has already been posted to the #{form_data["post_channel_name"]} channel, but will be viewable on the JobVyne website')
        
        final_update_text = '*Updates:*\n'
        for update in updates:
            final_update_text += f'\n{update}'
        
        final_notes = [
            # TODO: Update URL with query param for the connections tab
            f'ℹ️ To view an active list of job seekers, visit <{settings.BASE_URL}/group/{self.employer.employer_key}/|JobVyne for {self.employer.employer_name}>'
        ]
        if self.job.is_user_created:
            if self.job.is_creator(user):
                # TODO: Update JobVyne URL to the user's page where they can edit jobs
                final_notes.append(f'ℹ️ You can edit this job at any time by using the `/jv-job` command or visit <{settings.BASE_URL}/|JobVyne>')
            final_notes.append('ℹ️ This job will remain open for the next 30 days')
        
        final_notes_text = '*Notes:*\n'
        for note in final_notes:
            final_notes_text += f'\n{note}'
        
        return Modal(
            'JobVyne Jobs',
            f'{self.BASE_CALLBACK_ID}--final',
            None,
            [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': final_update_text
                    }
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': final_notes_text
                    }
                }
            ]
        ).get_slack_object()
