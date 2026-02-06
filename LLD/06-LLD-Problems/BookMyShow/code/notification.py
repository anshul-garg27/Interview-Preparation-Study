"""Notification service for booking confirmations."""

from booking import Booking


class NotificationService:
    """Sends booking confirmations to users."""

    @staticmethod
    def send_booking_confirmation(booking: Booking) -> None:
        """Send confirmation for a successful booking."""
        print(f"      [Notification] Email sent to {booking.user.email}: "
              f"Booking {booking.booking_id} confirmed for "
              f"'{booking.show.movie.title}' | "
              f"Seats: {booking.seat_ids} | "
              f"Amount: ${booking.total_amount:.2f}")

    @staticmethod
    def send_cancellation(booking: Booking) -> None:
        """Send cancellation notice."""
        print(f"      [Notification] Email sent to {booking.user.email}: "
              f"Booking {booking.booking_id} has been cancelled.")
