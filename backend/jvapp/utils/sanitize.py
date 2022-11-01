import re

from html_sanitizer import Sanitizer
from html_sanitizer.sanitizer import bold_span_to_strong, italic_span_to_em, tag_replacer, target_blank_noopener

__all__ = ('sanitize_html',)


def font_size_to_header_sanitizer(element):
    style = element.get('style')
    if not style or ('font-size' not in style):
        return element

    font_size_style = next((s for s in style.split(';') if 'font-size' in s), None)
    font_size_px = font_size_style.split(':')[1].strip()
    if 'px' not in font_size_px:
        return element

    font_size = float(font_size_px.replace('px', '').strip())
    if font_size >= 16:
        element.tag = 'h6'
    else:
        element.tag = 'p'

    return element


def font_weight_sanitizer(element):
    style = element.get('style')
    if not style or ('font-weight' not in style):
        return element

    font_weight_style = next((s for s in style.split(';') if 'font-weight' in s), None)
    font_weight = int(font_weight_style.split(':')[1].strip())
    if font_weight >= 400:
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


sanitizer = Sanitizer({
    'tags': allowed_tags,
    'attributes': allowed_attributes,
    'add_nofollow': True,
    'element_preprocessors': [
        bold_span_to_strong,
        italic_span_to_em,
        tag_replacer('b', 'strong'),
        tag_replacer('i', 'em'),
        tag_replacer('form', 'p'),
        tag_replacer('font', 'span'),
        target_blank_noopener,
        font_size_to_header_sanitizer,
        font_weight_sanitizer,
        header_size_reducer_sanitizer,
        secure_link_sanitizer
    ],
})


def sanitize_html(html_text):
    return sanitizer.sanitize(html_text)
