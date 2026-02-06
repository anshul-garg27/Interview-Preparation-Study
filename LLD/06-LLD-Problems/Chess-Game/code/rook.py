"""Rook piece - slides horizontally and vertically."""

from piece import Piece
from enums import Color


class Rook(Piece):
    """Rook slides along ranks and files."""

    def symbol(self) -> str:
        return "R" if self.color == Color.WHITE else "r"

    def get_possible_moves(self, board: "Board") -> list:
        return self._slide_moves(board, [(-1, 0), (1, 0), (0, -1), (0, 1)])
