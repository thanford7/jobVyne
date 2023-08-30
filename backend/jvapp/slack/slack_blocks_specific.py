import json

from django.db.models import Q
from django.utils import timezone

from jvapp.apis.taxonomy import TaxonomyJobProfessionView
from jvapp.models.employer import ConnectionTypeBit, EmployerJob, EmployerJobConnection, Taxonomy
from jvapp.models.location import REMOTE_TYPES
from jvapp.slack.slack_blocks import Button, InputOption, InputText, Modal, SectionText, Select, SelectExternal, \
    SelectMulti
from jvapp.utils.data import coerce_int


class SelectEmployer(SelectExternal):
    OPTIONS_LOAD_KEY = 'options-employer'
    
    def __init__(self, *args, focus_on_load=False, **kwargs):
        super().__init__(
            self.OPTIONS_LOAD_KEY, 'Select employer', 'Select employer',
            focus_on_load=focus_on_load, min_query_length=2
        )
    
    def get_form_value(self, form_data):
        val = form_data.get(self.OPTIONS_LOAD_KEY)
        return val['value'] if val else None
    
    def get_form_text(self, form_data):
        val = form_data.get(self.OPTIONS_LOAD_KEY)
        return val['text'] if val else None


class SelectEmployerJob(SelectExternal):
    OPTIONS_LOAD_KEY_PREPEND = 'options-employer-job'
    EMPLOYER_ID_SPLIT = '--'
    
    def __init__(self, *args, employer_id=None, focus_on_load=False, **kwargs):
        assert employer_id
        self.employer_id = employer_id
        super().__init__(
            self.get_options_load_key(), 'Select job', 'Select job',
            focus_on_load=focus_on_load, min_query_length=2
        )
    
    def get_form_value(self, form_data):
        val = form_data.get(self.get_options_load_key())
        return val['value'] if val else None
    
    def set_form_value(self, form_data, job_id):
        val = form_data.get(self.get_options_load_key())
        val['value'] = job_id
    
    def get_options_load_key(self):
        return f'{self.OPTIONS_LOAD_KEY_PREPEND}{self.EMPLOYER_ID_SPLIT}{self.employer_id}'
    
    @classmethod
    def get_employer_id(cls, options_load_key):
        return coerce_int(options_load_key.split(cls.EMPLOYER_ID_SPLIT)[-1])
    
    @classmethod
    def get_employer_jobs(cls, employer_id=None, options_load_key=None, regex_pattern=None):
        assert employer_id or options_load_key
        employer_id = employer_id or SelectEmployerJob.get_employer_id(options_load_key)
        employer_job_filter = (
                Q(employer_id=employer_id)
                & (Q(close_date__isnull=True) | Q(close_date__gt=timezone.now().date()))
        )
        if regex_pattern:
            employer_job_filter &= Q(job_title__iregex=regex_pattern)
        employer_jobs = (
            EmployerJob.objects
            .prefetch_related('locations')
            .filter(employer_job_filter)
        )
        
        # If we are loading jobs for the first time, we present the most recent because that
        # is likely what the user is looking for
        if not options_load_key:
            employer_jobs.order_by('-open_date')
        else:
            employer_jobs.order_by('job_title', 'id')
        
        return employer_jobs[:SelectExternal.OPTIONS_LIMIT]


def get_final_confirmation_modal(title, confirmation_text):
    return Modal(
        title, 'final', None,
        [SectionText(confirmation_text).get_slack_object()], is_final=True
    )


def get_profession_label(profession):
    has_parent = bool(profession.parent_taxonomy.all())
    inset = '•    ' if has_parent else ''
    return f'{inset}{profession.name}'


def get_profession_selections(set_professions=None, max_selected_items=3):
    profession_selections = None
    if set_professions:
        profession_selections = [
            InputOption(get_profession_label(profession), profession.id).get_slack_object() for profession in
            set_professions
        ]
    
    professions = TaxonomyJobProfessionView.get_job_profession_taxonomy()
    profession_options = []
    for profession in professions:
        profession_options.append(
            InputOption(get_profession_label(profession), profession.id).get_slack_object()
        )
        for sub_profession in profession.sub_taxonomies.all():
            profession_options.append(
                InputOption(get_profession_label(sub_profession), sub_profession.id).get_slack_object()
            )
    
    return SelectMulti(
        'job_search_professions', 'Professions', 'Professions',
        options=profession_options, max_selected_items=max_selected_items, initial_option=profession_selections
    )


