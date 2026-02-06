"""
ParkingLot class - the main Singleton entry point.
Manages floors, vehicle entry/exit, and coordinates payments.
"""

import threading

from enums import TicketStatus
from vehicle import Vehicle
from parking_floor import ParkingFloor
from parking_ticket import ParkingTicket
from payment import PaymentStrategy, PaymentProcessor
from display_board import DisplayBoard


class ParkingLot:
    """
    Singleton Parking Lot managing multiple floors.
    Thread-safe entry and exit operations.
    """

    _instance: "ParkingLot | None" = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> "ParkingLot":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name: str = "Default Lot") -> None:
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.name = name
        self._floors: list[ParkingFloor] = []
        self._active_tickets: dict[str, ParkingTicket] = {}
        self._op_lock = threading.Lock()
        self._display = DisplayBoard(name)

    @property
    def floors(self) -> list[ParkingFloor]:
        return self._floors

    def add_floor(self, floor: ParkingFloor) -> None:
        """Add a floor to the parking lot."""
        self._floors.append(floor)

    def enter(self, vehicle: Vehicle) -> ParkingTicket | None:
        """Park a vehicle, returning a ticket or None if full."""
        with self._op_lock:
            if vehicle.license_plate in self._active_tickets:
                print(f"  [WARN] {vehicle} is already parked!")
                return None
            for floor in self._floors:
                spot = floor.find_available_spot(vehicle.vehicle_type)
                if spot:
                    spot.assign_vehicle(vehicle)
                    ticket = ParkingTicket(vehicle, spot)
                    self._active_tickets[vehicle.license_plate] = ticket
                    print(f"  [ENTER] {vehicle} -> {spot.spot_id} | {ticket.ticket_id}")
                    return ticket
            print(f"  [FULL] No spot available for {vehicle}")
            return None

    def pay_and_exit(self, license_plate: str, strategy: PaymentStrategy,
                     simulated_hours: int = 1) -> bool:
        """Process payment and exit a vehicle."""
        with self._op_lock:
            ticket = self._active_tickets.get(license_plate)
            if not ticket:
                print(f"  [ERROR] No active ticket for {license_plate}")
                return False
            processor = PaymentProcessor(ticket, strategy)
            if processor.process(simulated_hours):
                ticket.spot.remove_vehicle()
                ticket.mark_exited()
                del self._active_tickets[license_plate]
                print(f"  [EXIT] {ticket.vehicle} | {simulated_hours}h | "
                      f"Fee=${ticket.amount_paid:.2f} | {ticket.ticket_id}")
                return True
            return False

    def display_availability(self) -> None:
        """Show the display board with current availability."""
        self._display.show(self._floors)
