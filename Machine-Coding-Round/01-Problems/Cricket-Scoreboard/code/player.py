"""Player class representing a cricket player."""


class Player:
    """Represents a cricket player with batting and bowling capabilities.

    Attributes:
        name: Full name of the player.
        is_batsman: Whether the player is primarily a batsman.
        is_bowler: Whether the player is primarily a bowler.
    """

    def __init__(
        self, name: str, is_batsman: bool = True, is_bowler: bool = False
    ) -> None:
        """Initialize a Player.

        Args:
            name: Player's name.
            is_batsman: Whether player bats (default True).
            is_bowler: Whether player bowls (default False).

        Raises:
            ValueError: If name is empty.
        """
        if not name or not name.strip():
            raise ValueError("Player name cannot be empty.")
        self.name = name
        self.is_batsman = is_batsman
        self.is_bowler = is_bowler

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
