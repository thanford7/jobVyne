import csv
from dataclasses import dataclass
from typing import Iterable

from jvapp import models


@dataclass
class FieldDefinition:
    model_field: str
    is_key: bool = False
    aliases: Iterable[str] = ()
    default: object = None
    override: object = None

    def get_value(self, row, colIndex, original_val):
        if 0 <= colIndex < len(row):
            return row[colIndex] or self.default
        return self.override or original_val or self.default


def normalize(s):
    return s.replace('_', '').lower()


def is_column_match(normalized_header, field_definition):
    normalized_model_field = normalize(field_definition.model_field)
    if normalized_model_field == normalized_header:
        return True
    for alias in field_definition.aliases:
        if alias == normalized_header:
            return True
    return False


def bulk_load_users(csv_file, employer):
    return bulk_load_objects(csv_file, models.JobVyneUser, [
        FieldDefinition(model_field='email', aliases=['emailaddress'], is_key=True),
        FieldDefinition(model_field='first_name', aliases=['first']),
        FieldDefinition(model_field='last_name', aliases=['last']),
        FieldDefinition(model_field='employer', default=employer),
    ])


def bulk_load_objects(csv_file, model, field_definitions):
    dialect = csv.Sniffer().sniff(csv_file.read())
    csv_file.seek(0)

    reader = csv.reader(csv_file, dialect=dialect)
    header_row = next(reader)

    field_map = []  # Mapping of row_index -> field_definition
    for idx, header in enumerate(header_row):
        normalized_header = normalize(header)
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

    new_records = [
        model(**{field_def.model_field: field_def.get_value(row, i, None) or field_definition.default for i, field_def in enumerate(field_map + unmapped_fields)})
        for row in reader
    ]

    # If there's a key field, identify those objects and update (rather than create) them
    key_field = next((fd.model_field for fd in field_definitions if fd.is_key), None)
    if key_field:
        objects_by_key = {getattr(o, key_field): o for o in new_records}
        existing_records = model.objects.filter(**{f'{key_field}__in': objects_by_key.keys()})
        for existing_records in existing_records:
            key = getattr(existing_records, key_field)
            new = objects_by_key[key]
            for field_definition in field_definitions:
                if field_definition.model_field != key_field:
                    val = field_definition.get_value([], -1, getattr(new, field_definition.model_field))
                    setattr(existing_records, field_definition.model_field, val)
            objects_by_key.pop(key)
            existing_records.save()
        # model.objects.bulk_update(existing_records, (fd.model_field for fd in field_definitions if not fd.is_key))
        new_records = list(objects_by_key.values())

    # model.objects.bulk_create(new_records)
    for new_record in new_records:
        new_record.save()


