__all__ = ['compensation_data_template', 'parse_compensation_text', 'merge_compensation_data']


import re
from functools import reduce

from jvapp.models.currency import currencies, currency_lookup
from jvapp.utils.sanitize import sanitize_html

# Example -- Minimum: $157,300.00 Maximum: $344,200.00
CURRENCY_RANGE_MAX_CHAR_COUNT = 10


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
    currency_pattern = reduce(lambda full_pattern, currency: f'{full_pattern}{"|" if full_pattern else ""}{currency}', currencies, '')
    currency_match = re.search(f'({currency_pattern})\s', text)
    bad_salary_floor = 40000 if salary_interval == 'year' else 1
    bad_salary_ceiling = 500000
    grouped_compensation_matches = get_grouped_compensation_matches(text, bad_salary_floor, bad_salary_ceiling)
    best_compensation_match = get_best_compensation_group(grouped_compensation_matches, bad_salary_floor, bad_salary_ceiling)
    currency = None
    if best_compensation_match and best_compensation_match['currency']:
        currency = currency_lookup.get(best_compensation_match['currency'], None)
    elif currency_match:
        currency = currency_match.group(0).strip()
    if not all((best_compensation_match, currency)):
        return {**compensation_data_template}

    return {
        'salary_interval': salary_interval,
        'salary_currency': currency,
        'salary_floor': best_compensation_match['salary'][0],
        'salary_ceiling': best_compensation_match['salary'][-1]
    }


def get_best_compensation_group(compensation_groups, bad_salary_floor, bad_salary_ceiling):
    possible_matches = [
        g for g in compensation_groups
        if g['salary'][0] > bad_salary_floor and g['salary'][-1] < bad_salary_ceiling
    ]
    possible_matches.sort(key=lambda x: (bool(x['currency']), len(x['salary'])), reverse=True)
    return possible_matches[0] if possible_matches else None


def get_salary_for_group(group):
    if len(group) == 1:
        return {
            'salary': [get_salary_from_match(group[0])],
            'group': group,
            'currency': group[0].group('currency')
        }
    else:
        has_thousand_marker = bool(len([g for g in group if g.group('thousand_marker')]))
        return {
            'salary': [get_salary_from_match(g, has_thousand_marker=has_thousand_marker) for g in group],
            'group': group,
            'currency': next((g.group('currency') for g in group if g.group('currency')), None)
        }


def is_good_salary_range(salary_group_data, min_salary, max_salary):
    salary = salary_group_data['salary']
    group = salary_group_data['group']
    if len(salary) == 1:
        is_good_salary = salary[0] <= max_salary and salary[0] >= min_salary
        if not is_good_salary:
            group = []
        return is_good_salary, group
    
    if salary[1] < salary[0]:
        return False, group[1:]
    is_good_min_salary = salary[0] <= max_salary and salary[0] >= min_salary
    is_good_max_salary = salary[1] <= max_salary and salary[1] >= min_salary
    if (not is_good_min_salary) and (not is_good_max_salary):
        return False, []
    if not is_good_min_salary:
        return False, group[1:]
    if not is_good_max_salary:
        return False, group[:1]
    return True, group


def get_grouped_compensation_matches(text, min_salary, max_salary):
    compensation_pattern = f'(?P<currency>{currency_characters})?\s?(?P<first_numbers>[0-9]+((\.?[0-9]+)|([0-9]*?))),?(?P<second_numbers>[0-9]+(\.?[0-9]+)?)?\s?(?P<thousand_marker>[kK])?'
    compensation_matches = list(re.finditer(compensation_pattern, text))
    groups = []
    combined_group = []
    last_end_position = 0
    for idx, match in enumerate(compensation_matches):
        if idx != 0 and (len(combined_group) == 2 or match.start() - CURRENCY_RANGE_MAX_CHAR_COUNT > last_end_position):
            salary = get_salary_for_group(combined_group)
            is_good_salary, updated_group = is_good_salary_range(salary, min_salary, max_salary)
            if is_good_salary:
                groups.append(combined_group)
                combined_group = [match]
            else:
                combined_group = updated_group
                combined_group.append(match)
        else:
            combined_group.append(match)
        if idx == len(compensation_matches) - 1:
            groups.append(combined_group)
        last_end_position = match.end()
    
    salary_groups = []
    for group in groups:
        if not group:
            continue
        salary_groups.append(get_salary_for_group(group))
            
    return salary_groups
    

def get_salary_from_match(match, has_thousand_marker=False):
    try:
        salary = float(match.group('first_numbers') + (match.group('second_numbers') or ''))
    except ValueError:
        return 0
    if match.group('thousand_marker') or has_thousand_marker:
        salary *= 1000
    return salary


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
