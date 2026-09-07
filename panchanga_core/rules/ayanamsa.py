"""
Ayanamsa correction: converts a tropical ecliptic longitude (what the
ephemeris service returns) into a sidereal longitude (what panchanga
calculations conventionally use).

This is a matter of astrological convention/tradition, not physics — it
must be a configurable value, not hardcoded, since different regions and
sampradayas expect different defaults (Lahiri is most common in India).
"""

from enum import Enum


class AyanamsaSystem(str, Enum):
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KP = "kp"


# TODO: replace with real, validated ayanamsa values/formulas per system.
# These are illustrative only and NOT accurate for production use.
_AYANAMSA_OFFSET_DEG_2026 = {
    AyanamsaSystem.LAHIRI: 24.19,
    AyanamsaSystem.RAMAN: 22.44,
    AyanamsaSystem.KP: 23.85,
}


def tropical_to_sidereal(tropical_longitude_deg: float, system: AyanamsaSystem) -> float:
    """
    STUB — replace with a proper, date-dependent ayanamsa calculation
    (ayanamsa drifts ~50 arcsec/year) before relying on this for real output.
    """
    offset = _AYANAMSA_OFFSET_DEG_2026[system]
    return (tropical_longitude_deg - offset) % 360.0
