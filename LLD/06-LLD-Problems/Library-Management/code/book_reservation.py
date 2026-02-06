"""BookReservation class - holds a book for a member."""

from datetime import datetime
from enums import ReservationStatus
from book import Book
from member import Member


class BookReservation:
    """A reservation request for a book that is currently unavailable."""

    _counter = 0

    def __init__(self, book: Book, member: Member):
        BookReservation._counter += 1
        self.reservation_id = f"RES-{BookReservation._counter:04d}"
        self.book = book
        self.member = member
        self.status = ReservationStatus.WAITING
        self.date = datetime.now()

    def fulfill(self) -> None:
        self.status = ReservationStatus.FULFILLED

    def cancel(self) -> None:
        self.status = ReservationStatus.CANCELLED

    def __repr__(self) -> str:
        return (f"Reservation({self.reservation_id}, {self.member.name}, "
                f"'{self.book.title}', {self.status.value})")
