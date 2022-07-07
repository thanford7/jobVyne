

def set_object_attributes(obj, data: dict, key_func_dict: dict):
    for key, prop_helpers in key_func_dict.items():
        form_name = None
        prop_func = None
        is_protect_existing = False
        is_ignore_excluded = False
        if prop_helpers:
            form_name = prop_helpers.get('form_name')
            prop_func = prop_helpers.get('prop_func')
            is_protect_existing = prop_helpers.get('is_protect_existing')
            is_ignore_excluded = prop_helpers.get('is_ignore_excluded')

        if is_ignore_excluded and (form_name or key) not in data:
            continue

        val = data.get(form_name or key)
        if prop_func:
            val = prop_func(val)
        if val is None and is_protect_existing:
            continue
        setattr(obj, key, val)
