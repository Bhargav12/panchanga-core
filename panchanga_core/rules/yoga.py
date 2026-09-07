"""
Yoga = sum of sidereal Sun and Moon longitudes, divided into 27 segments
of 13 degrees 20 minutes each (same segment size as nakshatra, different
underlying quantity).
"""

from dataclasses import dataclass
from datetime import datetime

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti",
]

_SEGMENT_DEG = 360.0 / 27.0


@dataclass
class YogaSegment:
    name: str
    end_utc: datetime


def current_yoga_index(sun_sidereal_deg: float, moon_sidereal_deg: float) -> int:
    total = (sun_sidereal_deg + moon_sidereal_deg) % 360.0
    return int(total // _SEGMENT_DEG)


def find_yoga_end_time(dt_utc: datetime, lat: float, lon: float, yoga_index: int) -> datetime:
    """STUB — root-find against sun+moon sum crossing the next 13°20' boundary."""
    raise NotImplementedError(
        "Implement boundary root-finding using EphemerisClient before use."
    )
