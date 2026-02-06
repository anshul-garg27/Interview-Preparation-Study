"""Floor entity."""


class Floor:
    """Represents a floor in a building containing conference rooms."""

    def __init__(self, floor_number):
        self.number = floor_number
        self.rooms = {}  # room_id -> ConferenceRoom

    def add_room(self, room):
        room.floor_number = self.number
        self.rooms[room.id] = room

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def get_all_rooms(self):
        return list(self.rooms.values())

    def __str__(self):
        room_names = ", ".join(r.name for r in self.rooms.values())
        return f"Floor {self.number}: [{room_names}]"
