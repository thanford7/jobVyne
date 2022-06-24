
def get_datetime_format_or_none(val):
    """Serialize a date or datetime value if it exists, otherwise return None"""
    if val:
        return val.isoformat()
    return None
