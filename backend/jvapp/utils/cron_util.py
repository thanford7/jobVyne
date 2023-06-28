import datetime
from dataclasses import dataclass
from typing import Union

from jvapp.utils.data import round_to
from jvapp.utils.datetime import get_current_datetime


@dataclass
class CronPattern:
    year: Union[int, None]
    month: Union[int, None]
    day: Union[int, None]
    hour: Union[int, None]
    minute: Union[int, None]
    
    def is_match(self, target_dt):
        return all([
            ((self.year is None) or self.year == target_dt.year),
            ((self.month is None) or self.month == target_dt.month),
            ((self.day is None) or self.day == target_dt.day),
            ((self.hour is None) or self.hour == target_dt.hour),
            ((self.minute is None) or self.minute == target_dt.minute),
        ])


def get_seconds_to_next_minute_interval(minute_interval):
    """ Get the seconds from the current time when the time will hit a specific minute interval, starting at the top
    of the hour. For example, if minute_interval = 15, returns the next minute interval divisible by 15 (0, 15, 30, 45).
    Minute interval must be evently divisible into 60
    :param minute_interval: The target minute interval
    :return {float}:
    """
    assert 60 % minute_interval == 0
    current_utc_dt = get_current_datetime()
    target_utc_dt = get_current_datetime().replace(second=0, microsecond=0)
    target_utc_dt = target_utc_dt + datetime.timedelta(minutes=minute_interval - (target_utc_dt.minute % minute_interval))
    return (target_utc_dt - current_utc_dt).total_seconds()


def get_datetime_to_nearest_minutes(input_dt, minute_interval):
    """ Get datetime at the exact minute based on the nearest minute interval.
    Example:
        input_dt = '2022-10-01 11:22:33'
        minute_interval = 10
        returns '2022-10-01 11:20:00'
    :param input_dt: {datetime} The datetime value to round to the nearest minutes
    :param minute_interval: {int} The minute interval to round to
    :return:
    """
    round_interval = round_to(input_dt.minute, minute_interval)
    rounded_dt = input_dt + datetime.timedelta(minutes=round_interval - input_dt.minute)
    return rounded_dt.replace(second=0, microsecond=0)
