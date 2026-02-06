"""
DisplayBoard for the Parking Lot system.
Acts as an Observer - shows real-time availability per floor.
"""

from parking_floor import ParkingFloor


class DisplayBoard:
    """Displays available spots per floor (Observer pattern)."""

    def __init__(self, lot_name: str) -> None:
        self._lot_name = lot_name

    def show(self, floors: list[ParkingFloor]) -> None:
        """Print the availability dashboard for all floors."""
        print(f"\n{'='*50}")
        print(f"  {self._lot_name} - Availability Dashboard")
        print(f"{'='*50}")
        for floor in floors:
            floor.display_available()
        print(f"{'='*50}")
