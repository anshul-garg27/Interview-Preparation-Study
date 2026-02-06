"""Booking service - core business logic for room bookings."""

from booking import Booking
from calendar_view import CalendarView


class BookingService:
    """Handles booking creation, cancellation, and retrieval."""

    def __init__(self, buildings):
        self._buildings = {b.name: b for b in buildings}
        self._bookings = {}  # booking_id -> Booking
        self._calendar = CalendarView()
        self._room_lookup = {}  # room_id -> ConferenceRoom
        self._build_room_index()

    def _build_room_index(self):
        """Build a lookup from room_id to ConferenceRoom."""
        for building in self._buildings.values():
            for room in building.get_all_rooms():
                self._room_lookup[room.id] = room

    def book_room(self, room_id, organizer, start_time, end_time):
        """Book a room for the given time slot."""
        # Validate room exists
        room = self._room_lookup.get(room_id)
        if not room:
            print(f"[ERROR] Room '{room_id}' not found")
            return None

        # Validate time
        if not self._validate_time(start_time, end_time):
            return None

        # Check availability
        conflict = self._calendar.get_conflicting_booking(room_id, start_time, end_time)
        if conflict:
            print(f"[ERROR] {room.name} is not available from {start_time} to {end_time} "
                  f"(conflicts with {conflict.id})")
            return None

        # Create booking
        booking = Booking(room, organizer, start_time, end_time)
        self._bookings[booking.id] = booking
        self._calendar.add_booking(booking)
        print(f"[SUCCESS] Booking {booking.id} created: {room.name}, "
              f"{start_time}-{end_time}, Organizer: {organizer}")
        return booking

    def cancel_booking(self, booking_id):
        """Cancel an existing booking."""
        booking = self._bookings.get(booking_id)
        if not booking:
            print(f"[ERROR] Booking '{booking_id}' not found")
            return False

        if not booking.is_active():
            print(f"[ERROR] Booking '{booking_id}' is already cancelled")
            return False

        booking.cancel()
        print(f"[SUCCESS] Booking {booking_id} cancelled "
              f"({booking.room.name}, {booking.start_time}-{booking.end_time})")
        return True

    def get_booking(self, booking_id):
        """Get booking details."""
        booking = self._bookings.get(booking_id)
        if not booking:
            print(f"[ERROR] Booking '{booking_id}' not found")
        return booking

    def get_all_bookings(self):
        """Get all active bookings."""
        return [b for b in self._bookings.values() if b.is_active()]

    def show_room_calendar(self, room_id):
        """Display the calendar for a specific room."""
        room = self._room_lookup.get(room_id)
        if not room:
            print(f"[ERROR] Room '{room_id}' not found")
            return
        self._calendar.display_room_calendar(room)

    def get_room(self, room_id):
        return self._room_lookup.get(room_id)

    def get_all_rooms(self):
        return list(self._room_lookup.values())

    def get_calendar(self):
        return self._calendar

    def _validate_time(self, start_time, end_time):
        """Validate that the time range is valid."""
        if not start_time or not end_time:
            print("[ERROR] Start time and end time are required")
            return False
        if start_time >= end_time:
            print(f"[ERROR] Start time ({start_time}) must be before end time ({end_time})")
            return False
        return True
