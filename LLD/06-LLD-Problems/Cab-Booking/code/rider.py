"""Rider class for the Cab Booking System."""

from location import Location
from rating import Rating


class Rider:
    """A customer who requests rides."""

    def __init__(self, rider_id: str, name: str, phone: str, location: Location):
        self.rider_id = rider_id
        self.name = name
        self.phone = phone
        self.location = location
        self.rating = Rating()
        self.ride_history: list = []

    def __repr__(self) -> str:
        return f"Rider({self.name}, Rating={self.rating.average:.1f})"
