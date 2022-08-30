from collections import Callable
from dataclasses import dataclass


@dataclass
class AttributeCfg:
    form_name: str = None  # If the data field key is different from the object attribute name
    prop_func: Callable = None  # A function that processes the raw form value
    is_protect_existing: bool = False  # If true, prevents setting the object attribute to None
    is_ignore_excluded: bool = True  # If true, doesn't modify the attribute if it's not included in the form data


def set_object_attributes(obj, data: dict, form_cfg: dict):
    for key, attribute_cfg in form_cfg.items():
        attribute_cfg = attribute_cfg or AttributeCfg()
        
        if attribute_cfg.is_ignore_excluded and (attribute_cfg.form_name or key) not in data:
            continue
        
        val = data.get(attribute_cfg.form_name or key)
        if attribute_cfg.prop_func:
            val = attribute_cfg.prop_func(val)
        if val is None and attribute_cfg.is_protect_existing:
            continue
        setattr(obj, key, val)
        
        
def get_list_intersection(list1, list2):
    return list(set(list1) & set(list2))
