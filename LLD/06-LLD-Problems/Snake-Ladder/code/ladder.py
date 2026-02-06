"""
Ladder entity for Snake and Ladder game.
A ladder has a start (bottom) and end (top).
Landing on the bottom sends the player up to the top.
"""


class Ladder:
    """Represents a ladder on the board."""

    def __init__(self, start: int, end: int):
        """
        Args:
            start: Bottom of the ladder (lower number).
            end: Top of the ladder (higher number).

        Raises:
            ValueError: If end <= start.
        """
        if end <= start:
            raise ValueError(f"Ladder top ({end}) must be above bottom ({start})")
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Ladder({self.start}->{self.end})"
