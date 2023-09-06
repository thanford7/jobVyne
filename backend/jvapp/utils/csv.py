import csv
import logging
from dataclasses import dataclass
from functools import partial
from typing import Iterable

from django.db.transaction import atomic

from jvapp import models
from jvapp.utils.email import get_domain_from_email

logger = logging.getLogger(__name__)

@dataclass
class FieldDefinition:
    model_field: str
    is_key: bool = False
    aliases: Iterable[str] = ()
    default: object = None
    override: object = None
    validate_fn: callable = None

    class InvalidFieldData(Exception):
        pass

    def get_value(self, row, colIndex, original_val=None):
        val = row[colIndex].strip() if 0 <= colIndex < len(row) else original_val
        self.validate_fn and self.validate_fn(val)
        return self.override or val or self.default

def normalize_field_name(s):
    return s.replace('_', '').lower()

def identity(o):
    return o

def create_from_model(model, *args, **kwargs):
    obj = model(*args, **kwargs)
    obj.save()
    return obj

def is_column_match(normalized_header, field_definition):
    normalized_model_field = normalize_field_name(field_definition.model_field)
    if normalized_model_field == normalized_header:
        return True
    for alias in field_definition.aliases:
        if alias == normalized_header:
            return True
    return False


def bulk_load_users(csv_file, employer):
    def email_check(email):
        if employer.email_domains:
            if not get_domain_from_email(email) in employer.email_domains:
                raise FieldDefinition.InvalidFieldData(f'Email {email} not allowed for employer {employer}')
    
    with atomic():
        return bulk_load_objects(csv_file, models.JobVyneUser, [
            FieldDefinition(model_field='email', aliases=['emailaddress'], is_key=True, validate_fn=email_check),
            FieldDefinition(model_field='first_name', aliases=['first']),
            FieldDefinition(model_field='last_name', aliases=['last']),
            FieldDefinition(model_field='phone_number', aliases=['phone']),
            FieldDefinition(model_field='employer', default=employer),
            FieldDefinition(model_field='user_type_bits', override=models.JobVyneUser.USER_TYPE_EMPLOYEE),
        ], instance_create_fn=models.JobVyneUser.objects.create_user)


def bulk_load_objects(csv_file, model, field_definitions, instance_create_fn=None, key_clean_fn=None):
    instance_create_fn = instance_create_fn or partial(create_from_model, model)
    key_clean_fn = key_clean_fn or identity
    dialect = csv.Sniffer().sniff(csv_file.read())
    csv_file.seek(0)

    reader = csv.reader(csv_file, dialect=dialect)
    header_row = next(reader)

    field_map = []  # Mapping of row_index -> field_definition
    for idx, header in enumerate(header_row):
        normalized_header = normalize_field_name(header)
        has_been_matched = False
        for field_definition in field_definitions:
            if has_been_matched:
                break
            if is_column_match(normalized_header, field_definition):
                if field_definition in field_map:
                    raise Exception(f'Field {header} has already been mapped to field {field_definition.model_field}')
                field_map.append(field_definition)
                has_been_matched = True
    unmapped_fields = [fd for fd in field_definitions if fd not in field_map]

    data_rows = [row for row in reader]

    # If there's a key field, identify update rows and update them
    key_idx, key_field = next(((key_idx, fd.model_field) for key_idx, fd in enumerate(field_definitions) if fd.is_key), None)
    if key_field:
        data_rows_by_key = {key_clean_fn(row[key_idx]): row for row in data_rows}
        existing_records = model.objects.filter(**{f'{key_field}__in': data_rows_by_key.keys()})
        for existing_record in existing_records:
            key = getattr(existing_record, key_field)
            update_row = data_rows_by_key[key]
            for idx, field_definition in enumerate(field_definitions):
                if field_definition.model_field != key_field:
                    val = field_definition.get_value(update_row, idx, getattr(existing_record, field_definition.model_field))
                    setattr(existing_record, field_definition.model_field, val)
            data_rows_by_key.pop(key)
            existing_record.save()
        data_rows = list(data_rows_by_key.values())

    for row in data_rows:
        kwargs = {
            fd.model_field: fd.get_value(row, idx)
            for idx, fd in enumerate(field_map)
        }
        # Go through all the unmapped fields because they might provide default or override values
        for unmapped_field in unmapped_fields:
            kwargs[unmapped_field.model_field] = unmapped_field.get_value([], 0)
        instance_create_fn(**kwargs)



