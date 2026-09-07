"""
Karana = half-tithi (6-degree segments of the moon-sun angular difference).
There are 11 karanas total: 4 fixed (occur once per lunar month at specific
positions) and 7 movable (repeat 8 times each across the month). The
sequencing rule (which karana falls in which half-tithi slot) is a fixed
traditional table, not a simple modulo — implement carefully and validate.
"""

from dataclasses import dataclass
from datetime import datetime

FIXED_KARANAS = ["Shakuni", "Chatushpada", "Naga", "Kimstughna"]
MOVABLE_KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"]


@dataclass
class KaranaSegment:
    name: str
    end_utc: datetime


def current_karana_index(sun_sidereal_deg: float, moon_sidereal_deg: float) -> int:
    """
    Returns 0-59 index (half-tithi number across the lunar month).
    STUB — the mapping from this index to a specific karana name follows a
    fixed traditional table (movable karanas cycle 8x, fixed karanas occur
    once each at specific points near the start/end of the month). Implement
    the real lookup table and validate against a trusted reference before use.
    """
    diff = (moon_sidereal_deg - sun_sidereal_deg) % 360.0
    return int(diff // 6)


def karana_name_for_index(half_tithi_index: int) -> str:
    raise NotImplementedError(
        "Implement the fixed/movable karana lookup table before use."
    )
