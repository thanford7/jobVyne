import time
from datetime import datetime, timezone

import pytz
from dateutil.parser import parse


def get_datetime_format_or_none(val):
    """Serialize a date or datetime value if it exists, otherwise return None"""
    if val:
        return val.isoformat()
    return None


def get_datetime_or_none(dateStr, format='%m/%d/%Y %H:%M:%S%z', as_date=False):
    if not dateStr:
        return None
    try:
        dt = parse(dateStr)
    except ValueError:
        try:
            dt = datetime.strptime(dateStr, format)
        except ValueError:
            dt = datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%S.%fZ')  # This is the format of native JavaScript dates
    if as_date:
        return dt.date()
    return dt


def get_current_datetime(tz=pytz.UTC):
    return datetime.now(tz=tz)


def get_unix_datetime(date_time: datetime):
    return int(time.mktime(date_time.timetuple()))


def get_datetime_from_unix(unix_time, is_in_ms=False):
    unix_time = int(unix_time)
    if is_in_ms:
        unix_time /= 1000
    return datetime.fromtimestamp(unix_time, tz=timezone.utc)
