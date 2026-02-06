"""Player in a chess game."""

from enums import Color
from piece import Piece


class Player:
    """Represents a chess player."""

    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color
        self.captured_pieces: list[Piece] = []

    def add_capture(self, piece: Piece) -> None:
        """Record a captured enemy piece."""
        self.captured_pieces.append(piece)

    def __repr__(self) -> str:
        return f"Player({self.name}, {self.color.value})"
