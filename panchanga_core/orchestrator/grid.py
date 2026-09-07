"""
Supported location grid. Panchanga barely changes over ~10-25km, so a
city-level grid (rather than infinite lat/long) is sufficient for the vast
majority of users. Snap unlisted user locations to the nearest grid city.

TODO: replace this placeholder list with the real supported-city list
(e.g. top 200-500 Indian cities + key diaspora cities) before Phase 1.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    city_id: str
    name: str
    lat: float
    lon: float
    timezone: str  # IANA tz name, e.g. "Asia/Kolkata"


CITY_GRID = [
    City("chennai_in", "Chennai", 13.0827, 80.2707, "Asia/Kolkata"),
    City("delhi_in", "Delhi", 28.6139, 77.2090, "Asia/Kolkata"),
    City("mumbai_in", "Mumbai", 19.0760, 72.8777, "Asia/Kolkata"),
    City("bengaluru_in", "Bengaluru", 12.9716, 77.5946, "Asia/Kolkata"),
    # TODO: extend to full supported grid
]


def nearest_city(lat: float, lon: float) -> City:
    """Naive nearest-neighbor by Euclidean distance on lat/lon — fine at
    city-grid granularity; replace with haversine if precision matters
    near grid boundaries."""
    return min(
        CITY_GRID,
        key=lambda c: (c.lat - lat) ** 2 + (c.lon - lon) ** 2,
    )
