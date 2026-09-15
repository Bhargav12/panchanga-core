"""
Ayanamsa correction: converts a tropical ecliptic longitude (what the
ephemeris service returns) into a sidereal longitude (what panchanga
calculations conventionally use).

This is a matter of astrological convention/tradition, not physics — it
must be a configurable value, not hardcoded, since different regions and
sampradayas expect different defaults (Lahiri is most common in India).

Per CLAUDE.md, `EphemerisClient` is the only point of contact with
ephemeris-service, and its `/position` response carries no ayanamsa
field (just sun/moon tropical longitude and sunrise/sunset) — so this
module reimplements the standard ayanamsa formula in pure Python rather
than depending on the service or importing Swiss Ephemeris directly.

Lahiri (Chitrapaksha) ayanamsa is modeled here as a linear function of
time — a fixed value at the J2000.0 epoch, plus a constant precession
rate — which is the same simplification most panchanga software uses to
get a date-dependent ayanamsa without reimplementing full precession/
nutation theory:

  - Anchor: 23°51'11" (23.853055...deg) at J2000.0 (2000-01-01 12:00 TT).
    This is the Lahiri/Chitrapaksha ayanamsa value widely published for
    the J2000 epoch (matches the figure produced by Swiss Ephemeris's
    SE_SIDM_LAHIRI and quoted across Indian ephemeris references).
  - Rate: 50.2910"/year — the IAU 1976 general precession in ecliptic
    longitude (5029.0966"/Julian century; Lieske et al. 1977), which is
    also the commonly cited "~50 arcsec/year" drift rate for ayanamsa.

Sanity check: this model gives ~24°13' for 2026, close to this module's
old placeholder (24.19deg = 24°11.4') and to the ~24°10'-24°12' figures
Indian ephemerides publish for the mid-2020s.

Caveat: this is a linear approximation, not a reproduction of full
precession/nutation theory. It is accurate to within roughly an
arcminute over the few centuries either side of J2000 — enough for
tithi/nakshatra/yoga boundaries (12deg / 13deg20' segments), but it
should not be treated as sub-arcsecond-accurate. This module's author
did not have live internet access to independently verify the anchor
value against a primary source at implementation time (e.g. the Swiss
Ephemeris source or an Indian Positional Astronomy Centre almanac) —
treat the Lahiri figures below as "well-established secondary-source
values, cross-checked against the drift rate and this repo's own prior
placeholder," not as independently re-derived from a primary source.
Validate against a printed panchangam per CLAUDE.md before production use.

Raman and KP ayanamsa are derived from Lahiri via fixed offsets carried
over from this module's original placeholder table. Unlike Lahiri,
these offsets have NOT been researched against any source — they exist
so the enum stays fully supported, not as a validated calculation. Do
not trust them for production use without independently sourcing each
system's own reference epoch/rate.
"""

from datetime import datetime, timezone
from enum import Enum


class AyanamsaSystem(str, Enum):
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KP = "kp"


# J2000.0 epoch: 2000-01-01 12:00 TT. The ~64s TT-UTC offset at this epoch
# is negligible next to this model's arcminute-level accuracy, so we treat
# the anchor as UTC.
_J2000_EPOCH_UTC = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

# Lahiri (Chitrapaksha) ayanamsa at J2000.0: 23 deg 51' 11".
_LAHIRI_AYANAMSA_AT_J2000_DEG = 23 + 51 / 60 + 11 / 3600

# IAU 1976 general precession in ecliptic longitude: 5029.0966"/Julian century.
_PRECESSION_DEG_PER_YEAR = (5029.0966 / 100) / 3600

_JULIAN_YEAR_DAYS = 365.25

# Raman/KP offsets from Lahiri, carried over from the original placeholder
# table (illustrative 2026 values) purely to preserve the existing spread
# between systems. NOT independently validated — see module docstring.
_RAMAN_OFFSET_FROM_LAHIRI_DEG = 22.44 - 24.19
_KP_OFFSET_FROM_LAHIRI_DEG = 23.85 - 24.19


def _years_since_j2000(dt_utc: datetime) -> float:
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    delta_days = (dt_utc - _J2000_EPOCH_UTC).total_seconds() / 86400.0
    return delta_days / _JULIAN_YEAR_DAYS


def ayanamsa_deg(dt_utc: datetime, system: AyanamsaSystem) -> float:
    """
    Date-dependent ayanamsa offset (degrees) for `system` at `dt_utc`.
    See module docstring for the model and its accuracy caveats.
    """
    lahiri = _LAHIRI_AYANAMSA_AT_J2000_DEG + _PRECESSION_DEG_PER_YEAR * _years_since_j2000(dt_utc)

    if system == AyanamsaSystem.LAHIRI:
        return lahiri
    if system == AyanamsaSystem.RAMAN:
        return lahiri + _RAMAN_OFFSET_FROM_LAHIRI_DEG
    if system == AyanamsaSystem.KP:
        return lahiri + _KP_OFFSET_FROM_LAHIRI_DEG
    raise ValueError(f"Unsupported ayanamsa system: {system}")


def tropical_to_sidereal(tropical_longitude_deg: float, system: AyanamsaSystem, dt_utc: datetime) -> float:
    """
    Converts a tropical ecliptic longitude to sidereal, using the
    date-dependent ayanamsa for `system` at `dt_utc`.
    """
    offset = ayanamsa_deg(dt_utc, system)
    return (tropical_longitude_deg - offset) % 360.0
