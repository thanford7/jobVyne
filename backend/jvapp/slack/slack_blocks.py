import json
import re

from django.db.models import Q
from django.utils import timezone

from jvapp.models import JobVyneUser
from jvapp.models.employer import EmployerJob
from jvapp.utils.data import coerce_int


class SlackBlock:
    def get_slack_object(self):
        raise NotImplementedError()


class Divider(SlackBlock):
    def get_slack_object(self):
        return {'type': 'divider'}


class Modal(SlackBlock):
    
    def __init__(
        self, title, callback_id, submit_text, blocks,
        is_final=False, metadata: dict = None, validation_fns: list = None, process_data_fn: callable = None
    ):
        self.title = title
        self.callback_id = callback_id
        self.submit_text = submit_text
        self.blocks = blocks
        self.is_final = is_final
        self.metadata = metadata
        self.validation_fns = validation_fns or []
        self.process_data_fn = process_data_fn
    
    def get_slack_object(self):
        slack_object = {
            'type': 'modal',
            'callback_id': self.callback_id,
            'title': {
                'type': 'plain_text',
                'text': self.title
            },
            'blocks': self.blocks
        }
        
        if self.submit_text:
            slack_object['submit'] = {
                'type': 'plain_text',
                'text': self.submit_text
            }
        if self.metadata:
            slack_object['private_metadata'] = json.dumps(self.metadata)
        
        return slack_object
    
    def process_data(self, user: JobVyneUser):
        if not self.process_data_fn:
            return
        self.process_data_fn(user, self.metadata)
    
    def get_modal_errors(self, form_data):
        errors = []
        for validation_fn in self.validation_fns:
            if error := validation_fn(form_data):
                errors.append(error)
        if not errors:
            return None
        return {
            'response_action': 'errors',
            'errors': {
                error_key: error_message for error_key, error_message in errors
            }
        }
    
    @staticmethod
    def get_modal_values(data):
        values = {}
        for value_dict in list(data['view']['state']['values'].values()):
            for input_key, input_dict in value_dict.items():
                input_type = input_dict['type']
                if input_type == 'checkboxes':
                    val = InputCheckbox.get_values(input_dict)
                elif input_type == Select.TYPE:
                    val = Select.get_value(input_dict)
                elif input_type == SelectExternal.TYPE:
                    val = SelectExternal.get_value(input_dict)
                elif input_type == SelectMulti.TYPE:
                    val = SelectMulti.get_value(input_dict)
                elif input_type == SelectMultiExternal.TYPE:
                    val = SelectMultiExternal.get_value(input_dict)
                elif input_type in (
                InputText.INPUT_TYPE, InputEmail.INPUT_TYPE, InputUrl.INPUT_TYPE, InputNumber.INPUT_TYPE):
                    val = InputText.get_value(input_dict)
                else:
                    val = input_dict['value']
                values[input_key] = val
        return values


class SectionText(SlackBlock):
    def __init__(self, text):
        self.text = text
    
    def get_slack_object(self):
        return {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': self.text
            }
        }


class InputText(SlackBlock):
    INPUT_TYPE = 'plain_text_input'
    
    def __init__(
            self, action_id, label, placeholder,
            initial_value: str = None, is_optional: bool = False,
            is_multiline: bool = False, help_text: str = None,
            is_focused: bool = False, max_length: int = None
    ):
        self.action_id = action_id
        self.label = label
        self.placeholder = placeholder
        
        if (initial_value is not None) and (not isinstance(initial_value, str)):
            initial_value = str(initial_value)
        self.initial_value = initial_value
        
        self.is_optional = is_optional
        self.is_multiline = is_multiline
        self.help_text = help_text
        self.is_focused = is_focused
        self.max_length = max_length
    
    def get_slack_object(self):
        slack_object = {
            'type': 'input',
            'label': {
                'type': 'plain_text',
                'text': self.label
            },
            'element': {
                'type': self.INPUT_TYPE,
                'action_id': self.action_id,
                'placeholder': {
                    'type': 'plain_text',
                    'text': self.placeholder
                },
                'focus_on_load': self.is_focused
            }
        }
        
        if self.is_optional:
            slack_object['optional'] = self.is_optional
        if self.is_multiline:
            slack_object['element']['multiline'] = self.is_multiline
        if self.initial_value:
            slack_object['element']['initial_value'] = self.initial_value
        if self.max_length:
            slack_object['element']['max_length'] = self.max_length
        if self.help_text:
            slack_object['hint'] = {
                'type': 'plain_text',
                'text': self.help_text
            }
        
        return slack_object
    
    @staticmethod
    def get_value(input_dict):
        return input_dict.get('value')


