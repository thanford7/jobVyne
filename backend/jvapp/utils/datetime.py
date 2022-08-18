from datetime import datetime


def get_datetime_format_or_none(val):
    """Serialize a date or datetime value if it exists, otherwise return None"""
    if val:
        return val.isoformat()
    return None


def get_datetime_or_none(dateStr, format='%m/%d/%Y %H:%M:%S', asDate=False):
    if not dateStr:
        return None
    dt = datetime.strptime(dateStr, format)
    if asDate:
        return dt.date()
    return dt
