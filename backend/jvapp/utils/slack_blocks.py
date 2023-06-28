import json


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
                elif input_type in (InputText.INPUT_TYPE, InputEmail.INPUT_TYPE, InputUrl.INPUT_TYPE):
                    val = InputText.get_values(input_dict)
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
    def get_values(input_dict):
        return input_dict['value']


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
    def __init__(self, label, value, description: str = None):
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
        