def get_industry_selections(set_industries=None, max_selected_items=5):
    industry_selections = None
    if set_industries:
        industry_selections = [
            InputOption(industry.name, industry.id).get_slack_object() for industry in
            set_industries
        ]
    industry_options = [
        InputOption(tax.name, tax.id).get_slack_object() for tax in
        Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_INDUSTRY).order_by('name')
    ]
    
    return SelectMulti(
        'job_search_industries', 'Industries', 'Any Industry',
        options=industry_options, max_selected_items=max_selected_items, initial_option=industry_selections,
        is_optional=True
    )


def get_job_level_selections(set_job_levels=None):
    job_level_selections = None
    if set_job_levels:
        job_level_selections = [
            InputOption(job_level.name, job_level.id).get_slack_object() for job_level in
            set_job_levels
        ]
    job_level_options = [
        InputOption(tax.name, tax.id).get_slack_object() for tax in
        Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_JOB_LEVEL).order_by('sort_order')
    ]
    
    return SelectMulti(
        'job_search_levels', 'Job Levels', 'Any Level',
        options=job_level_options, initial_option=job_level_selections
    )


def get_remote_work_selection(remote_selection=None):
    default_selection = REMOTE_TYPES.NO.value | REMOTE_TYPES.YES.value
    remote_selection = remote_selection or default_selection
    remote_work_selection_option = InputOption('Any', remote_selection).get_slack_object()
    remote_work_options = [
        InputOption('Any', default_selection).get_slack_object(),
        InputOption('On-site Only', REMOTE_TYPES.NO.value).get_slack_object(),
        InputOption('Remote Only', REMOTE_TYPES.YES.value).get_slack_object()
    ]
    
    return Select(
        'work_remote_type_bit', 'Remote Work Preference', 'Preference',
        remote_work_options,
        initial_option=remote_work_selection_option
    )


def get_home_zip_code_input(current_postal_code=None):
    return InputText(
        'home_post_code',
        'Home Postal Code',
        'Postal Code',
        initial_value=current_postal_code,
        help_text='This is used to find jobs and events close to your location'
    )


def get_job_connections_section_id(job_id):
    return f'job_connections_{job_id}'


job_connection_config = {
    ConnectionTypeBit.HIRING_MEMBER.value: {'text': 'Hiring team', 'star_count': 4},
    ConnectionTypeBit.CURRENT_EMPLOYEE.value: {'text': 'Employee', 'star_count': 3},
    ConnectionTypeBit.FORMER_EMPLOYEE.value: {'text': 'Past employee', 'star_count': 2},
    ConnectionTypeBit.KNOW_EMPLOYEE.value: {'text': 'Knows employee at company', 'star_count': 1}
}


def get_job_connections_section(job_id):
    connection_filter = Q(job_id=job_id) & ~Q(connection_type=ConnectionTypeBit.NO_CONNECTION.value)
    job_connections = EmployerJobConnection.objects.select_related('user').filter(connection_filter).order_by(
        'connection_type')
    if not job_connections:
        return None
    section_text = (
        ':grapes: *JOB CONNECTIONS* :grapes: \n'
        '💡 You are 700% more likely to be hired from a referral! Connect with the people below:\n'
    )
    job_connection_texts = []
    for job_connection in job_connections:
        cfg = job_connection_config[job_connection.connection_type]
        job_connection_texts.append(f'({cfg["text"]}) {job_connection.user.full_name}')
    section_text += '\n'.join(job_connection_texts) + '\n\n'
    return SectionText(section_text, get_job_connections_section_id(job_id)).get_slack_object()


FIRST_NAME_KEY = 'first_name'


def get_first_name_input(initial_value):
    return InputText(
        FIRST_NAME_KEY,
        'First Name',
        'First Name',
        initial_value=initial_value,
    ).get_slack_object()


LAST_NAME_KEY = 'last_name'


def get_last_name_input(initial_value):
    return InputText(
        LAST_NAME_KEY,
        'Last Name',
        'Last Name',
        initial_value=initial_value,
    ).get_slack_object()
