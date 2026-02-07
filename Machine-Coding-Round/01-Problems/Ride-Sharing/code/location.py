"""Location class with latitude/longitude and distance calculation."""

import math


class Location:
    """Represents a geographical location with latitude and longitude.

    Uses the Haversine formula to calculate distance between two points.
    """

    EARTH_RADIUS_KM = 6371.0

    def __init__(self, latitude: float, longitude: float) -> None:
        """Initialize a location with lat/lng coordinates.

        Args:
            latitude: Latitude in degrees (-90 to 90).
            longitude: Longitude in degrees (-180 to 180).

        Raises:
            ValueError: If coordinates are out of valid range.
        """
        if not (-90 <= latitude <= 90):
            raise ValueError(f"Latitude must be between -90 and 90, got {latitude}")
        if not (-180 <= longitude <= 180):
            raise ValueError(f"Longitude must be between -180 and 180, got {longitude}")
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, other: "Location") -> float:
        """Calculate distance to another location using the Haversine formula.

        Args:
            other: The other location to calculate distance to.

        Returns:
            Distance in kilometers, rounded to 2 decimal places.
        """
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = self.EARTH_RADIUS_KM * c
        return round(distance, 2)

    def __str__(self) -> str:
        return f"({self.latitude:.4f}, {self.longitude:.4f})"

    def __repr__(self) -> str:
        return f"Location(lat={self.latitude}, lng={self.longitude})"
