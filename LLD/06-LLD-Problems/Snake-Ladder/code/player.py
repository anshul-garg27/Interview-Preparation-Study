"""
Player entity for Snake and Ladder game.
Tracks the player's name, position, and win status.
"""


class Player:
    """Represents a player in the game."""

    def __init__(self, name: str):
        """
        Args:
            name: Display name of the player.
        """
        self.name = name
        self.position: int = 0  # 0 means not yet on the board
        self.has_won: bool = False

    def __repr__(self) -> str:
        return f"{self.name}(pos={self.position})"
