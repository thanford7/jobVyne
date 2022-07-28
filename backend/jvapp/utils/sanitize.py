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
