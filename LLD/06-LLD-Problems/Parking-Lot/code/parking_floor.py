"""
ParkingFloor class for the Parking Lot system.
Each floor contains multiple parking spots and can find available spots.
"""

from enums import SpotType, VehicleType, VEHICLE_SPOT_MAP
from parking_spot import ParkingSpot


class ParkingFloor:
    """Represents one floor of the parking lot with multiple spots."""

    def __init__(self, floor_number: int, spots_config: dict[SpotType, int]) -> None:
        self._floor_number = floor_number
        self._spots: list[ParkingSpot] = []
        spot_counter = 1
        for spot_type, count in spots_config.items():
            for _ in range(count):
                spot_id = f"F{floor_number}-{spot_type.value[0]}{spot_counter}"
                self._spots.append(ParkingSpot(spot_id, spot_type, floor_number))
                spot_counter += 1

    @property
    def floor_number(self) -> int:
        return self._floor_number

    @property
    def spots(self) -> list[ParkingSpot]:
        return self._spots

    def find_available_spot(self, vehicle_type: VehicleType) -> ParkingSpot | None:
        """Find the first available spot compatible with the vehicle type."""
        compatible_types = VEHICLE_SPOT_MAP[vehicle_type]
        for spot in self._spots:
            if spot.is_available and spot.spot_type in compatible_types:
                return spot
        return None

    def get_availability(self) -> dict[SpotType, dict[str, int]]:
        """Return counts of total and available spots by type."""
        counts: dict[SpotType, dict[str, int]] = {}
        for spot in self._spots:
            key = spot.spot_type
            if key not in counts:
                counts[key] = {"total": 0, "available": 0}
            counts[key]["total"] += 1
            if spot.is_available:
                counts[key]["available"] += 1
        return counts

    def display_available(self) -> None:
        """Print availability for this floor."""
        avail = self.get_availability()
        print(f"  Floor {self._floor_number}:")
        for stype, info in avail.items():
            bar = "+" * info["available"] + "-" * (info["total"] - info["available"])
            print(f"    {stype.value:>8}: [{bar}] {info['available']}/{info['total']}")
