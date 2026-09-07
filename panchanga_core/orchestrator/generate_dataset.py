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
from datetime import date, datetime, timedelta

from panchanga_core.client.ephemeris_client import EphemerisClient
from panchanga_core.orchestrator.grid import CITY_GRID
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


def generate(start: date, days: int, db_path: str, ephemeris_url: str) -> None:
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

            sun_sidereal = tropical_to_sidereal(raw.sun_longitude_deg, AyanamsaSystem.LAHIRI)
            moon_sidereal = tropical_to_sidereal(raw.moon_longitude_deg, AyanamsaSystem.LAHIRI)

            tithi_name = TITHI_NAMES[current_tithi_index(sun_sidereal, moon_sidereal)]
            nakshatra_name = NAKSHATRA_NAMES[current_nakshatra_index(moon_sidereal)]
            yoga_name = YOGA_NAMES[current_yoga_index(sun_sidereal, moon_sidereal)]

            weekday_name = VARA_NAMES[(current_date.weekday() + 1) % 7]  # Mon=0 -> Sun=0 remap

            rk = rahu_kalam(raw.sunrise_utc, raw.sunset_utc, weekday_name)
            ym = yamaganda(raw.sunrise_utc, raw.sunset_utc, weekday_name)
            gk = gulika_kalam(raw.sunrise_utc, raw.sunset_utc, weekday_name)

            conn.execute(
                """
                INSERT OR REPLACE INTO panchanga_day
                (city_id, date, sunrise, sunset, rahu_kalam_start, rahu_kalam_end,
                 yamaganda_start, yamaganda_end, gulika_start, gulika_end, vara)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    city.city_id, current_date.isoformat(),
                    raw.sunrise_utc.isoformat(), raw.sunset_utc.isoformat(),
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
