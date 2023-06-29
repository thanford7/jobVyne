import re

from html_sanitizer import Sanitizer
from html_sanitizer.sanitizer import bold_span_to_strong, italic_span_to_em, tag_replacer, target_blank_noopener

__all__ = ('sanitize_html',)

text_align_class_map = {
    'left': 'text-left',
    'center': 'text-center',
    'right': 'text-right'
}


def _get_style_value(element, style_key):
    style = element.get('style')
    if not style or (style_key not in style):
        return None
    style_val = next((s for s in style.split(';') if style_key in s), None)
    if style_val is None:
        return None
    return style_val.split(':')[1].strip()


def text_align_to_class_sanitizer(element):
    text_alignment = _get_style_value(element, 'text-align')
    if text_alignment is None:
        return element
    
    alignment_class = text_align_class_map.get(text_alignment)
    if not alignment_class:
        return element
    
    element.classes.add(alignment_class)
    return element


def font_size_to_header_sanitizer(element):
    font_size_px = _get_style_value(element, 'font-size')
    if font_size_px is None:
        return element
    if 'px' not in font_size_px:
        return element

    font_size = float(font_size_px.replace('px', '').replace('!important', '').strip())
    if font_size >= 16:
        element.tag = 'h6'
    else:
        element.tag = 'p'

    return element


def font_weight_sanitizer(element):
    font_weight = _get_style_value(element, 'font-weight')
    if font_weight is None:
        return element
    try:
        font_weight = int(font_weight)
        if font_weight >= 400:
            element.tag = 'strong'
    except ValueError:
        if font_weight in ('bold', 'bolder'):
            element.tag = 'strong'
    
    return element


def header_size_reducer_sanitizer(element):
    if element.tag in ('h1', 'h2', 'h3', 'h4', 'h5'):
        element.tag = 'h6'

    return element


def secure_link_sanitizer(element):
    if element.tag == 'a' and (href := element.attrib.get('href')):
        link_match = re.match('^((?P<protocol>.*?)://)?(?P<link>.*?)$', href)
        if link_match:
            protocol = link_match.group('protocol')
            link = link_match.group('link')
    
            # If there is no protocol or the protocol is insecure, make it secure
            # Only update for no protocol or http. Other protocols like mail should be left alone
            if not protocol or protocol == 'http':
                element.attrib['href'] = f'https://{link}'
        element.attrib['target'] = '_blank'
    
    return element

allowed_tags = {
    'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'b', 'i', 'u', 'p', 'ul', 'ol',
    'li', 'br', 'sub', 'sup', 'hr', 'div', 'span', 'blockquote', 'font', 'strong'
}
allowed_attributes = {
    'a': ('href', 'name', 'target', 'title', 'id', 'rel'),  # Default setting
}
for el in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'div', 'span', 'font'):
    allowed_attributes[el] = ('class',)

default_sanitizer_cfg = {
    'tags': allowed_tags,
    'attributes': allowed_attributes,
    'add_nofollow': True,
    'separate': ('br', 'li'),
    'element_preprocessors': [
        bold_span_to_strong,
        italic_span_to_em,
        tag_replacer('b', 'strong'),
        tag_replacer('i', 'em'),
        tag_replacer('form', 'p'),
        tag_replacer('font', 'span'),
        target_blank_noopener,
        text_align_to_class_sanitizer,
        font_size_to_header_sanitizer,
        font_weight_sanitizer,
        header_size_reducer_sanitizer,
        secure_link_sanitizer
    ],
}


def get_sanitizer(cfg_override=None, add_element_preprocessors=None):
    cfg_override = cfg_override or {}
    sanitizer_cfg = {**default_sanitizer_cfg, **cfg_override}
    if add_element_preprocessors:
        sanitizer_cfg['element_preprocessors'] += add_element_preprocessors
    return Sanitizer(sanitizer_cfg)

default_sanitizer = get_sanitizer(
    cfg_override={
        'separate': {'br', 'li', 'p'},
        'empty': {'p'},
        'keep_typographic_whitespace': True
    },
    add_element_preprocessors=[tag_replacer('div', 'p')]
)


def sanitize_html(html_text, is_email=False, sanitizer=default_sanitizer):
    if is_email:
        # New lines are not honored in html interpreters like email
        html_text = html_text.replace('\n', '<br/>')
    return sanitizer.sanitize(html_text)
