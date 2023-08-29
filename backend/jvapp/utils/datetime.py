import time
from datetime import datetime, timezone
from enum import IntEnum
from math import ceil

import pytz
from dateutil.parser import parse


TIME_INTERVAL_SECONDS = 'seconds'
TIME_INTERVAL_MINUTES = 'minutes'
TIME_INTERVAL_HOURS = 'hours'
TIME_INTERVAL_DAYS = 'days'


# Keep in sync with DAYS_OF_WEEK in datetime.js
class DowBit(IntEnum):
    MON = 1
    TUE = 2
    WED = 4
    THU = 8
    FRI = 16
    SAT = 32
    SUN = 64


WEEKDAY_BITS = (
    DowBit.MON.value |
    DowBit.TUE.value |
    DowBit.WED.value |
    DowBit.THU.value |
    DowBit.FRI.value
)


dow_bit_map = {
    0: DowBit.MON.value,
    1: DowBit.TUE.value,
    2: DowBit.WED.value,
    3: DowBit.THU.value,
    4: DowBit.FRI.value,
    5: DowBit.SAT.value,
    6: DowBit.SUN.value
}


def get_datetime_format_or_none(val, format_str: str = None):
    """Serialize a date or datetime value if it exists, otherwise return None"""
    if val:
        if not format_str:
            return val.isoformat()
        else:
            return val.strftime(format_str)
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


def get_datetime_minutes(target_dt: datetime):
    return target_dt.hour * 60 + target_dt.minute


def get_dow_bit(target_dt: datetime):
    return dow_bit_map[target_dt.weekday()]


def get_datetime_diff(earlier_time: datetime, later_time: datetime, interval=TIME_INTERVAL_SECONDS, round_to=0):
    diff_seconds = (later_time - earlier_time).total_seconds()
    if interval == TIME_INTERVAL_SECONDS:
        return round(diff_seconds, round_to)
    if interval == TIME_INTERVAL_MINUTES:
        return round(diff_seconds / 60, round_to)
    if interval == TIME_INTERVAL_HOURS:
        return round(diff_seconds / (60 * 60), round_to)
    if interval == TIME_INTERVAL_DAYS:
        return round(diff_seconds / (60 * 60 * 24), round_to)
    raise ValueError('Unsupported time interval')
    
