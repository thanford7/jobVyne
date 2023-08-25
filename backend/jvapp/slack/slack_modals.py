import json

from django.conf import settings

from jvapp.apis.employer import EmployerJobConnectionView
from jvapp.apis.geocoding import LocationParser
from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.apis.social import SocialLinkView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.content import JobPost
from jvapp.models.currency import Currency
from jvapp.models.employer import Employer, EmployerJob, EmployerJobConnection, ConnectionTypeBit
from jvapp.models.user import JobVyneUser, UserSocialSubscription
from jvapp.slack.slack_blocks_specific import ACTION_KEY_JOB_CONNECTION, SelectEmployer, \
    SelectEmployerJob, get_home_zip_code_input, get_industry_selections, get_job_connection_select, \
    get_job_level_selections, \
    get_profession_selections, get_remote_work_selection
from jvapp.utils.data import capitalize, coerce_float, coerce_int
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT, send_django_email
from jvapp.utils.oauth import OauthProviders
from jvapp.slack.slack_blocks import Button, Divider, InputCheckbox, InputEmail, InputNumber, InputOption, InputText, \
    Modal, \
    SectionText, Select
from jvapp.utils.response import ProcessTimer
from scrape.job_processor import JobItem, UserCreatedJobProcessor


def add_user_home_location(user, post_code):
    if not post_code:
        user.home_location = None
    else:
        location_parser = LocationParser(is_use_location_caching=False)
        home_location = location_parser.get_location(post_code, is_zip_code=True)
        user.home_location_id = home_location.id if home_location else None


def add_user_job_preferences(user, data):
    if 'job_search_type_bit' in data:
        user.job_search_type_bit = coerce_int(data['job_search_type_bit']['value'])
    user.work_remote_type_bit = coerce_int(data['work_remote_type_bit']['value'])
    
    job_search_levels = data['job_search_levels'] or []
    user.job_search_levels.set([coerce_int(l['value']) for l in job_search_levels])
    
    job_search_professions = data['job_search_professions'] or []
    user.job_search_professions.set([coerce_int(p['value']) for p in job_search_professions])
    
    job_search_industries = data['job_search_industries'] or []
    user.job_search_industries.set([coerce_int(i['value']) for i in job_search_industries])
    
    if 'job_search_qualifications' in data:
        user.job_search_qualifications = data['job_search_qualifications']


class SlackMultiViewModal:
    MODAL_IDX_SEPARATOR = '--'
    FINAL_KEY = 'final'
    START_KEY = 'start'  # Some modals are triggered from a button so we need to know that the first modal is at index 0
    BASE_CALLBACK_ID = None  # Subclass
    DEFAULT_BLOCK_TITLE = None  # Subclass
    
    def __init__(self, slack_user_profile, user, metadata, slack_cfg, action_id=None):
        self.slack_user_profile = slack_user_profile
        self.user = user
        self.metadata = metadata or {}
        self.slack_cfg = slack_cfg
        
        if action_id:
            idx_key = action_id.split(self.MODAL_IDX_SEPARATOR)[-1]
            if idx_key == self.START_KEY:
                self.current_modal_idx = 0
            else:
                self.current_modal_idx = coerce_int(idx_key) + 1
        else:
            self.current_modal_idx = 0
        
        self.header_blocks = []
        self.modal_views = []
        self.set_modal_views()
    
    def set_modal_views(self) -> list:
        raise NotImplementedError()
    
    def get_trigger_button(self, data):
        # Get the slack button that kicks off the modal view
        raise NotImplementedError()
    
    def add_modal(
            self, slack_blocks, submit_text=None, is_final=False, title_text=None,
            process_data_fn=None, process_data_once_fn=None
    ):
        """ process_data_fn is run every time to pull in data relevant to future modals
        process_data_once_fn performs some update or action, but doesn't add data necessary for future modals
        """
        modal_idx = len(self.modal_views)
        action_id = self.get_modal_action_id(modal_idx, is_final=is_final)
        self.modal_views.append(
            Modal(self.DEFAULT_BLOCK_TITLE or title_text, action_id, submit_text, slack_blocks, metadata=self.metadata)
        )
        if (modal_idx < self.current_modal_idx) and process_data_fn:
            process_data_fn()
        
        if (modal_idx + 1 == self.current_modal_idx) and process_data_once_fn:
            process_data_once_fn()
        
        is_final = is_final or (modal_idx == self.current_modal_idx)
        return is_final
    
    @classmethod
    def get_modal_action_id(cls, idx, is_final=False, is_start=False):
        idx_key = idx
        if is_final:
            idx_key = cls.FINAL_KEY
        elif is_start:
            idx_key = cls.START_KEY
        return f'{cls.BASE_CALLBACK_ID}{cls.MODAL_IDX_SEPARATOR}{idx_key}'
    
    @property
    def modal_view(self):
        return self.modal_views[-1]
    
    @property
    def modal_view_slack_object(self):
        return self.modal_view.get_slack_object()
    
    @classmethod
    def is_modal_view(cls, callback_id):
        return cls.BASE_CALLBACK_ID in callback_id


class JobSeekerModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'job-seeker'
    SUBSCRIPTION_OPTIONS_KEY = 'job_seeker_subscription'
    CONNECT_WITH_MANAGERS_KEY = 'CONNECT'
    DEFAULT_BLOCK_TITLE = 'JobVyne for Job Seekers'
    
    def save_job_seeker_preferences(self):
        add_user_job_preferences(self.user, self.metadata)
        self.user.save()
    
    def set_modal_views(self):
        is_final = self.modal_set_user_info()
        if is_final:
            return
        
        # second modal (job search preferences)
        is_final = self.modal_set_job_search_preferences()
        if is_final:
            return
        
        is_final = self.modal_set_job_search_subscriptions()
        if is_final:
            return
        
        self.modal_finalize()
    
    def modal_set_user_info(self):
        home_postal_code = self.user.home_location.postal_code if (self.user and self.user.home_location) else None
        contact_email = self.slack_user_profile['email']
        if self.user:
            contact_email = self.user.business_email or self.user.email
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
                'contact_email',
                'Email',
                'Email',
                initial_value=contact_email,
            ).get_slack_object(),
            get_home_zip_code_input(current_postal_code=home_postal_code).get_slack_object(),
        ]
        return self.add_modal(
            profile_blocks, submit_text='Continue to preferences',
            process_data_once_fn=self.save_user_data
        )
    
    def save_user_data(self):
        add_user_home_location(self.user, self.metadata['home_post_code'])
        
        self.user.professional_site_url = self.metadata['professional_site_url']
        self.user.linkedin_url = self.metadata['linkedin_url']
        if self.metadata['contact_email'] != self.user.email:
            self.user.business_email = self.metadata['contact_email']
        
        self.user.save()
    
    def modal_set_job_search_preferences(self):
        default_job_search_status = InputOption('Active', JobVyneUser.JOB_SEARCH_TYPE_ACTIVE).get_slack_object()
        job_search_status_options = [
            default_job_search_status,
            InputOption('Passive', JobVyneUser.JOB_SEARCH_TYPE_PASSIVE).get_slack_object(),
            InputOption('Not Looking', 0).get_slack_object(),
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
            get_remote_work_selection(remote_selection=self.user.work_remote_type_bit).get_slack_object(),
            get_job_level_selections(set_job_levels=self.user.job_search_levels.all()).get_slack_object(),
            get_profession_selections(set_professions=self.user.job_search_professions.all()).get_slack_object(),
            get_industry_selections(set_industries=self.user.job_search_industries.all()).get_slack_object(),
            InputText(
                'job_search_qualifications', 'Qualifications',
                'Write a few sentences about your job qualifications',
                is_multiline=True, is_optional=True, max_length=1000,
                initial_value=self.user.job_search_qualifications
            ).get_slack_object()
        ]
        
        return self.add_modal(preference_blocks, submit_text='Continue to options',
                              process_data_once_fn=self.save_job_seeker_preferences)
    
    def modal_set_job_search_subscriptions(self):
        subscription_options = [
            InputOption(
                'Receive daily job recommendations',
                UserSocialSubscription.SubscriptionType.jobs.value,
                description='Up to 6 new job recommendations per day will be sent via direct Slack message'
            ),
            InputOption(
                'Connect with hiring managers',
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
        
        return self.add_modal(subscription_blocks, submit_text='Save')
    
    def modal_finalize(self):
        subscription_changes = []
        selected_subscriptions = self.metadata[self.SUBSCRIPTION_OPTIONS_KEY]
        if self.CONNECT_WITH_MANAGERS_KEY in selected_subscriptions:
            if not self.user.is_job_search_visible:
                self.user.is_job_search_visible = True
                subscription_changes.append('➕ Added connection to hiring managers')
        elif self.user.is_job_search_visible:
            self.user.is_job_search_visible = False
            subscription_changes.append('➖ Removed connection to hiring managers')
        self.user.save()
        
        current_user_subscriptions = {
            sub.subscription_type: sub for sub in
            self.user.social_subscription.filter(provider=OauthProviders.slack.value)
        }
        current_job_sub = current_user_subscriptions.get(UserSocialSubscription.SubscriptionType.jobs.value)
        
        subscription_data = {
            'slack_cfg_id': self.slack_cfg.id,
            'slack_user_id': self.metadata['slack_user_id'],
            'user_id': self.user.id
        }
        if UserSocialSubscription.SubscriptionType.jobs.value in selected_subscriptions:
            if not current_job_sub:
                UserSocialSubscription(
                    user=self.user,
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
        self.add_modal(
            [SectionText(final_text).get_slack_object()],
            is_final=True
        )


class JobModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'job-post'
    SUBSCRIPTION_OPTIONS_KEY = 'job-influencer-subscription'
    CONTACT_OPTIONS_KEY = 'can-contact'
    DEFAULT_BLOCK_TITLE = 'JobVyne Jobs'
    
    def __init__(self, slack_user_profile, user, metadata, slack_cfg, action_id=None):
        self.job = None
        self.employer = None
        self.can_edit = False
        super().__init__(slack_user_profile, user, metadata, slack_cfg, action_id=action_id)
    
    def set_modal_views(self):
        is_final = self.modal_select_employer()
        if is_final:
            return
        
        # Second modal
        if self.employer and (not self.employer.is_user_created):
            is_final = self.modal_select_job()
            if is_final:
                return
        else:
            is_final = self.modal_create_job()
            if is_final:
                return
            
            if self.can_edit:
                is_final = self.modal_add_salary_details()
                if is_final:
                    return
                
        if (not self.job.has_salary) and self.slack_cfg.modal_cfg_is_salary_required:
            self.modal_required_job_salary()
            return
        
        is_final = self.modal_update_subscriptions()
        if is_final:
            return
        
        self.modal_finalize()
    
    def modal_select_employer(self):
        if not (post_channel_name := self.metadata['post_channel_name']):
            return self.add_modal(
                [
                    SectionText(
                        f'The admin for {self.metadata["group_name"]} has not configured a channel to post jobs to.'
                        ' Please message them to request they configure the jobs channel for JobVyne.'
                    ).get_slack_object()
                ],
                is_final=True
            )
        
        self.header_blocks = [
            SectionText(
                f'Post a job and get connected to job seekers!\nJob will be posted to #{post_channel_name}'
            ).get_slack_object(),
            Divider().get_slack_object(),
        ]
        
        return self.add_modal(
            [
                *self.header_blocks,
                SelectEmployer().get_slack_object()
            ],
            'Continue to job', process_data_fn=self.get_or_create_employer
        )
    
    def modal_select_job(self):
        potential_jobs = SelectEmployerJob.get_employer_jobs(employer_id=self.employer.id)
        if not potential_jobs:
            return self.add_modal(
                [
                    *self.header_blocks,
                    SectionText(
                        f'😔 {self.employer.employer_name} does not currently have any open jobs. If you believe this is an error, please contact support@jobvyne.com').get_slack_object()
                ],
                is_final=True
            )
        
        return self.add_modal(
            [
                *self.header_blocks,
                SelectEmployerJob(employer_id=self.employer.id).get_slack_object()
            ],
            'Continue to preferences', process_data_fn=self.get_or_create_job
        )
    
    def modal_create_job(self):
        job_detail_blocks = [
            *self.header_blocks,
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
            InputText(
                'job-application-url',
                'Job Application URL',
                'URL',
            ).get_slack_object()
        ]
        return self.add_modal(job_detail_blocks, 'Continue to salary', process_data_fn=self.get_or_create_job)
    
    def modal_add_salary_details(self):
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
            *self.header_blocks,
            Select(
                'employment-type', 'Employment Type', 'Type',
                options=employment_options,
                initial_option=default_employment_option
            ).get_slack_object(),
        ]
        
        if self.slack_cfg.modal_cfg_is_salary_required:
            job_detail_blocks.append(
                SectionText(f'\n💰 {self.slack_cfg.employer.employer_name} requires a salary range for all jobs 💰').get_slack_object()
            )
        
        salary_detail_blocks = [
            Select(
                'salary-currency', 'Currency', 'Currency',
                options=currency_options,
                initial_option=default_currency_option
            ).get_slack_object(),
            InputNumber(
                'salary-min', 'Minimum Salary', 'Amount',
                is_optional=not self.slack_cfg.modal_cfg_is_salary_required, min_value=0, is_decimal_allowed=True,
                initial_value=self.job.salary_floor
            ).get_slack_object(),
            InputNumber(
                'salary-max', 'Maximum Salary', 'Amount',
                is_optional=not self.slack_cfg.modal_cfg_is_salary_required, min_value=0, is_decimal_allowed=True,
                initial_value=self.job.salary_ceiling
            ).get_slack_object(),
            Select(
                'salary-interval', 'Salary Interval', 'Interval',
                options=salary_interval_options,
                initial_option=default_interval_option
            ).get_slack_object()
        ]
        
        job_detail_blocks = job_detail_blocks + salary_detail_blocks
        
        return self.add_modal(job_detail_blocks, 'Continue to preferences', process_data_once_fn=self.update_job_salary)
    
    def modal_required_job_salary(self):
        return self.add_modal([
            SectionText(
                (
                    f'{self.slack_cfg.employer.employer_name} requires a salary range for all jobs.\n'
                    f'Unfortunately the <{self.job.preferred_application_url}|{self.job.job_title} position> with {self.employer.employer_name} does not list a salary.\n'
                    f'If you believe this is an error, please contact {EMAIL_ADDRESS_SUPPORT}'
                )
            ).get_slack_object()
        ], is_final=True)
    
    def modal_update_subscriptions(self):
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
            *self.header_blocks,
            get_job_connection_select(False, is_include_no_connection=True).get_slack_object(),
            subscription_checkboxes.get_slack_object()
        ]
        return self.add_modal(subscription_blocks, 'Post job')
    
    def modal_finalize(self):
        from jvapp.apis.slack import SlackUserGeneratedJobPoster  # Avoid circular import
        
        # Add job connection
        connection_type = coerce_int(json.loads(self.metadata[ACTION_KEY_JOB_CONNECTION]['value'])['connection_bit'])
        is_employer_update = False
        if connection_type in (
                ConnectionTypeBit.HIRING_MEMBER.value,
                ConnectionTypeBit.CURRENT_EMPLOYEE.value
        ):
            self.user.user_type_bits |= JobVyneUser.USER_TYPE_EMPLOYEE
            is_employer_update = self.user.employer_id == self.employer.id
            self.user.employer_id = self.employer.id
            self.user.save()
        
        job_connection = EmployerJobConnection(user=self.user, job=self.job)
        is_allow_contact = self.CONTACT_OPTIONS_KEY in self.metadata[self.SUBSCRIPTION_OPTIONS_KEY]
        job_connection, is_new = EmployerJobConnectionView.get_and_update_job_connection(job_connection, {
            'connection_type': connection_type,
            'is_allow_contact': is_allow_contact
        })
        
        # Add job to group's subscription (this ensures it is displayed for this group)
        job_subscription = JobSubscriptionView.get_or_create_user_generated_subscription(self.employer.id)
        job_subscription.filter_job.add(self.job)
        
        # Summarize output
        updates = []
        
        if is_employer_update:
            updates.append(f'✔️ Updated your user profile to be an employee of {self.employer.employer_name}')
        
        if connection_type == ConnectionTypeBit.HIRING_MEMBER.value:
            updates.append('✔️ Indicated that you are part of the hiring team for this job')
        elif connection_type == ConnectionTypeBit.CURRENT_EMPLOYEE.value:
            updates.append('✔️ Indicated that you work at the employer for this job')
        elif connection_type == ConnectionTypeBit.FORMER_EMPLOYEE.value:
            updates.append('✔️ Indicated that you previously worked at the employer for this job')
        elif connection_type == ConnectionTypeBit.KNOW_EMPLOYEE.value:
            updates.append('✔️ Indicated that you know someone who works at the employer for this job')
        elif connection_type == ConnectionTypeBit.NO_CONNECTION.value:
            updates.append('✔️ Indicated that you have no connection with the employer for this job')
        
        updates.append(
            f'✔️ Indicated that you are{"" if is_allow_contact else " NOT"} open to job seekers contacting you about this job')
        
        # TODO: Ability to edit post?
        job_poster = SlackUserGeneratedJobPoster(
            self.slack_cfg, JobPost.PostChannel.SLACK_JOB.value,
            employer_id=self.metadata['group_id'],
            message_data={
                'slack_user_profile': self.slack_user_profile,
                'job_connection': job_connection
            }
        )
        is_not_sent = job_poster.send_slack_job_post(self.job)
        if is_not_sent:
            updates.append(
                f'➖ This job has already been posted to the #{self.metadata["post_channel_name"]} channel, but will be viewable on the JobVyne website')
        
        final_update_text = '*Updates:*\n'
        for update in updates:
            final_update_text += f'\n{update}'
        
        final_notes = [
            f'ℹ️ To view an active list of job seekers, visit <{settings.BASE_URL}/group/{self.slack_cfg.employer.employer_key}/?tab=community|JobVyne for {self.slack_cfg.employer.employer_name}>'
        ]
        if self.job.jv_check_permission(PermissionTypes.EDIT.value, self.user, is_raise_error=False):
            # TODO: Update JobVyne URL to the user's page where they can edit jobs
            final_notes.append(f'ℹ️ You can edit this job at any time by using the `/jv-job` command')
            final_notes.append('ℹ️ This job will remain open for the next 30 days')
        
        final_notes_text = '*Notes:*\n'
        for note in final_notes:
            final_notes_text += f'\n{note}'
        
        return self.add_modal(
            [
                SectionText(final_update_text).get_slack_object(),
                SectionText(final_notes_text).get_slack_object()
            ],
            is_final=True
        )
    
    def get_or_create_employer(self):
        employer_id = SelectEmployer().get_form_value(self.metadata)
        if not employer_id:
            return  # The use has not selected an employer yet
        if employer_id != InputOption.NEW_VALUE_KEY:
            self.employer = Employer.objects.get(id=employer_id)
        else:
            employer_name = SelectEmployer().get_form_text(self.metadata)
            employer = Employer(
                organization_type=Employer.ORG_TYPE_EMPLOYER,
                employer_name=employer_name,
                is_user_created=True,
                is_use_job_url=True
            )
            employer.save()
            self.metadata['options-employer']['value'] = employer.id
            self.employer = employer
    
    def get_or_create_job(self):
        job_id = self.metadata.get('job_id') or SelectEmployerJob(employer_id=self.employer.id).get_form_value(
            self.metadata)
        if job_id:
            self.job = EmployerJob.objects.select_related('employer').get(id=job_id)
        else:
            create_job_processor_timer = ProcessTimer('UserCreatedJobProcessor')
            job_processor = UserCreatedJobProcessor(
                self.employer,
                ignore_fields=['salary-currency', 'salary_floor', 'salary_ceiling', 'salary_interval'],
                is_use_location_caching=False
            )
            create_job_processor_timer.log_time(is_warning=True)
            
            process_job_timer = ProcessTimer('Process job')
            job_item = JobItem(
                job_title=self.metadata['job-title'],
                application_url=self.metadata['job-application-url'],
                locations=[x.strip() for x in self.metadata['locations'].split('|')],
                created_user_id=self.user.id
            )
            self.job, is_new = job_processor.process_job(job_item, user=self.user)
            self.metadata['job_id'] = self.job.id
            process_job_timer.log_time(is_warning=True)
            
            # TODO: Sending an email takes too long for Slack's 3 second response time. Make async
            # process_email_timer = ProcessTimer('Send email')
            # send_django_email(
            #     f'User {"created" if is_new else "updated"} job',
            #     'emails/user_created_job_admin_notification.html',
            #     to_email=[EMAIL_ADDRESS_SUPPORT],
            #     django_context={
            #         'job': self.job,
            #         'user': self.user,
            #         'is_exclude_final_message': True
            #     },
            #     is_tracked=False,
            #     is_include_jobvyne_subject=False
            # )
            # process_email_timer.log_time(is_warning=True)
        self.can_edit = self.job.jv_check_permission(PermissionTypes.EDIT.value, self.user, is_raise_error=False)
    
    def update_job_salary(self):
        if not self.can_edit:
            return
        
        self.job.salary_currency_name = self.metadata['salary-currency']['value']
        self.job.salary_floor = coerce_float(self.metadata['salary-min'])
        self.job.salary_ceiling = coerce_float(self.metadata['salary-max'])
        self.job.salary_interval = self.metadata['salary-interval']['value']
        self.job.save()


class FollowEmployerModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'jv-follow-employer'
    DEFAULT_BLOCK_TITLE = 'Follow employer'
    
    def __init__(self, slack_user_profile, user, metadata, slack_cfg, action_id=None):
        self.job = None
        super().__init__(slack_user_profile, user, metadata, slack_cfg, action_id=action_id)
    
    @classmethod
    def get_trigger_button(cls, data):
        job = data['job']
        return SectionText(
            f'*👀 Follow {job.employer.employer_name}*\nGet notified when this employer posts new, relevant jobs',
            accessory=Button(cls.get_modal_action_id(None, is_start=True), 'Follow', job.id)
        )
    
    def set_modal_views(self):
        is_final = self.job_preferences_modal()
        if is_final:
            return
        self.modal_finalize()
    
    def job_preferences_modal(self):
        home_post_code = self.user.home_location.postal_code if (self.user and self.user.home_location) else None
        preference_blocks = [
            SectionText(
                'Update or confirm your job search preferences so we only send you relevant jobs'
            ).get_slack_object(),
            Divider().get_slack_object(),
            get_home_zip_code_input(current_postal_code=home_post_code).get_slack_object(),
            get_remote_work_selection(remote_selection=self.user.work_remote_type_bit).get_slack_object(),
            get_job_level_selections(set_job_levels=self.user.job_search_levels.all()).get_slack_object(),
            get_profession_selections(set_professions=self.user.job_search_professions.all()).get_slack_object(),
            get_industry_selections(set_industries=self.user.job_search_industries.all()).get_slack_object()
        ]
        
        return self.add_modal(preference_blocks, submit_text='Save preferences',
                              process_data_once_fn=self.add_subscription)
    
    def add_subscription(self):
        job = EmployerJob.objects.select_related('employer').get(id=self.metadata['job_id'])
        
        # Add employer to memberships
        self.user.membership_employers.add(job.employer)
        
        # Update user preferences
        add_user_home_location(self.user, self.metadata['home_post_code'])
        add_user_job_preferences(self.user, self.metadata)
        
        # Add subscription
        subscription_data = {
            'slack_cfg_id': self.slack_cfg.id,
            'slack_user_id': self.metadata['slack_user_id'],
            'user_id': self.user.id
        }
        
        unique_subscription_fields = {
            'user': self.user,
            'provider': OauthProviders.slack.value,
            'subscription_type': UserSocialSubscription.SubscriptionType.jobs.value
        }
        
        try:
            user_subscription = UserSocialSubscription.objects.get(**unique_subscription_fields)
        except UserSocialSubscription.DoesNotExist:
            user_subscription = UserSocialSubscription(
                subscription_data=subscription_data, **unique_subscription_fields
            )
            user_subscription.save()
        self.metadata['employer_name'] = job.employer.employer_name
    
    def modal_finalize(self):
        final_text = (
            f'➕ Added {self.metadata["employer_name"]} to your list of followed companies.\n\n'
            f'ℹ You will receive a Slack notification at most once per day if {self.metadata["employer_name"]} posts a new job that matches your preferences.\n\n'
            f'You can update which companies you follow on your <{settings.BASE_URL}/candidate/favorites/|JobVyne profile>.'
        )
        self.add_modal(
            [SectionText(final_text).get_slack_object()],
            title_text='Job saved',
            is_final=True
        )


class ShareJobModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'jv-share-job'
    DEFAULT_BLOCK_TITLE = 'Share job'
    
    def __init__(self, slack_user_profile, user, metadata, slack_cfg, action_id=None):
        self.job = None
        super().__init__(slack_user_profile, user, metadata, slack_cfg, action_id=action_id)
    
    @classmethod
    def get_trigger_button(cls, data):
        job = data['job']
        return SectionText(
            f'*✉️ Share {job.job_title} job*\nShare this job with someone outside of {data["group_name"]}. The email will come from JobVyne and you will be CCed.',
            accessory=Button(cls.get_modal_action_id(None, is_start=True), 'Share', job.id)
        )
    
    def set_modal_views(self):
        is_final = self.send_job_email_modal()
        if is_final:
            return
        self.modal_finalize()
    
    def send_job_email_modal(self):
        job = EmployerJob.objects.select_related('employer').get(id=self.metadata['job_id'])
        job_link = SocialLinkView.get_or_create_single_job_link(job, owner_id=self.user.id)
        job_link_url = job_link.get_link_url()
        job_post_date = get_datetime_format_or_none(job.open_date, format_str='%x')
        email_text = (
            'Hi {to_first_name},\n'
            'I saw this job on JobVyne and thought you would be a good fit:\n\n'
            f'*Job*: <{job_link_url}|{job.job_title}>\n'
            f'*Employer*: {job.employer.employer_name}\n'
            f'*Employer description*: {job.employer.description if job.employer.description else ""}'
            f'*Location:* {job.locations_text}\n'
            f'*Salary:* {job.salary_text}\n'
            f'*Post date:* {job_post_date}\n\n'
            'I sent this email using JobVyne, but I am CCed if you have any questions.\n\n'
            f'- {self.user.full_name}'
        )
        
        # Add data to Slack's metadata so we don't have to refetch in subsequent modals
        self.metadata['job_title'] = job.job_title
        self.metadata['job_link_url'] = job_link_url
        self.metadata['job_locations_text'] = job.locations_text
        self.metadata['job_salary_text'] = job.salary_text
        self.metadata['job_post_date'] = job_post_date
        self.metadata['job_employer_name'] = job.employer.employer_name
        self.metadata['job_employer_description'] = job.employer.description
        
        job_email_blocks = [
            InputText(
                'to_first_name', 'To first name', 'Name',
                help_text='The first name of the person you want to send the job to',
                is_focused=True
            ).get_slack_object(),
            InputEmail(
                'to_email', 'To email', 'Email',
                help_text='This is the email of the person you want to send the job to'
            ).get_slack_object(),
            # TODO: Lock the CC email down to user verified emails
            InputEmail(
                'cc_email', 'CC email', 'Email',
                initial_value=self.user.email
            ).get_slack_object(),
            SectionText((
                'This is the email that will be sent (but with better formatting). '
                'The first name of the recipient will be filled in automatically.'
            )).get_slack_object(),
            Divider().get_slack_object(),
            SectionText(email_text).get_slack_object()
        ]
        
        return self.add_modal(job_email_blocks, submit_text='Send email',
                              process_data_once_fn=self.send_job_email)
    
    def send_job_email(self):
        process_email_timer = ProcessTimer('Send email')
        send_django_email(
            f'{self.user.full_name} thinks you would be great for the {self.metadata["job_title"]} position at {self.metadata["job_employer_name"]}',
            'emails/share_job_email.html',
            to_email=[self.metadata['to_email']],
            cc_email=self.metadata['cc_email'],
            django_context={
                **self.metadata,
                'recipient_first_name': self.metadata['to_first_name'],
                'from_user': self.user
            },
        )
        process_email_timer.log_time(is_warning=True)
    
    def modal_finalize(self):
        final_text = (
            f'Sent email to {self.metadata["to_first_name"]} at {self.metadata["to_email"]}.\n'
            f'Good on you for helping someone else in their job search! :grapes:'
        )
        self.add_modal(
            [SectionText(final_text).get_slack_object()],
            title_text='Email sent',
            is_final=True
        )
