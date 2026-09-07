"""
Tithi = angular distance between Moon and Sun (sidereal), divided into
30 segments of 12 degrees each.

This module takes raw sidereal sun/moon longitudes (already ayanamsa-
corrected) and determines which tithi is active and when it ends. Finding
the exact END time of a tithi requires root-finding against the ephemeris
service (the 12-degree boundary crossing doesn't fall on a clean timestamp)
— stubbed here as a TODO since it needs iterative querying, not a single
raw-position call.
"""

from dataclasses import dataclass
from datetime import datetime

TITHI_NAMES = [
    "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi",
    "Shukla Panchami", "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami",
    "Shukla Navami", "Shukla Dashami", "Shukla Ekadashi", "Shukla Dwadashi",
    "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi",
    "Krishna Panchami", "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami",
    "Krishna Navami", "Krishna Dashami", "Krishna Ekadashi", "Krishna Dwadashi",
    "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya",
]


@dataclass
class TithiSegment:
    name: str
    end_utc: datetime


def current_tithi_index(sun_sidereal_deg: float, moon_sidereal_deg: float) -> int:
    """Returns 0-29 index into TITHI_NAMES."""
    diff = (moon_sidereal_deg - sun_sidereal_deg) % 360.0
    return int(diff // 12)


def find_tithi_end_time(
    dt_utc: datetime,
    lat: float,
    lon: float,
    tithi_index: int,
) -> datetime:
    """
    STUB — needs iterative/root-finding queries against the ephemeris
    client to find the exact moment moon-sun angular difference crosses
    the next 12-degree boundary. Do not ship without implementing and
    validating this against a trusted reference panchanga.
    """
    raise NotImplementedError(
        "Implement boundary root-finding using EphemerisClient before use."
    )
