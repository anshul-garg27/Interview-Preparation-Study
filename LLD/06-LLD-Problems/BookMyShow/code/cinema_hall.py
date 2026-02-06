"""CinemaHall (Screen) with seat layout."""

from enums import SeatType, SeatStatus
from seat import Seat


class CinemaHall:
    """A screen/auditorium in a cinema with a fixed seat layout."""

    def __init__(self, hall_id: str, name: str, seat_layout: dict):
        self.hall_id = hall_id
        self.name = name
        self.seats: dict[str, Seat] = {}
        self._create_seats(seat_layout)

    def _create_seats(self, layout: dict) -> None:
        """Create seats from layout: {SeatType: [(row_letter, count)]}."""
        for seat_type, rows in layout.items():
            for row_letter, count in rows:
                for i in range(1, count + 1):
                    sid = f"{row_letter}{i}"
                    self.seats[sid] = Seat(sid, row_letter, i, seat_type)

    def display_layout(self, show=None) -> None:
        """Print seat map, marking booked seats for a show."""
        print(f"\n    Screen: {self.name}")
        print(f"    {'=' * 40}")
        print(f"    {'[  SCREEN  ]':^40}")
        print()
        rows: dict[str, list[Seat]] = {}
        for seat in self.seats.values():
            rows.setdefault(seat.row, []).append(seat)
        for row_letter in sorted(rows.keys()):
            seats = sorted(rows[row_letter], key=lambda s: s.number)
            row_str = f"    {row_letter}: "
            for s in seats:
                booked = show and s.seat_id in show.booked_seats
                row_str += "[XX] " if booked else "[  ] "
            print(row_str)
        print(f"    Legend: [  ]=Available  [XX]=Booked")
