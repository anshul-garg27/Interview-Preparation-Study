"""Enums for Chess Game."""

from enum import Enum


class Color(Enum):
    """Player color in chess."""
    WHITE = "White"
    BLACK = "Black"


class GameStatus(Enum):
    """Current status of the chess game."""
    ACTIVE = "Active"
    CHECK = "Check"
    CHECKMATE = "Checkmate"
    STALEMATE = "Stalemate"
    RESIGNED = "Resigned"
