"""Abstract base class for all chess pieces."""

from abc import ABC, abstractmethod
from enums import Color


class Piece(ABC):
    """Base class for chess pieces."""

    def __init__(self, color: Color, row: int, col: int):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False

    @abstractmethod
    def get_possible_moves(self, board: "Board") -> list:
        """Return list of (row, col) tuples this piece can move to."""
        pass

    @abstractmethod
    def symbol(self) -> str:
        """Single character symbol for display."""
        pass

    def __repr__(self) -> str:
        return self.symbol()

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < 8 and 0 <= c < 8

    def _slide_moves(self, board: "Board", directions: list) -> list:
        """Generate moves for sliding pieces (Rook, Bishop, Queen)."""
        moves = []
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while self._in_bounds(r, c):
                target = board.grid[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves
