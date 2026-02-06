"""Location with Haversine distance calculation."""

import math


class Location:
    """Represents a geographic point with lat/lng coordinates."""

    EARTH_RADIUS_KM = 6371.0

    def __init__(self, lat: float, lng: float, name: str = ""):
        self.lat = lat
        self.lng = lng
        self.name = name or f"({lat:.1f},{lng:.1f})"

    def distance_to(self, other: "Location") -> float:
        """Calculate distance using Haversine formula (km)."""
        lat1, lat2 = math.radians(self.lat), math.radians(other.lat)
        dlat = math.radians(other.lat - self.lat)
        dlng = math.radians(other.lng - self.lng)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2)
        return self.EARTH_RADIUS_KM * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def __repr__(self) -> str:
        return self.name
