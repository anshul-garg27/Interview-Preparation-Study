"""Show - a screening of a movie in a cinema hall."""

import threading
from datetime import datetime, timedelta
from movie import Movie
from enums import SeatStatus


class Show:
    """A movie screening at a specific time in a specific hall."""

    def __init__(self, show_id: str, movie: Movie, screen: "CinemaHall",
                 start_time: datetime):
        self.show_id = show_id
        self.movie = movie
        self.screen = screen
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=movie.duration_min)
        self.booked_seats: set[str] = set()
        self._lock = threading.Lock()

    def is_seat_available(self, seat_id: str) -> bool:
        """Check if a seat is available for this show."""
        return seat_id not in self.booked_seats

    def book_seats(self, seat_ids: list[str]) -> bool:
        """Atomically book multiple seats. Returns False if any taken."""
        with self._lock:
            for sid in seat_ids:
                if sid in self.booked_seats:
                    return False
            self.booked_seats.update(seat_ids)
            return True

    def available_count(self) -> int:
        """Count of seats still available."""
        return len(self.screen.seats) - len(self.booked_seats)

    def __repr__(self) -> str:
        return (f"Show({self.movie.title}, {self.screen.name}, "
                f"{self.start_time.strftime('%I:%M %p')})")
