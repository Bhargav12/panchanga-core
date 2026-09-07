"""
The ONLY point of contact with ephemeris-service.

Nothing else in panchanga-core should make network calls to the ephemeris
service directly — always go through this client, so the AGPL boundary
stays enforceable and auditable in one place.
"""

from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass
class RawPosition:
    sun_longitude_deg: float
    moon_longitude_deg: float
    sunrise_utc: datetime
    sunset_utc: datetime


class EphemerisClient:
    def __init__(self, base_url: str, timeout_s: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    def get_position(self, dt_utc: datetime, lat: float, lon: float) -> RawPosition:
        resp = requests.post(
            f"{self.base_url}/position",
            json={
                "datetime_utc": dt_utc.isoformat(),
                "lat": lat,
                "lon": lon,
            },
            timeout=self.timeout_s,
        )
        resp.raise_for_status()
        data = resp.json()
        return RawPosition(
            sun_longitude_deg=data["sun_longitude_deg"],
            moon_longitude_deg=data["moon_longitude_deg"],
            sunrise_utc=datetime.fromisoformat(data["sunrise_utc"]),
            sunset_utc=datetime.fromisoformat(data["sunset_utc"]),
        )
