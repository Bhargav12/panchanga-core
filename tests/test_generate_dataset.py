import sqlite3
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from panchanga_core.client.ephemeris_client import RawPosition
from panchanga_core.orchestrator.generate_dataset import (
    _fetch_sun_times,
    _local_midnight_utc,
    generate,
)
from panchanga_core.orchestrator.grid import CITY_GRID


class FakeRiseTransClient:
    """Mimics ephemeris-service's real /position contract: sunrise_utc and
    sunset_utc are each independently "the next occurrence after
    datetime_utc" (swe.rise_trans semantics), not "today's sunrise/sunset".
    Used to reproduce issue #7 without a live ephemeris-service instance.
    """

    def __init__(self, sunrise_local: time, sunset_local: time, tz_name: str):
        self.sunrise_local = sunrise_local
        self.sunset_local = sunset_local
        self.tz_name = tz_name

    def _next_occurrence(self, dt_utc: datetime, local_time: time) -> datetime:
        tz = ZoneInfo(self.tz_name)
        dt_local = dt_utc.replace(tzinfo=timezone.utc).astimezone(tz)
        candidate_local = datetime.combine(dt_local.date(), local_time, tzinfo=tz)
        if candidate_local <= dt_local:
            candidate_local += timedelta(days=1)
        return candidate_local.astimezone(timezone.utc).replace(tzinfo=None)

    def get_position(self, dt_utc: datetime, lat: float, lon: float) -> RawPosition:
        return RawPosition(
            sun_longitude_deg=0.0,
            moon_longitude_deg=0.0,
            sunrise_utc=self._next_occurrence(dt_utc, self.sunrise_local),
            sunset_utc=self._next_occurrence(dt_utc, self.sunset_local),
        )


def _chennai():
    return next(c for c in CITY_GRID if c.city_id == "chennai_in")


def test_fake_client_reproduces_the_inverted_pairing_bug():
    # Sanity-check the fake against the exact scenario from issue #7:
    # querying at the mid-day sample instant (06:30 UTC, ~noon IST) pairs
    # today's sunset with tomorrow's sunrise.
    client = FakeRiseTransClient(time(6, 0), time(18, 0), "Asia/Kolkata")
    sample_dt_utc = datetime(2026, 11, 1, 6, 30)

    raw = client.get_position(sample_dt_utc, 13.0827, 80.2707)

    assert raw.sunrise_utc > raw.sunset_utc


def test_fetch_sun_times_returns_correctly_ordered_same_day_window():
    client = FakeRiseTransClient(time(6, 0), time(18, 0), "Asia/Kolkata")
    city = _chennai()

    sun_times = _fetch_sun_times(client, date(2026, 11, 1), city)

    assert sun_times.sunrise_utc < sun_times.sunset_utc
    assert (sun_times.sunset_utc - sun_times.sunrise_utc) < timedelta(hours=13)


def test_local_midnight_utc_precedes_both_sunrise_and_sunset():
    anchor_utc = _local_midnight_utc(date(2026, 11, 1), "Asia/Kolkata")
    client = FakeRiseTransClient(time(6, 0), time(18, 0), "Asia/Kolkata")

    sun_times = client.get_position(anchor_utc, 13.0827, 80.2707)

    assert anchor_utc < sun_times.sunrise_utc < sun_times.sunset_utc


def test_generate_writes_ordered_rahu_kalam_window_for_midday_sample(tmp_path):
    # End-to-end regression test for issue #7: generate() samples at
    # 06:30 UTC (between sunrise and sunset for Asia/Kolkata cities), which
    # is exactly the instant that triggered inverted rahu_kalam/yamaganda/
    # gulika windows before the fix.
    client = FakeRiseTransClient(time(6, 0), time(18, 0), "Asia/Kolkata")
    db_path = str(tmp_path / "panchanga.sqlite3")

    generate(start=date(2026, 11, 1), days=1, db_path=db_path, client=client)

    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT sunrise, sunset, rahu_kalam_start, rahu_kalam_end, "
        "yamaganda_start, yamaganda_end, gulika_start, gulika_end "
        "FROM panchanga_day WHERE city_id = ? AND date = ?",
        ("chennai_in", "2026-11-01"),
    ).fetchone()
    conn.close()

    assert row is not None
    sunrise, sunset, rk_start, rk_end, ym_start, ym_end, gk_start, gk_end = row

    assert sunrise < sunset
    assert rk_start < rk_end
    assert ym_start < ym_end
    assert gk_start < gk_end
