"""
Nakshatra = Moon's sidereal longitude divided into 27 segments of
13 degrees 20 minutes (13.333...) each.
"""

from dataclasses import dataclass
from datetime import datetime

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

_SEGMENT_DEG = 360.0 / 27.0  # 13.333...


@dataclass
class NakshatraSegment:
    name: str
    end_utc: datetime


def current_nakshatra_index(moon_sidereal_deg: float) -> int:
    """Returns 0-26 index into NAKSHATRA_NAMES."""
    return int(moon_sidereal_deg // _SEGMENT_DEG)


def find_nakshatra_end_time(dt_utc: datetime, lat: float, lon: float, nakshatra_index: int) -> datetime:
    """
    STUB — same root-finding approach as tithi.py, against the
    13°20' boundary instead of 12°. Implement and validate before use.
    """
    raise NotImplementedError(
        "Implement boundary root-finding using EphemerisClient before use."
    )
