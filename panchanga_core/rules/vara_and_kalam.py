"""
Vara (weekday) and the inauspicious-window rules (Rahu Kalam, Yamaganda,
Gulika Kalam) are pure day-of-week + sunrise/sunset segmentation logic.
No Swiss Ephemeris call is needed beyond the sunrise/sunset times already
returned by /position — this is why these rules live entirely on the
proprietary side with no additional network round-trip.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

VARA_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Each day is split into 8 equal segments between sunrise and sunset.
# The segment index (0-7) assigned to Rahu Kalam depends on the weekday.
_RAHU_KALAM_SEGMENT_BY_WEEKDAY = {
    "Sunday": 7, "Monday": 1, "Tuesday": 6, "Wednesday": 4,
    "Thursday": 5, "Friday": 3, "Saturday": 2,
}
_YAMAGANDA_SEGMENT_BY_WEEKDAY = {
    "Sunday": 4, "Monday": 3, "Tuesday": 2, "Wednesday": 1,
    "Thursday": 0, "Friday": 6, "Saturday": 5,
}
_GULIKA_SEGMENT_BY_WEEKDAY = {
    "Sunday": 5, "Monday": 4, "Tuesday": 3, "Wednesday": 2,
    "Thursday": 1, "Friday": 0, "Saturday": 6,
}


@dataclass
class TimeWindow:
    start_utc: datetime
    end_utc: datetime


def vara_name(sunrise_local_date_weekday: int) -> str:
    """sunrise_local_date_weekday: Python's date.weekday() convention adjusted to Sun=0."""
    return VARA_NAMES[sunrise_local_date_weekday]


def _segment_window(sunrise_utc: datetime, sunset_utc: datetime, segment_index: int) -> TimeWindow:
    day_length = sunset_utc - sunrise_utc
    segment_length = day_length / 8
    start = sunrise_utc + segment_length * segment_index
    end = start + segment_length
    return TimeWindow(start_utc=start, end_utc=end)


def rahu_kalam(sunrise_utc: datetime, sunset_utc: datetime, weekday_name: str) -> TimeWindow:
    return _segment_window(sunrise_utc, sunset_utc, _RAHU_KALAM_SEGMENT_BY_WEEKDAY[weekday_name])


def yamaganda(sunrise_utc: datetime, sunset_utc: datetime, weekday_name: str) -> TimeWindow:
    return _segment_window(sunrise_utc, sunset_utc, _YAMAGANDA_SEGMENT_BY_WEEKDAY[weekday_name])


def gulika_kalam(sunrise_utc: datetime, sunset_utc: datetime, weekday_name: str) -> TimeWindow:
    return _segment_window(sunrise_utc, sunset_utc, _GULIKA_SEGMENT_BY_WEEKDAY[weekday_name])
