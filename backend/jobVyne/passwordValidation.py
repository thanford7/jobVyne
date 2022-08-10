import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class LowercaseCharValidator:

    def validate(self, password, user=None):
        if not re.search('[a-z]', password):
            raise ValidationError(
                _("This password must contain at least one lowercase character."),
                code='no_lowercase_char',
            )


class UppercaseCharValidator:

    def validate(self, password, user=None):
        if not re.search('[A-Z]', password):
            raise ValidationError(
                _("This password must contain at least one uppercase character."),
                code='no_uppercase_char',
            )


class NumberValidator:

    def validate(self, password, user=None):
        if not re.search('[0-9]', password):
            raise ValidationError(
                _("This password must contain at least one number."),
                code='no_number',
            )


class SymbolValidator:

    def validate(self, password, user=None):
        if not re.search('[^A-Za-z0-9]', password):
            raise ValidationError(
                _("This password must contain at least one symbol."),
                code='no_symbol',
            )
        
        
class WhitespaceValidator:

    def validate(self, password, user=None):
        if re.search('\s', password):
            raise ValidationError(
                _("This password cannot contain any whitespace."),
                code='has_whitespace',
            )
