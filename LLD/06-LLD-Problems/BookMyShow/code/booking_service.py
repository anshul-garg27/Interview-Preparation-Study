"""BookingService - Singleton that manages all bookings."""

import threading
from booking import Booking
from show import Show
from user import User
from payment import PaymentStrategy
from notification import NotificationService


class BookingService:
    """Singleton service for managing movie ticket bookings."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> "BookingService":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.bookings = []
        return cls._instance

    def book_seats(self, user: User, show: Show, seat_ids: list[str],
                   payment: PaymentStrategy) -> Booking | None:
        """Book seats for a user. Returns Booking or None on failure."""
        print(f"\n    [{user.name}] Attempting to book {seat_ids} "
              f"for '{show.movie.title}'")

        unavailable = [s for s in seat_ids if not show.is_seat_available(s)]
        if unavailable:
            print(f"    [{user.name}] FAILED - Already booked: {unavailable}")
            return None

        booking = Booking(user, show, seat_ids)
        if booking.confirm(payment):
            self.bookings.append(booking)
            NotificationService.send_booking_confirmation(booking)
            print(f"    [{user.name}] SUCCESS - {booking}")
            return booking

        print(f"    [{user.name}] FAILED - Payment or booking failed")
        return None

    def cancel_booking(self, booking: Booking) -> None:
        """Cancel an existing booking."""
        booking.cancel()
        NotificationService.send_cancellation(booking)

    def show_available_seats(self, show: Show) -> list[str]:
        """Return list of available seat IDs for a show."""
        return [sid for sid in show.screen.seats
                if show.is_seat_available(sid)]
