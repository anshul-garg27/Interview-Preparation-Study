"""Team class representing a cricket team."""

from typing import List

from player import Player


class Team:
    """Represents a cricket team with up to 11 players.

    Attributes:
        name: Name of the team.
        players: List of players in the team.
    """

    def __init__(self, name: str, players: List[Player]) -> None:
        """Initialize a Team.

        Args:
            name: Team name.
            players: List of players.

        Raises:
            ValueError: If team name is empty or too many/few players.
        """
        if not name or not name.strip():
            raise ValueError("Team name cannot be empty.")
        if len(players) < 2:
            raise ValueError("Team must have at least 2 players.")
        if len(players) > 11:
            raise ValueError("Team cannot have more than 11 players.")
        self.name = name
        self.players = players

    def get_player(self, name: str) -> Player:
        """Find a player by name.

        Args:
            name: Player name to find.

        Returns:
            The Player object.

        Raises:
            ValueError: If player not found.
        """
        for player in self.players:
            if player.name == name:
                return player
        raise ValueError(f"Player '{name}' not found in team {self.name}.")

    def get_bowlers(self) -> List[Player]:
        """Get all players who can bowl."""
        return [p for p in self.players if p.is_bowler]

    def __str__(self) -> str:
        return f"{self.name} ({len(self.players)} players)"

    def __repr__(self) -> str:
        return f"Team('{self.name}')"
