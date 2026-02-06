"""Pawn piece - moves forward, captures diagonally."""

from piece import Piece
from enums import Color


class Pawn(Piece):
    """Pawn moves forward one (or two from start), captures diagonally."""

    def symbol(self) -> str:
        return "P" if self.color == Color.WHITE else "p"

    def get_possible_moves(self, board: "Board") -> list:
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1

        # Forward one
        r = self.row + direction
        if self._in_bounds(r, self.col) and board.grid[r][self.col] is None:
            moves.append((r, self.col))
            # Forward two from start
            r2 = self.row + 2 * direction
            if self.row == start_row and board.grid[r2][self.col] is None:
                moves.append((r2, self.col))

        # Diagonal captures
        for dc in [-1, 1]:
            r, c = self.row + direction, self.col + dc
            if self._in_bounds(r, c) and board.grid[r][c] is not None:
                if board.grid[r][c].color != self.color:
                    moves.append((r, c))

        return moves
