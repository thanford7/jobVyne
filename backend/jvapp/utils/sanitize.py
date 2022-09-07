from bleach.css_sanitizer import CSSSanitizer
from bleach.sanitizer import Cleaner

__all__ = ('sanitizer', )

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
