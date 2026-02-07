"""Lane class representing a single bowling lane."""

from typing import List, Optional

from enums import LaneStatus
from player import Player
from game import Game


class Lane:
    """Represents a single bowling lane in the alley.

    Manages lane status and hosts games for players.

    Attributes:
        lane_id: Unique identifier for the lane.
        status: Current status of the lane.
        games: List of active games on this lane.
    """

    def __init__(self, lane_id: int) -> None:
        """Initialize a Lane.

        Args:
            lane_id: The lane number/ID.
        """
        self.lane_id = lane_id
        self.status: LaneStatus = LaneStatus.AVAILABLE
        self.games: List[Game] = []

    def start_game(self, players: List[Player]) -> List[Game]:
        """Start a new game on this lane for the given players.

        Args:
            players: List of players for the game.

        Returns:
            List of Game objects (one per player).

        Raises:
            ValueError: If lane is not available or no players given.
        """
        if self.status != LaneStatus.AVAILABLE:
            raise ValueError(f"Lane {self.lane_id} is not available ({self.status.value}).")
        if not players:
            raise ValueError("At least one player is required.")

        self.status = LaneStatus.OCCUPIED
        self.games = [Game(player) for player in players]
        return self.games

    def end_game(self) -> None:
        """End the current game and release the lane."""
        self.games = []
        self.status = LaneStatus.AVAILABLE

    def set_maintenance(self) -> None:
        """Put the lane in maintenance mode."""
        if self.status == LaneStatus.OCCUPIED:
            raise ValueError("Cannot set maintenance while lane is occupied.")
        self.status = LaneStatus.MAINTENANCE

    def clear_maintenance(self) -> None:
        """Remove the lane from maintenance mode."""
        if self.status == LaneStatus.MAINTENANCE:
            self.status = LaneStatus.AVAILABLE

    def __str__(self) -> str:
        return f"Lane {self.lane_id} ({self.status.value})"

    def __repr__(self) -> str:
        return f"Lane(id={self.lane_id}, status={self.status.value})"