class InputNumber(InputText):
    INPUT_TYPE = 'number_input'
    
    def __init__(self, *args, is_decimal_allowed=False, min_value=None, max_value=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_decimal_allowed = is_decimal_allowed
        self.min_value = min_value
        self.max_value = max_value
    
    def get_slack_object(self):
        slack_object = super().get_slack_object()
        slack_object['element']['is_decimal_allowed'] = self.is_decimal_allowed
        if self.min_value is not None:
            slack_object['element']['min_value'] = str(self.min_value)
        if self.max_value is not None:
            slack_object['element']['max_value'] = str(self.max_value)
        
        return slack_object


class InputEmail(InputText):
    INPUT_TYPE = 'email_text_input'


class InputUrl(InputText):
    INPUT_TYPE = 'url_text_input'


class InputCheckbox(SlackBlock):
    INPUT_TYPE = 'checkboxes'
    
    def __init__(self, action_id, label, options, initial_option_values: list[str] = None, is_optional: bool = False):
        self.action_id = action_id
        self.label = label
        self.options = options
        self.initial_option_values = initial_option_values
        self.is_optional = is_optional
    
    def get_slack_object(self):
        slack_object = {
            'type': 'input',
            'element': {
                'type': 'checkboxes',
                'options': self.options,
                'action_id': self.action_id
            },
            'label': {
                'type': 'plain_text',
                'text': self.label,
            },
            'optional': self.is_optional
        }
        
        if self.initial_option_values:
            slack_object['element']['initial_options'] = [
                opt for opt in self.options if opt['value'] in self.initial_option_values
            ]
        
        return slack_object
    
    @staticmethod
    def get_values(input_dict):
        selected_option_dicts = input_dict['selected_options']
        selected_options = []
        for selected_option_dict in selected_option_dicts:
            selected_options.append(selected_option_dict['value'])
        
        return selected_options


class InputOption(SlackBlock):
    NEW_VALUE_KEY = 'value-new'
    NEW_VALUE_PREPEND = '(New) '
    
    def __init__(self, label, value, description: str = None):
        if not isinstance(value, str):
            value = str(value)
        self.label = label
        self.value = value
        self.description = description
    
    def get_slack_object(self):
        slack_object = {
            'text': {
                'type': 'plain_text',
                'text': self.label,
            },
            'value': self.value
        }
        
        if self.description:
            slack_object['description'] = {
                'type': 'plain_text',
                'text': self.description
            }
        
        return slack_object
    
    @classmethod
    def parse_value_text(cls, text):
        if text.startswith(cls.NEW_VALUE_PREPEND):
            return text.replace(cls.NEW_VALUE_PREPEND, '').strip()
        return text


class Select(SlackBlock):
    TYPE = 'static_select'
    
    def __init__(
            self, action_id, label, placeholder, options,
            focus_on_load=False, initial_option=None, is_optional=False, **kwargs
    ):
        self.action_id = action_id
        self.label = label
        self.placeholder = placeholder
        self.options = options
        self.focus_on_load = focus_on_load
        self.initial_option = initial_option
        self.is_optional = is_optional
    
    def get_slack_object(self):
        slack_object = {
            'type': 'input',
            'label': {
                'type': 'plain_text',
                'text': self.label,
                'emoji': True
            },
            'element': {
                'type': self.TYPE,
                'action_id': self.action_id,
                'placeholder': {
                    'type': 'plain_text',
                    'text': self.placeholder
                },
                'options': self.options,
                'focus_on_load': self.focus_on_load
            }
        }
        self.add_initial_option(slack_object)
        if self.is_optional:
            slack_object['optional'] = self.is_optional
        return slack_object
    
    def add_initial_option(self, slack_object):
        if self.initial_option:
            slack_object['element']['initial_option'] = self.initial_option
    
    @staticmethod
    def get_value(input_dict):
        selected_option = input_dict.get('selected_option')
        if not selected_option:
            return None
        return {
            'text': selected_option['text']['text'],
            'value': selected_option['value']
        }


class SelectMulti(Select):
    TYPE = 'multi_static_select'
    
    def __init__(self, *args, max_selected_items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_selected_items = max_selected_items
    
    def get_slack_object(self):
        slack_object = super().get_slack_object()
        if self.max_selected_items:
            slack_object['element']['max_selected_items'] = self.max_selected_items
        
        return slack_object
    
    def add_initial_option(self, slack_object):
        if self.initial_option:
            slack_object['element']['initial_options'] = self.initial_option
    
    @staticmethod
    def get_value(input_dict):
        selected_options = input_dict.get('selected_options')
        if not selected_options:
            return None
        return [
            {
                'text': selected_option['text']['text'],
                'value': selected_option['value']
            } for selected_option in selected_options
        ]


class SelectExternal(SlackBlock):
    TYPE = 'external_select'
    OPTIONS_LIMIT = 100
    
    def __init__(self, action_id, label, placeholder, min_query_length=3, focus_on_load=False, **kwargs):
        self.action_id = action_id
        self.label = label
        self.placeholder = placeholder
        self.min_query_length = min_query_length
        self.focus_on_load = focus_on_load
    
    def get_slack_object(self):
        slack_object = {
            'type': 'input',
            'label': {
                'type': 'plain_text',
                'text': self.label,
                'emoji': True
            },
            'element': {
                'type': self.TYPE,
                'action_id': self.action_id,
                'placeholder': {
                    'type': 'plain_text',
                    'text': self.placeholder
                },
                'min_query_length': self.min_query_length,
                'focus_on_load': self.focus_on_load
            }
        }
        
        return slack_object
    
    @staticmethod
    def get_value(input_dict):
        val = Select.get_value(input_dict)
        # External select allows user entered values so we need to clean it up
        val['text'] = InputOption.parse_value_text(val['text'])
        return val


class SelectMultiExternal(SelectExternal):
    TYPE = 'multi_external_select'
    
    def __init__(self, *args, max_selected_items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_selected_items = max_selected_items
    
    def get_slack_object(self):
        slack_object = super().get_slack_object()
        
        if self.max_selected_items:
            slack_object['element']['max_selected_items'] = self.max_selected_items
        
        return slack_object
    
    @staticmethod
    def get_value(input_dict):
        values = SelectMulti.get_value(input_dict)
        # External select allows user entered values so we need to clean it up
        for val in values:
            val['text'] = InputOption.parse_value_text(val['text'])
        return values


class SelectEmployer(SelectExternal):
    OPTIONS_LOAD_KEY = 'options-employer'
    
    def __init__(self, *args, focus_on_load=False, **kwargs):
        super().__init__(self.OPTIONS_LOAD_KEY, 'Select employer', 'Select employer', focus_on_load=focus_on_load)
        
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
            focus_on_load=focus_on_load, min_query_length=0
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
