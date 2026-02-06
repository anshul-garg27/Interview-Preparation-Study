"""King piece - moves one square in any direction."""

from piece import Piece
from enums import Color


class King(Piece):
    """King moves one square in any direction."""

    def symbol(self) -> str:
        return "K" if self.color == Color.WHITE else "k"

    def get_possible_moves(self, board: "Board") -> list:
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = self.row + dr, self.col + dc
                if self._in_bounds(r, c):
                    target = board.grid[r][c]
                    if target is None or target.color != self.color:
                        moves.append((r, c))
        return moves
