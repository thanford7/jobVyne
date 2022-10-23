import re

from bleach.css_sanitizer import CSSSanitizer
from bleach.html5lib_shim import Filter
from bleach.sanitizer import Cleaner

__all__ = ('sanitize_html', 'REDUCE_H_TAG_MAP')


REDUCE_H_TAG_MAP = {'h1': 'h6', 'h2': 'h6', 'h3': 'h6', 'h4': 'h6', 'h5': 'h6'}


class SizeFilter(Filter):
    def __iter__(self):
        for token in Filter.__iter__(self):
            if token['type'] in ['StartTag', 'EmptyTag'] and token['style']:
                print(token)  # TODO: Update this to look at font-size in style
            yield token

# https://bleach.readthedocs.io/en/latest/clean.html#allowed-tags-tags
# Needs to align with frontend sanitization cfg (WysiwygEditor.vue)
sanitization_cfg = {
    'tags': [
        'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'b', 'i', 'u', 'p', 'ul', 'ol',
        'li', 'br', 'sub', 'sup', 'hr', 'div', 'span', 'blockquote'
    ],
    'attributes': {
        '*': ['class', 'style'],
        'a': ['href', 'name', 'target', 'title', 'id', 'rel'],
    },
    'css_sanitizer': CSSSanitizer(),
    'strip': True
}

sanitizer = Cleaner(**sanitization_cfg)


def sanitize_html(html_text, replace_tag_map=None):
    text = sanitizer.clean(html_text)
    if replace_tag_map:
        text = get_replace_tag_html(text, replace_tag_map)
    
    return make_links_secure(text)


def get_replace_tag_html(html_text: str, tag_map: dict):
    """
    :param tag_map: Should be in the form {<tag to be replaced>: <tag to replace with>}
        example: {h1: b}
    """
    
    for tag, tag_to_replace in tag_map.items():
        opening_tag = f'<{tag}>'
        opening_replace_tag = f'<{tag_to_replace}>'
        closing_tag = f'</{tag}>'
        closing_replace_tag = f'</{tag_to_replace}>'
        
        html_text = html_text.replace(opening_tag, opening_replace_tag)
        html_text = html_text.replace(closing_tag, closing_replace_tag)
        
    return html_text


def make_links_secure(html_text: str):
    return re.sub('href="(?P<link>.*?)"', make_secure_link, html_text)


def make_secure_link(re_match):
    link = re_match.group('link')
    if not link:
        return 'href=""'
    
    link_protocol = re.match('^(?P<protocol>.*?)://', link)
    
    # If there is no protocol or the protocol is insecure, make it secure
    if not link_protocol or link_protocol == 'http':
        return f'href="https://{link}"'
    
    # This could be something like a mail protocol so keep as is
    return f'href="{link}"'
