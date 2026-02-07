"""BowlingAlley class managing multiple lanes and bookings."""

from typing import List, Optional

from enums import LaneStatus
from player import Player
from lane import Lane
from booking import Booking
from game import Game


class BowlingAlley:
    """Manages the entire bowling alley with lanes and bookings.

    Provides a facade for lane management, booking, and game operations.

    Attributes:
        name: Name of the bowling alley.
        lanes: List of lanes in the alley.
        bookings: List of all bookings made.
    """

    def __init__(self, name: str, num_lanes: int) -> None:
        """Initialize a BowlingAlley.

        Args:
            name: Name of the alley.
            num_lanes: Number of lanes to create.

        Raises:
            ValueError: If name is empty or num_lanes < 1.
        """
        if not name or not name.strip():
            raise ValueError("Alley name cannot be empty.")
        if num_lanes < 1:
            raise ValueError("Must have at least 1 lane.")

        self.name = name
        self.lanes: List[Lane] = [Lane(i + 1) for i in range(num_lanes)]
        self.bookings: List[Booking] = []

    def get_available_lanes(self) -> List[Lane]:
        """Get all available lanes.

        Returns:
            List of lanes with AVAILABLE status.
        """
        return [lane for lane in self.lanes if lane.status == LaneStatus.AVAILABLE]

    def get_lane(self, lane_id: int) -> Optional[Lane]:
        """Get a lane by ID.

        Args:
            lane_id: The lane ID to find.

        Returns:
            The Lane, or None if not found.
        """
        for lane in self.lanes:
            if lane.lane_id == lane_id:
                return lane
        return None

    def book_lane(
        self, time_slot: str, players: List[Player], lane_id: Optional[int] = None
    ) -> Booking:
        """Book a lane for players.

        If lane_id is specified, books that specific lane.
        Otherwise, books the first available lane.

        Args:
            time_slot: Time slot description.
            players: List of players.
            lane_id: Optional specific lane to book.

        Returns:
            The Booking object.

        Raises:
            ValueError: If no available lane or specified lane unavailable.
        """
        if lane_id is not None:
            lane = self.get_lane(lane_id)
            if lane is None:
                raise ValueError(f"Lane {lane_id} does not exist.")
            if lane.status != LaneStatus.AVAILABLE:
                raise ValueError(f"Lane {lane_id} is not available.")
        else:
            available = self.get_available_lanes()
            if not available:
                raise ValueError("No lanes available.")
            lane = available[0]

        booking = Booking(lane, time_slot, players)
        self.bookings.append(booking)
        return booking

    def start_game_on_lane(self, lane: Lane, players: List[Player]) -> List[Game]:
        """Start a game on a specific lane.

        Args:
            lane: The lane to start the game on.
            players: List of players.

        Returns:
            List of Game objects.
        """
        return lane.start_game(players)

    def release_lane(self, lane_id: int) -> None:
        """Release a lane (end game and make available).

        Args:
            lane_id: The lane ID to release.

        Raises:
            ValueError: If lane not found.
        """
        lane = self.get_lane(lane_id)
        if lane is None:
            raise ValueError(f"Lane {lane_id} does not exist.")
        lane.end_game()

    def __str__(self) -> str:
        available = len(self.get_available_lanes())
        return f"{self.name} ({len(self.lanes)} lanes, {available} available)"
