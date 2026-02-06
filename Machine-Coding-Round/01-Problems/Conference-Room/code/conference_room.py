"""Conference Room entity."""

from enums import RoomSize, Amenity


class ConferenceRoom:
    """Represents a conference room with capacity and amenities."""

    def __init__(self, room_id, name, capacity, size, amenities=None):
        self.id = room_id
        self.name = name
        self.capacity = capacity
        self.size = size
        self.amenities = amenities or []
        self.floor_number = None
        self.building_name = None

    def has_amenity(self, amenity):
        return amenity in self.amenities

    def has_all_amenities(self, required_amenities):
        return all(a in self.amenities for a in required_amenities)

    def __str__(self):
        amenity_str = ", ".join(a.value for a in self.amenities) if self.amenities else "None"
        return (f"{self.name} ({self.size.value}, {self.capacity} seats, "
                f"Amenities: [{amenity_str}])")

    def short_str(self):
        location = ""
        if self.building_name and self.floor_number is not None:
            location = f" - Floor {self.floor_number}, {self.building_name}"
        return f"{self.name} ({self.size.value}, {self.capacity} seats){location}"
