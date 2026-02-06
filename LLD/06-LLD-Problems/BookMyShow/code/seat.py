"""Seat entity for a cinema hall."""

from enums import SeatType

SEAT_PRICES = {
    SeatType.REGULAR: 150,
    SeatType.PREMIUM: 300,
    SeatType.VIP: 500,
}


class Seat:
    """Represents a physical seat in a cinema hall."""

    def __init__(self, seat_id: str, row: str, number: int,
                 seat_type: SeatType):
        self.seat_id = seat_id
        self.row = row
        self.number = number
        self.seat_type = seat_type
        self.price = SEAT_PRICES[seat_type]

    def __repr__(self) -> str:
        return f"{self.row}{self.number}({self.seat_type.value})"
