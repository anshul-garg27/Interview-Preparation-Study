"""Calendar view for room availability checking."""


class CalendarView:
    """Manages booking calendar for rooms and checks availability."""

    def __init__(self):
        self._room_bookings = {}  # room_id -> [Booking]

    def add_booking(self, booking):
        room_id = booking.room.id
        if room_id not in self._room_bookings:
            self._room_bookings[room_id] = []
        self._room_bookings[room_id].append(booking)

    def is_available(self, room_id, start_time, end_time):
        """Check if a room is available for the given time slot."""
        bookings = self._room_bookings.get(room_id, [])
        for booking in bookings:
            if booking.overlaps_with(start_time, end_time):
                return False
        return True

    def get_conflicting_booking(self, room_id, start_time, end_time):
        """Return the booking that conflicts with the given time, or None."""
        bookings = self._room_bookings.get(room_id, [])
        for booking in bookings:
            if booking.overlaps_with(start_time, end_time):
                return booking
        return None

    def get_room_schedule(self, room_id):
        """Get all active bookings for a room, sorted by start time."""
        bookings = self._room_bookings.get(room_id, [])
        active = [b for b in bookings if b.is_active()]
        return sorted(active, key=lambda b: b.start_time)

    def display_room_calendar(self, room):
        """Display the full calendar for a room."""
        schedule = self.get_room_schedule(room.id)
        print(f"\n  Calendar for: {room.name} ({room.size.value}, {room.capacity} seats)")
        print(f"  {'=' * 45}")
        if not schedule:
            print("  (no bookings)")
        else:
            for booking in schedule:
                print(f"  {booking.short_str()}")
        print(f"  {'=' * 45}")
