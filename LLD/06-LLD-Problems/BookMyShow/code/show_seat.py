"""ShowSeat - per-show seat with thread-safe locking."""

import threading
from enums import SeatStatus
from seat import Seat


class ShowSeat:
    """Tracks availability of a seat for a specific show with locking."""

    def __init__(self, seat: Seat):
        self.seat = seat
        self.status = SeatStatus.AVAILABLE
        self._lock = threading.Lock()

    def try_lock(self, timeout: float = 5.0) -> bool:
        """Attempt to lock seat for booking (with timeout)."""
        acquired = self._lock.acquire(timeout=timeout)
        if acquired:
            if self.status == SeatStatus.AVAILABLE:
                self.status = SeatStatus.LOCKED
                return True
            self._lock.release()
            return False
        return False

    def confirm(self) -> None:
        """Confirm booking - mark as booked and release lock."""
        self.status = SeatStatus.BOOKED
        self._lock.release()

    def release(self) -> None:
        """Release lock and mark as available again."""
        self.status = SeatStatus.AVAILABLE
        self._lock.release()

    def __repr__(self) -> str:
        return f"{self.seat.seat_id}({self.status.value})"
