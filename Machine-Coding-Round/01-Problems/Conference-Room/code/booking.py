"""Booking entity."""

from enums import BookingStatus


class Booking:
    """Represents a room booking with time slot and organizer."""

    _counter = 0

    def __init__(self, room, organizer, start_time, end_time):
        Booking._counter += 1
        self.id = f"BK-{Booking._counter:03d}"
        self.room = room
        self.organizer = organizer
        self.start_time = start_time
        self.end_time = end_time
        self.status = BookingStatus.CONFIRMED

    def is_active(self):
        return self.status == BookingStatus.CONFIRMED

    def cancel(self):
        self.status = BookingStatus.CANCELLED

    def overlaps_with(self, start_time, end_time):
        """Check if this booking overlaps with the given time range."""
        if not self.is_active():
            return False
        return self.start_time < end_time and start_time < self.end_time

    def __str__(self):
        return (f"Booking {self.id}: {self.room.name}, "
                f"{self.start_time}-{self.end_time}, "
                f"Organizer: {self.organizer}, "
                f"Status: {self.status.value}")

    def short_str(self):
        return f"{self.start_time}-{self.end_time}  {self.organizer} ({self.id})"
