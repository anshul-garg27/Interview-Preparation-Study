"""Bishop piece - slides diagonally."""

from piece import Piece
from enums import Color


class Bishop(Piece):
    """Bishop slides along diagonals."""

    def symbol(self) -> str:
        return "B" if self.color == Color.WHITE else "b"

    def get_possible_moves(self, board: "Board") -> list:
        return self._slide_moves(board, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
