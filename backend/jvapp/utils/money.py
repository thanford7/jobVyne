__all__ = ['compensation_data_template', 'parse_compensation_text', 'merge_compensation_data']


import re
from functools import reduce

from jvapp.models.currency import currencies, currency_lookup
from jvapp.utils.sanitize import sanitize_html


currency_characters = u'[$¢£¤¥֏؋৲৳৻૱௹฿៛\u20a0-\u20bd\ua838\ufdfc\ufe69\uff04\uffe0\uffe1\uffe5\uffe6]'
compensation_data_template = {
    'salary_currency': None,
    'salary_floor': None,
    'salary_ceiling': None,
    'salary_interval': None
}


def parse_compensation_text(text, salary_interval='year'):
    if not text:
        return {**compensation_data_template}
    text = sanitize_html(text)
    compensation_pattern = f'(?P<currency>{currency_characters})?\s?(?P<first_numbers>[0-9]+((\.?[0-9]+)|([0-9]*?))),?(?P<second_numbers>[0-9]+)?\s?(?P<thousand_marker>[kK])?'
    compensation_matches = list(re.finditer(compensation_pattern, text))
    currency_pattern = reduce(lambda full_pattern, currency: f'{full_pattern}{"|" if full_pattern else ""}{currency}', currencies, '')
    currency_match = re.search(f'({currency_pattern})\s', text)
    first_match = False
    compensation_data = {'salary_interval': salary_interval}
    for idx, compensation_match in enumerate(compensation_matches):
        currency_symbol = compensation_match.group('currency') or ''
        currency_symbol = currency_symbol.strip()
        if not (currency_symbol or first_match):
            continue

        has_thousand_marker = False
        if (idx + 1) < len(compensation_matches):
            has_thousand_marker = is_next_match_thousand_marker(compensation_match, compensation_matches[idx + 1])
        salary = get_salary_from_match(compensation_match, has_thousand_marker=has_thousand_marker)
        # Some monetary matches may be for things like company valuations. Avoid using
        # erroneous values for salary
        bad_salary_floor = 10000 if salary_interval == 'year' else 1
        if (salary < bad_salary_floor) or (salary > 500000):
            continue
        if not first_match:
            compensation_data['salary_floor'] = salary
            if currency_match:
                compensation_data['salary_currency'] = currency_match.group(0).strip()
            elif currency_symbol:
                compensation_data['salary_currency'] = currency_lookup.get(currency_symbol, None)
            first_match = True
        else:
            compensation_data['salary_ceiling'] = salary
            return compensation_data
    
    # If there is only a salary floor, it means there is not a range, only a single value
    if salary_floor := compensation_data.get('salary_floor'):
        compensation_data['salary_ceiling'] = salary_floor
        return compensation_data
    
    return {**compensation_data_template}


def get_salary_from_match(match, has_thousand_marker=False):
    salary = float(match.group('first_numbers') + (match.group('second_numbers') or ''))
    if match.group('thousand_marker') or has_thousand_marker:
        salary *= 1000
    return salary


def is_next_match_thousand_marker(first_match, second_match):
    # Example $170-220K
    is_close_character_distance = first_match.end() >= (second_match.start() - 4)
    if not is_close_character_distance:
        return False
    return bool(second_match.group('thousand_marker'))


def merge_compensation_data(compensation_data_sets: list):
    """Merge compensation data with preference for later data sets
    """
    compensation_data = {**compensation_data_template}
    for data_set in compensation_data_sets:
        for compensation_key in ('salary_currency', 'salary_floor', 'salary_ceiling', 'salary_interval'):
            val = data_set.get(compensation_key)
            if not val:
                continue
            compensation_data[compensation_key] = val

    return compensation_data
