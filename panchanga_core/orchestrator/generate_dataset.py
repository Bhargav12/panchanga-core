"""
Precompute Orchestrator — loops over the location grid x date range,
calls ephemeris-service via EphemerisClient for raw positions, runs them
through the rule layer, and writes results to a static SQLite dataset.

This module never touches Swiss Ephemeris directly — it only calls
EphemerisClient over HTTP — so it stays on the proprietary side of the
AGPL boundary.

Usage:
    python -m panchanga_core.orchestrator.generate_dataset --start 2026-01-01 --days 365
"""

import argparse
import os
import sqlite3
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from panchanga_core.client.ephemeris_client import EphemerisClient
from panchanga_core.orchestrator.grid import CITY_GRID, City
from panchanga_core.orchestrator.schema import SCHEMA_SQL
from panchanga_core.rules.ayanamsa import AyanamsaSystem, tropical_to_sidereal
from panchanga_core.rules.nakshatra import NAKSHATRA_NAMES, current_nakshatra_index
from panchanga_core.rules.tithi import TITHI_NAMES, current_tithi_index
from panchanga_core.rules.vara_and_kalam import (
    VARA_NAMES,
    gulika_kalam,
    rahu_kalam,
    yamaganda,
)
from panchanga_core.rules.yoga import YOGA_NAMES, current_yoga_index


def _local_midnight_utc(local_date: date, tz_name: str) -> datetime:
    """UTC instant for local midnight (00:00) of local_date in the given
    IANA timezone.

    ephemeris-service's /position returns the NEXT sunrise/sunset after the
    requested instant (swe.rise_trans semantics). Requesting from a mid-day
    instant is unsafe: "next sunset after now" is later today, but "next
    sunrise after now" has already happened today and rolls over to
    tomorrow, so sunrise_utc ends up after sunset_utc. Anchoring the
    request to local midnight guarantees both the next sunrise and the
    next sunset land on the same local calendar day, in the correct order.
    """
    local_midnight = datetime(
        local_date.year, local_date.month, local_date.day, tzinfo=ZoneInfo(tz_name)
    )
    return local_midnight.astimezone(timezone.utc).replace(tzinfo=None)


def _fetch_sun_times(client: EphemerisClient, current_date: date, city: City):
    """Fetch today's sunrise/sunset for a city, anchored to local midnight
    so the pairing is always same-day and correctly ordered (see
    _local_midnight_utc)."""
    anchor_utc = _local_midnight_utc(current_date, city.timezone)
    return client.get_position(anchor_utc, city.lat, city.lon)


def generate(
    start: date,
    days: int,
    db_path: str,
    ephemeris_url: str = None,
    client: EphemerisClient = None,
) -> None:
    if client is None:
        client = EphemerisClient(base_url=ephemeris_url)

    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)

    for offset in range(days):
        current_date = start + timedelta(days=offset)

        for city in CITY_GRID:
            # Use local noon as a representative sample point for this
            # scaffold. NOTE: a production implementation needs the full
            # boundary-crossing logic (see tithi.py / nakshatra.py /
            # yoga.py TODOs) to capture segments that start/end mid-day,
            # not just a single noon snapshot.
            sample_dt_utc = datetime(current_date.year, current_date.month, current_date.day, 6, 30)

            raw = client.get_position(sample_dt_utc, city.lat, city.lon)

            # Sunrise/sunset must NOT come from `raw` above: that call is
            # anchored to the mid-day sample instant, which falls between
            # today's sunrise and today's sunset. Per ephemeris-service's
            # "next occurrence after this instant" semantics, that pairing
            # returns today's sunset but tomorrow's sunrise (sunrise_utc >
            # sunset_utc). Fetch sun times separately, anchored to local
            # midnight, so they're correctly ordered and same-day.
            sun_times = _fetch_sun_times(client, current_date, city)

            sun_sidereal = tropical_to_sidereal(raw.sun_longitude_deg, AyanamsaSystem.LAHIRI)
            moon_sidereal = tropical_to_sidereal(raw.moon_longitude_deg, AyanamsaSystem.LAHIRI)

            tithi_name = TITHI_NAMES[current_tithi_index(sun_sidereal, moon_sidereal)]
            nakshatra_name = NAKSHATRA_NAMES[current_nakshatra_index(moon_sidereal)]
            yoga_name = YOGA_NAMES[current_yoga_index(sun_sidereal, moon_sidereal)]

            weekday_name = VARA_NAMES[(current_date.weekday() + 1) % 7]  # Mon=0 -> Sun=0 remap

            rk = rahu_kalam(sun_times.sunrise_utc, sun_times.sunset_utc, weekday_name)
            ym = yamaganda(sun_times.sunrise_utc, sun_times.sunset_utc, weekday_name)
            gk = gulika_kalam(sun_times.sunrise_utc, sun_times.sunset_utc, weekday_name)

            conn.execute(
                """
                INSERT OR REPLACE INTO panchanga_day
                (city_id, date, sunrise, sunset, rahu_kalam_start, rahu_kalam_end,
                 yamaganda_start, yamaganda_end, gulika_start, gulika_end, vara)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    city.city_id, current_date.isoformat(),
                    sun_times.sunrise_utc.isoformat(), sun_times.sunset_utc.isoformat(),
                    rk.start_utc.isoformat(), rk.end_utc.isoformat(),
                    ym.start_utc.isoformat(), ym.end_utc.isoformat(),
                    gk.start_utc.isoformat(), gk.end_utc.isoformat(),
                    weekday_name,
                ),
            )

            conn.execute(
                "INSERT INTO tithi_segment (city_id, date, tithi_name, segment_start, segment_end) "
                "VALUES (?, ?, ?, ?, ?)",
                (city.city_id, current_date.isoformat(), tithi_name, None, None),
            )
            conn.execute(
                "INSERT INTO nakshatra_segment (city_id, date, nakshatra_name, segment_start, segment_end) "
                "VALUES (?, ?, ?, ?, ?)",
                (city.city_id, current_date.isoformat(), nakshatra_name, None, None),
            )
            conn.execute(
                "INSERT INTO yoga_segment (city_id, date, yoga_name, segment_start, segment_end) "
                "VALUES (?, ?, ?, ?, ?)",
                (city.city_id, current_date.isoformat(), yoga_name, None, None),
            )
            # karana intentionally omitted from this scaffold run — see
            # karana.py TODO (lookup table not yet implemented).

        conn.commit()

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Generate the static panchanga dataset.")
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--db", default="panchanga.sqlite3")
    args = parser.parse_args()

    ephemeris_url = os.environ.get("EPHEMERIS_SERVICE_URL", "http://localhost:8000")
    start_date = date.fromisoformat(args.start)

    generate(start=start_date, days=args.days, db_path=args.db, ephemeris_url=ephemeris_url)
    print(f"Done. Wrote dataset to {args.db}")


if __name__ == "__main__":
    main()
