"""Knight piece - moves in an L-shape."""

from piece import Piece
from enums import Color


class Knight(Piece):
    """Knight moves in L-shape: 2+1 squares."""

    def symbol(self) -> str:
        return "N" if self.color == Color.WHITE else "n"

    def get_possible_moves(self, board: "Board") -> list:
        moves = []
        deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in deltas:
            r, c = self.row + dr, self.col + dc
            if self._in_bounds(r, c):
                target = board.grid[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves
