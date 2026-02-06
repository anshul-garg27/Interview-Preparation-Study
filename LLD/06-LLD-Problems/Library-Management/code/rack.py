"""Rack class - physical location of a book in the library."""


class Rack:
    """Represents a shelf/rack where books are stored."""

    def __init__(self, number: int, location: str = ""):
        self.number = number
        self.location = location or f"Aisle-{number}"

    def __repr__(self) -> str:
        return f"Rack({self.number}, {self.location})"
