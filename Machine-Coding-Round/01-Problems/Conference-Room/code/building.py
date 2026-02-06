"""Building entity."""

from floor import Floor


class Building:
    """Represents a building with multiple floors."""

    def __init__(self, name):
        self.name = name
        self.floors = {}  # floor_number -> Floor

    def add_floor(self, floor_number):
        floor = Floor(floor_number)
        self.floors[floor_number] = floor
        return floor

    def get_floor(self, floor_number):
        return self.floors.get(floor_number)

    def get_all_rooms(self):
        """Get all rooms across all floors in this building."""
        rooms = []
        for floor in self.floors.values():
            for room in floor.get_all_rooms():
                room.building_name = self.name
                rooms.append(room)
        return rooms

    def __str__(self):
        floor_strs = []
        for fn in sorted(self.floors.keys()):
            floor_strs.append(f"  {self.floors[fn]}")
        return f"Building: {self.name}\n" + "\n".join(floor_strs)
