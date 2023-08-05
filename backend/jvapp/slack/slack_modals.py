from django.conf import settings

from jvapp.apis.employer import EmployerJobConnectionView
from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.content import JobPost
from jvapp.models.currency import Currency
from jvapp.models.employer import Employer, EmployerJob, EmployerJobConnection, Taxonomy, ConnectionTypeBit
from jvapp.models.location import REMOTE_TYPES
from jvapp.models.user import JobVyneUser, UserSocialSubscription
from jvapp.utils.data import capitalize, coerce_float, coerce_int
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT, send_django_email
from jvapp.utils.oauth import OauthProviders
from jvapp.slack.slack_blocks import Divider, InputCheckbox, InputEmail, InputNumber, InputOption, InputText, InputUrl, \
    Modal, \
    SectionText, Select, SelectEmployer, SelectEmployerJob, SelectMulti
from scrape.job_processor import JobItem, UserCreatedJobProcessor


class SlackMultiViewModal:
    MODAL_IDX_SEPARATOR = '--'
    FINAL_KEY = 'final'
    BASE_CALLBACK_ID = None  # Subclass
    DEFAULT_BLOCK_TITLE = None  # Subclass
    
    def __init__(self, slack_user_profile, user, metadata, slack_cfg, action_id=None):
        self.slack_user_profile = slack_user_profile
        self.user = user
        self.metadata = metadata or {}
        self.slack_cfg = slack_cfg
        self.current_modal_idx = coerce_int(action_id.split(self.MODAL_IDX_SEPARATOR)[-1]) + 1 if action_id else 0
        self.header_blocks = []
        self.modal_views = []
        self.set_modal_views()
    
    def set_modal_views(self) -> list:
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
    
    def get_modal_action_id(self, idx, is_final=False):
        return f'{self.BASE_CALLBACK_ID}{self.MODAL_IDX_SEPARATOR}{self.FINAL_KEY if is_final else idx}'
    
    @property
    def modal_view(self):
        return self.modal_views[-1].get_slack_object()
    
    @classmethod
    def is_modal_view(cls, callback_id):
        return cls.BASE_CALLBACK_ID in callback_id


class JobSeekerModalViews(SlackMultiViewModal):
    BASE_CALLBACK_ID = 'job-seeker'
    SUBSCRIPTION_OPTIONS_KEY = 'job_seeker_subscription'
    CONNECT_WITH_MANAGERS_KEY = 'CONNECT'
    DEFAULT_BLOCK_TITLE = 'JobVyne for Job Seekers'
    
    def save_job_seeker_preferences(self):
        self.user.job_search_type_bit = coerce_int(self.metadata['job_search_type_bit']['value'])
        self.user.work_remote_type_bit = coerce_int(self.metadata['work_remote_type_bit']['value'])
        self.user.job_search_level_id = coerce_int(self.metadata['job_search_level']['value'])
        
        job_search_professions = self.metadata['job_search_professions'] or []
        self.user.job_search_professions.set([coerce_int(p['value']) for p in job_search_professions])
        
        job_search_industries = self.metadata['job_search_industries'] or []
        self.user.job_search_industries.set([coerce_int(i['value']) for i in job_search_industries])
        
        self.user.job_search_qualifications = self.metadata['job_search_qualifications']
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
        return self.add_modal(profile_blocks, submit_text='Continue to preferences')
    
    def modal_set_job_search_preferences(self):
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
            user_job_level_selection = InputOption(self.user.job_search_level.name,
                                                   self.user.job_search_level.id).get_slack_object()
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
                options=industry_options, max_selected_items=5, initial_option=user_industry_selections,
                is_optional=True
            ).get_slack_object(),
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
                description='Up to 10 new job recommendations per day will be sent via direct Slack message'
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
    CONNECTION_OPTIONS_KEY = 'job-connection'
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
        return self.add_modal(job_detail_blocks, 'Continue to preferences', process_data_once_fn=self.update_job_salary)
    
    def modal_update_subscriptions(self):
        connection_options = [
            InputOption(
                'I am hiring for this job',
                ConnectionTypeBit.HIRING_MEMBER.value,
            ).get_slack_object(),
            InputOption(
                'I work at this company',
                ConnectionTypeBit.CURRENT_EMPLOYEE.value,
            ).get_slack_object(),
            InputOption(
                'I previously worked at this company',
                ConnectionTypeBit.FORMER_EMPLOYEE.value,
            ).get_slack_object(),
            InputOption(
                'I know someone at this company',
                ConnectionTypeBit.KNOW_EMPLOYEE.value,
            ).get_slack_object(),
            InputOption(
                'I have no connection to this company',
                ConnectionTypeBit.NO_CONNECTION.value,
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
            *self.header_blocks,
            Select(
                self.CONNECTION_OPTIONS_KEY,
                'Job Connection',
                'Select Connection',
                options=connection_options
            ).get_slack_object(),
            subscription_checkboxes.get_slack_object()
        ]
        return self.add_modal(subscription_blocks, 'Post job')
    
    def modal_finalize(self):
        from jvapp.apis.slack import SlackUserGeneratedJobPoster  # Avoid circular import
        
        # Add job connection
        connection_type = coerce_int(self.metadata[self.CONNECTION_OPTIONS_KEY]['value'])
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
        if self.job.jv_check_permission(PermissionTypes.EDIT.value, self.user):
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
        job_id = self.metadata.get('job_id') or SelectEmployerJob(employer_id=self.employer.id).get_form_value(self.metadata)
        if job_id:
            self.job = EmployerJob.objects.select_related('employer').get(id=job_id)
        else:
            job_processor = UserCreatedJobProcessor(
                self.employer,
                ignore_fields=['salary-currency', 'salary_floor', 'salary_ceiling', 'salary_interval']
            )
            job_item = JobItem(
                job_title=self.metadata['job-title'],
                application_url=self.metadata['job-application-url'],
                locations=[x.strip() for x in self.metadata['locations'].split('|')],
                created_user_id=self.user.id
            )
            self.job, is_new = job_processor.process_job(job_item, user=self.user)
            self.metadata['job_id'] = self.job.id
            
            send_django_email(
                f'User {"created" if is_new else "updated"} job',
                'emails/user_created_job_admin_notification.html',
                to_email=[EMAIL_ADDRESS_SUPPORT],
                django_context={
                    'job': self.job,
                    'user': self.user,
                    'is_exclude_final_message': True
                },
                is_tracked=False,
                is_include_jobvyne_subject=False
            )
        self.can_edit = self.job.jv_check_permission(PermissionTypes.EDIT.value, self.user)
    
    def update_job_salary(self):
        if not self.can_edit:
            return
        
        self.job.salary_currency_name = self.metadata['salary-currency']['value']
        self.job.salary_floor = coerce_float(self.metadata['salary-min'])
        self.job.salary_ceiling = coerce_float(self.metadata['salary-max'])
        self.job.salary_interval = self.metadata['salary-interval']['value']
        self.job.save()
