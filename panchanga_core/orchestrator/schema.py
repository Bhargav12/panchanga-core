"""
On-device SQLite schema for the generated, static panchanga dataset.
This is the artifact that ships inside the mobile app — pure data, no
Swiss Ephemeris code, no AGPL exposure.
"""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS panchanga_day (
  city_id TEXT,
  date TEXT,
  sunrise TEXT,
  sunset TEXT,
  rahu_kalam_start TEXT,
  rahu_kalam_end TEXT,
  yamaganda_start TEXT,
  yamaganda_end TEXT,
  gulika_start TEXT,
  gulika_end TEXT,
  vara TEXT,
  PRIMARY KEY (city_id, date)
);

CREATE TABLE IF NOT EXISTS tithi_segment (
  city_id TEXT,
  date TEXT,
  tithi_name TEXT,
  segment_start TEXT,
  segment_end TEXT
);

CREATE TABLE IF NOT EXISTS nakshatra_segment (
  city_id TEXT,
  date TEXT,
  nakshatra_name TEXT,
  segment_start TEXT,
  segment_end TEXT
);

CREATE TABLE IF NOT EXISTS yoga_segment (
  city_id TEXT,
  date TEXT,
  yoga_name TEXT,
  segment_start TEXT,
  segment_end TEXT
);

CREATE TABLE IF NOT EXISTS karana_segment (
  city_id TEXT,
  date TEXT,
  karana_name TEXT,
  segment_start TEXT,
  segment_end TEXT
);

CREATE TABLE IF NOT EXISTS festival_flag (
  city_id TEXT,
  date TEXT,
  festival_name TEXT
);
"""
