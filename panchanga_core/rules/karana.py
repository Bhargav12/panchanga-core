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
    """
    Maps a 0-59 half-tithi index to its karana name using the traditional
    sequencing rule:
      - index 0: Kimstughna (fixed)
      - indices 1-56: the 7 movable karanas, cycling 8 times
      - index 57: Shakuni (fixed)
      - index 58: Chatushpada (fixed)
      - index 59: Naga (fixed)
    """
    if not 0 <= half_tithi_index <= 59:
        raise ValueError(f"half_tithi_index must be in [0, 59], got {half_tithi_index}")

    if half_tithi_index == 0:
        return "Kimstughna"
    if half_tithi_index == 57:
        return "Shakuni"
    if half_tithi_index == 58:
        return "Chatushpada"
    if half_tithi_index == 59:
        return "Naga"
    return MOVABLE_KARANAS[(half_tithi_index - 1) % len(MOVABLE_KARANAS)]
