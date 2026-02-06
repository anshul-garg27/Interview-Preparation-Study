"""Booking entity for movie tickets."""

import threading
from enums import BookingStatus
from show import Show
from user import User
from seat import SEAT_PRICES
from payment import PaymentStrategy


class Booking:
    """A ticket booking for a show."""

    _counter = 0
    _lock = threading.Lock()

    def __init__(self, user: User, show: Show, seat_ids: list[str]):
        with Booking._lock:
            Booking._counter += 1
            self.booking_id = f"BKG-{Booking._counter:04d}"
        self.user = user
        self.show = show
        self.seat_ids = seat_ids
        self.status = BookingStatus.PENDING
        self.total_amount = self._calculate_total()

    def _calculate_total(self) -> float:
        """Sum up prices of all booked seats."""
        total = 0.0
        for sid in self.seat_ids:
            seat = self.show.screen.seats[sid]
            total += SEAT_PRICES[seat.seat_type]
        return total

    def confirm(self, payment: PaymentStrategy) -> bool:
        """Process payment and confirm booking."""
        if payment.pay(self.total_amount, self.user.name):
            if self.show.book_seats(self.seat_ids):
                self.status = BookingStatus.CONFIRMED
                return True
        self.status = BookingStatus.CANCELLED
        return False

    def cancel(self) -> None:
        """Cancel this booking."""
        self.status = BookingStatus.CANCELLED

    def __repr__(self) -> str:
        return (f"Booking({self.booking_id}, {self.user.name}, "
                f"{self.show.movie.title}, Seats={self.seat_ids}, "
                f"${self.total_amount:.2f}, {self.status.value})")
