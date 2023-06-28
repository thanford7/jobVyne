import re
from collections.abc import Callable
from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass
class AttributeCfg:
    form_name: str = None  # If the data field key is different from the object attribute name
    prop_func: Callable = None  # A function that processes the raw form value
    is_protect_existing: bool = False  # If true, prevents setting the object attribute to None
    is_ignore_excluded: bool = True  # If true, doesn't modify the attribute if it's not included in the form data
    is_empty_to_none: bool = True


def set_object_attributes(obj: object, data: dict, form_cfg: dict):
    for key, attribute_cfg in form_cfg.items():
        attribute_cfg = attribute_cfg or AttributeCfg()
        
        if attribute_cfg.is_ignore_excluded and (attribute_cfg.form_name or key) not in data:
            continue
        
        val = data.get(attribute_cfg.form_name or key)
        if attribute_cfg.prop_func:
            val = attribute_cfg.prop_func(val)
        if attribute_cfg.is_empty_to_none and isinstance(val, str) and not val:
            val = None
        if val is None and attribute_cfg.is_protect_existing:
            continue
        setattr(obj, key, val)
        
        
def get_list_intersection(list1, list2):
    return list(set(list1) & set(list2))


def obfuscate_string(text, allowed_chars=5):
    if not text:
        return text
    allowed_chars = min(allowed_chars, len(text))
    cut_off = len(text) - allowed_chars
    return '*' * (cut_off) + text[cut_off:]


def is_obfuscated_string(text, allowed_chars=5):
    obs_text = obfuscate_string(text, allowed_chars=allowed_chars)
    return obs_text == text


def coerce_bool(val):
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    try:
        val = int(val)
        return val != 0
    except ValueError:
        pass
    if isinstance(val, str):
        return val.lower() == 'true'
    
    raise ValueError(f'Unknown boolean val: {val}')


def coerce_int(val, default=None, is_raise_error=False):
    try:
        return int(val)
    except (ValueError, TypeError) as e:
        if is_raise_error:
            raise e
        return default


def coerce_float(val, default=None, is_raise_error=False):
    try:
        return float(val)
    except (ValueError, TypeError) as e:
        if is_raise_error:
            raise e
        return default
    

def round_to(num, round_num):
    return round(num / round_num) * round_num


def get_base_url(url):
    if not url:
        return url
    
    split_url = urlsplit(url)
    return f'{split_url.scheme}://{split_url.netloc}'


def capitalize(text, is_every_word=True):
    if not text:
        return text
    
    last_char = None
    new_text = ''
    for char in text:
        if not last_char or (is_every_word and re.match('\s', last_char or '')):
            new_text += char.upper()
        else:
            new_text += char.lower()
        last_char = char
    
    return new_text


def get_website_domain_from_url(url):
    if not url:
        return None
    url_groups = url.split('.')
    if len(url_groups) >= 2:
        return '.'.join(url_groups[-2:])
    return None
