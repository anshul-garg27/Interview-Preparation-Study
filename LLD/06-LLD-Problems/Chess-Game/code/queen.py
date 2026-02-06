"""Queen piece - slides in all 8 directions."""

from piece import Piece
from enums import Color


class Queen(Piece):
    """Queen slides horizontally, vertically, and diagonally."""

    def symbol(self) -> str:
        return "Q" if self.color == Color.WHITE else "q"

    def get_possible_moves(self, board: "Board") -> list:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._slide_moves(board, directions)
