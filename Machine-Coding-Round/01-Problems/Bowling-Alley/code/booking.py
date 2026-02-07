"""Booking class for lane reservations."""

import uuid
from datetime import datetime
from typing import List

from player import Player
from lane import Lane


class Booking:
    """Represents a lane booking/reservation.

    Attributes:
        booking_id: Unique identifier for the booking.
        lane: The booked lane.
        time_slot: The reserved time slot string.
        players: List of players for this booking.
        created_at: When the booking was made.
    """

    def __init__(
        self, lane: Lane, time_slot: str, players: List[Player]
    ) -> None:
        """Initialize a Booking.

        Args:
            lane: The lane to book.
            time_slot: Time slot description (e.g., "6:00 PM - 7:00 PM").
            players: List of players.

        Raises:
            ValueError: If time_slot is empty or no players.
        """
        if not time_slot or not time_slot.strip():
            raise ValueError("Time slot cannot be empty.")
        if not players:
            raise ValueError("At least one player is required.")

        self.booking_id: str = str(uuid.uuid4())[:8]
        self.lane = lane
        self.time_slot = time_slot
        self.players = players
        self.created_at: datetime = datetime.now()

    def __str__(self) -> str:
        player_names = ", ".join(p.name for p in self.players)
        return (
            f"Booking({self.booking_id}) | Lane {self.lane.lane_id} | "
            f"{self.time_slot} | Players: {player_names}"
        )

    def __repr__(self) -> str:
        return f"Booking(id={self.booking_id}, lane={self.lane.lane_id})"
