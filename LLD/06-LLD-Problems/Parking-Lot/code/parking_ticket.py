"""
ParkingTicket class for the Parking Lot system.
Issued on entry, tracks time and calculates fee on exit.
"""

import threading
from datetime import datetime

from enums import TicketStatus, RATE_PER_HOUR
from vehicle import Vehicle
from parking_spot import ParkingSpot


class ParkingTicket:
    """Ticket issued when a vehicle enters the parking lot."""

    _counter: int = 0
    _lock = threading.Lock()

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot) -> None:
        with ParkingTicket._lock:
            ParkingTicket._counter += 1
            self.ticket_id = f"TKT-{ParkingTicket._counter:04d}"
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time: datetime = datetime.now()
        self.exit_time: datetime | None = None
        self.status: TicketStatus = TicketStatus.ACTIVE
        self.amount_paid: float = 0.0

    def calculate_fee(self, exit_time: datetime | None = None) -> float:
        """Calculate parking fee based on hours parked and spot type."""
        end = exit_time or datetime.now()
        hours = max(1, (end - self.entry_time).seconds // 3600 + 1)
        return hours * RATE_PER_HOUR[self.spot.spot_type]

    def mark_paid(self, amount: float) -> None:
        """Mark this ticket as paid."""
        self.amount_paid = amount
        self.status = TicketStatus.PAID

    def mark_exited(self) -> None:
        """Mark this ticket as exited."""
        self.status = TicketStatus.EXITED

    def __repr__(self) -> str:
        return (f"Ticket({self.ticket_id}, {self.vehicle}, "
                f"Spot={self.spot.spot_id}, Status={self.status.value})")
