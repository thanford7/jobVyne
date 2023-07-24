import json
import re


class SlackBlock:
    def get_slack_object(self):
        raise NotImplementedError()
    

class Divider(SlackBlock):
    def get_slack_object(self):
        return {'type': 'divider'}


class Modal(SlackBlock):
    MODAL_IDX_SEPARATOR = '--'
    
    def __init__(self, title, callback_id, submit_text, blocks, private_metadata: dict = None, validation_fns: list = None):
        self.title = title
        self.callback_id = callback_id
        self.submit_text = submit_text
        self.blocks = blocks
        self.private_metadata = private_metadata
        self.validation_fns = validation_fns or []
        
    def set_modal_view_idx(self, idx):
        self.callback_id = f'{self.callback_id}{self.MODAL_IDX_SEPARATOR}{idx}'
        
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
        if self.private_metadata:
            slack_object['private_metadata'] = json.dumps(self.private_metadata)
        
        return slack_object
    
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
                elif input_type in (Select.TYPE, SelectExternal.TYPE):
                    val = SelectExternal.get_value(input_dict)
                elif input_type in (InputText.INPUT_TYPE, InputEmail.INPUT_TYPE, InputUrl.INPUT_TYPE, InputNumber.INPUT_TYPE):
                    val = InputText.get_value(input_dict)
                else:
                    val = input_dict['value']
                values[input_key] = val
        return values
    
    
class InputText(SlackBlock):
    INPUT_TYPE = 'plain_text_input'
    
    def __init__(
        self, action_id, label, placeholder,
        initial_value: str = None, is_optional: bool = False,
        is_multiline: bool = False, help_text: str = None,
        is_focused: bool = False
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
        if re.match(f'^{cls.NEW_VALUE_PREPEND}.+?$', text):
            return text.replace(cls.NEW_VALUE_PREPEND, '').strip()
        return text
    
    
class Select(SlackBlock):
    TYPE = 'static_select'
    
    def __init__(self, action_id, label, placeholder, options, focus_on_load=False, initial_option=None, **kwargs):
        self.action_id = action_id
        self.label = label
        self.placeholder = placeholder
        self.options = options
        self.focus_on_load = focus_on_load
        self.initial_option = initial_option

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
        
        if self.initial_option:
            slack_object['element']['initial_option'] = self.initial_option
    
        return slack_object

    @staticmethod
    def get_value(input_dict):
        selected_option = input_dict.get('selected_option')
        if not selected_option:
            return None
        return {
            'text': selected_option['text']['text'],
            'value': selected_option['value']
        }
    
    
class SelectExternal(SlackBlock):
    TYPE = 'external_select'
    
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
        return Select.get_value(input_dict)
        
    
class MultiSelectExternal(SelectExternal):
    TYPE = 'multi_external_select'
    
    def __init__(self, *args, max_selected_items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_selected_items = max_selected_items
        
    def get_slack_object(self):
        slack_object = super().get_slack_object()
        
        if self.max_selected_items:
            slack_object['element']['max_selected_items'] = self.max_selected_items
            
        return slack_object


class SelectEmployer(SelectExternal):
    OPTIONS_LOAD_KEY = 'options-employer'
    
    def __init__(self, *args, focus_on_load=False, **kwargs):
        super().__init__(self.OPTIONS_LOAD_KEY, 'Select employer', 'Select employer', focus_on_load=focus_on_load)
        