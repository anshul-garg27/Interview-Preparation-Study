"""Move record for chess game history."""

from piece import Piece
from position import Position


class Move:
    """Records a single move in the game."""

    def __init__(self, piece: Piece, start: Position, end: Position,
                 captured_piece: Piece = None):
        self.piece = piece
        self.start = start
        self.end = end
        self.captured_piece = captured_piece

    def __repr__(self) -> str:
        capture = f"x{self.captured_piece.symbol()}" if self.captured_piece else ""
        return (f"{self.piece.__class__.__name__}({self.piece.symbol()}) "
                f"{self.start}->{self.end}{capture}")
