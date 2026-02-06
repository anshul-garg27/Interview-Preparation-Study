"""
Snake entity for Snake and Ladder game.
A snake has a head (higher position) and tail (lower position).
Landing on the head sends the player down to the tail.
"""


class Snake:
    """Represents a snake on the board."""

    def __init__(self, head: int, tail: int):
        """
        Args:
            head: Position of the snake's head (higher number).
            tail: Position of the snake's tail (lower number).

        Raises:
            ValueError: If tail >= head.
        """
        if tail >= head:
            raise ValueError(f"Snake head ({head}) must be above tail ({tail})")
        self.head = head
        self.tail = tail

    def __repr__(self) -> str:
        return f"Snake({self.head}->{self.tail})"
