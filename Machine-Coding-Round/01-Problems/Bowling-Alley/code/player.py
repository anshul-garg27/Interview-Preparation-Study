"""Player class for the Bowling Alley system."""


class Player:
    """Represents a bowling player.

    Attributes:
        name: The player's name.
    """

    def __init__(self, name: str) -> None:
        """Initialize a Player.

        Args:
            name: Player's name.

        Raises:
            ValueError: If name is empty.
        """
        if not name or not name.strip():
            raise ValueError("Player name cannot be empty.")
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Player('{self.name}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
