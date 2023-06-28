from django.db import models
from django.utils.translation import gettext_lazy as _


class SeparatedValueField(models.CharField):

    description = _("Converts a list to a separated character field based on the separator argument")
    
    def __init__(self, separator, data_type=str, *args, **kwargs):
        self.separator = separator
        self.data_type = data_type  # Defines how to reconstruct the string values from the database
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args.append(self.separator)
        if self.data_type != str:
            kwargs['data_type'] = self.data_type
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return [self.data_type(val) for val in value.split(self.separator)]

    def to_python(self, value):
        if isinstance(value, list):
            return value
    
        if value is None:
            return value
    
        return [self.data_type(val) for val in value.split(self.separator)]

    def get_prep_value(self, value):
        if value is None:
            return value

        # Use sorted to ensure value comparisons are correct
        # e.g. [a, b] == [b, a]
        return self.separator.join([str(val) for val in sorted(value)])
    
    
class LowercaseCharField(models.CharField):

    def get_prep_value(self, value):
        if value is None:
            return value
        
        return str(value).lower()
