"""Chess board with piece placement and move validation."""

from enums import Color
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from piece import Piece


class Board:
    """8x8 chess board with pieces."""

    COL_NAMES = "abcdefgh"

    def __init__(self):
        self.grid: list[list[Piece | None]] = [[None] * 8 for _ in range(8)]
        self._setup_pieces()

    def _setup_pieces(self) -> None:
        """Place all 32 pieces in standard starting position."""
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_cls in enumerate(back_rank):
            self.grid[0][col] = piece_cls(Color.BLACK, 0, col)
            self.grid[7][col] = piece_cls(Color.WHITE, 7, col)
        for col in range(8):
            self.grid[1][col] = Pawn(Color.BLACK, 1, col)
            self.grid[6][col] = Pawn(Color.WHITE, 6, col)

    def get_piece(self, row: int, col: int) -> Piece | None:
        """Get piece at given position."""
        return self.grid[row][col]

    def find_king(self, color: Color) -> King | None:
        """Find the king of given color."""
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and isinstance(p, King) and p.color == color:
                    return p
        return None

    def is_square_attacked(self, row: int, col: int, by_color: Color) -> bool:
        """Check if a square is attacked by any piece of given color."""
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == by_color:
                    if (row, col) in p.get_possible_moves(self):
                        return True
        return False

    def is_in_check(self, color: Color) -> bool:
        """Check if the given color's king is in check."""
        king = self.find_king(color)
        if not king:
            return False
        opponent = Color.BLACK if color == Color.WHITE else Color.WHITE
        return self.is_square_attacked(king.row, king.col, opponent)

    def move_piece(self, from_r: int, from_c: int,
                   to_r: int, to_c: int) -> Piece | None:
        """Execute a move. Returns captured piece or None."""
        piece = self.grid[from_r][from_c]
        captured = self.grid[to_r][to_c]
        self.grid[to_r][to_c] = piece
        self.grid[from_r][from_c] = None
        piece.row = to_r
        piece.col = to_c
        piece.has_moved = True
        return captured

    def undo_move(self, from_r: int, from_c: int,
                  to_r: int, to_c: int, captured: Piece | None) -> None:
        """Undo a previously executed move."""
        piece = self.grid[to_r][to_c]
        self.grid[from_r][from_c] = piece
        self.grid[to_r][to_c] = captured
        piece.row = from_r
        piece.col = from_c

    def is_valid_move(self, from_r: int, from_c: int,
                      to_r: int, to_c: int) -> bool:
        """Check if move is legal (valid + doesn't leave king in check)."""
        piece = self.grid[from_r][from_c]
        if not piece:
            return False
        if (to_r, to_c) not in piece.get_possible_moves(self):
            return False
        captured = self.move_piece(from_r, from_c, to_r, to_c)
        in_check = self.is_in_check(piece.color)
        self.undo_move(from_r, from_c, to_r, to_c, captured)
        return not in_check

    def has_legal_moves(self, color: Color) -> bool:
        """Check if the given color has any legal moves."""
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color:
                    for mr, mc in p.get_possible_moves(self):
                        if self.is_valid_move(r, c, mr, mc):
                            return True
        return False

    @staticmethod
    def pos_to_notation(row: int, col: int) -> str:
        return f"{Board.COL_NAMES[col]}{8 - row}"

    @staticmethod
    def notation_to_pos(notation: str) -> tuple[int, int]:
        col = Board.COL_NAMES.index(notation[0])
        row = 8 - int(notation[1])
        return row, col

    def display(self) -> None:
        """Print the board to console."""
        print()
        print("    a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")
        for r in range(8):
            row_str = f"{8 - r} |"
            for c in range(8):
                p = self.grid[r][c]
                sym = str(p) if p else " "
                row_str += f" {sym} |"
            row_str += f" {8 - r}"
            print(row_str)
            print("  +---+---+---+---+---+---+---+---+")
        print("    a   b   c   d   e   f   g   h")
        print()
