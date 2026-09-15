from datetime import datetime, timezone

import pytest

from panchanga_core.rules.ayanamsa import AyanamsaSystem, ayanamsa_deg, tropical_to_sidereal

# Reference values:
#   - 23 deg 51' 11" (23.853056 deg) at J2000.0 (2000-01-01 12:00 TT) is the
#     widely published Lahiri/Chitrapaksha ayanamsa value for that epoch
#     (matches the figure produced by Swiss Ephemeris's SE_SIDM_LAHIRI and
#     quoted across Indian ephemeris references).
#   - ~24 deg 10'-24 deg 12' for the mid-2020s is the range commonly quoted
#     by contemporary Indian panchangam/ephemeris publications for the
#     Lahiri ayanamsa.
#   - 50.290966"/year is the IAU 1976 general precession in ecliptic
#     longitude (5029.0966"/Julian century; Lieske et al. 1977), the
#     standard citation for the "~50 arcsec/year" ayanamsa drift rate.
#
# Tolerance is kept loose (+/- 5 arcmin) because this module uses a linear
# precession approximation, not full precession/nutation theory.

J2000_UTC = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
_TOLERANCE_DEG = 5 / 60


def test_lahiri_at_j2000_epoch():
    assert ayanamsa_deg(J2000_UTC, AyanamsaSystem.LAHIRI) == pytest.approx(
        23 + 51 / 60 + 11 / 3600, abs=1e-6
    )


def test_lahiri_mid_2020s_matches_published_range():
    dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    value = ayanamsa_deg(dt, AyanamsaSystem.LAHIRI)
    assert (24 + 10 / 60) - _TOLERANCE_DEG <= value <= (24 + 12 / 60) + _TOLERANCE_DEG


def test_ayanamsa_increases_at_expected_precession_rate():
    # Over exactly 24 Julian years (2000-01-01 12:00 -> 2024-01-01 12:00),
    # this model should add 24 * 50.290966" = 1206.98" (~0.335273 deg).
    later = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    delta = ayanamsa_deg(later, AyanamsaSystem.LAHIRI) - ayanamsa_deg(J2000_UTC, AyanamsaSystem.LAHIRI)
    assert delta == pytest.approx(24 * 50.290966 / 3600, abs=1e-6)


def test_raman_and_kp_are_offset_from_lahiri_not_equal():
    dt = datetime(2010, 6, 15, tzinfo=timezone.utc)
    lahiri = ayanamsa_deg(dt, AyanamsaSystem.LAHIRI)
    assert ayanamsa_deg(dt, AyanamsaSystem.RAMAN) != lahiri
    assert ayanamsa_deg(dt, AyanamsaSystem.KP) != lahiri


def test_tropical_to_sidereal_applies_offset_and_wraps():
    offset = ayanamsa_deg(J2000_UTC, AyanamsaSystem.LAHIRI)
    assert tropical_to_sidereal(offset, AyanamsaSystem.LAHIRI, J2000_UTC) == pytest.approx(0.0, abs=1e-9)
    # A tropical longitude smaller than the ayanamsa offset must wrap into [0, 360).
    assert tropical_to_sidereal(1.0, AyanamsaSystem.LAHIRI, J2000_UTC) == pytest.approx(
        (1.0 - offset) % 360.0, abs=1e-9
    )


def test_naive_datetime_is_treated_as_utc():
    naive = datetime(2000, 1, 1, 12, 0, 0)
    assert ayanamsa_deg(naive, AyanamsaSystem.LAHIRI) == pytest.approx(
        ayanamsa_deg(J2000_UTC, AyanamsaSystem.LAHIRI), abs=1e-9
    )
