"""Position on the chess board."""

COL_NAMES = "abcdefgh"


class Position:
    """Represents a square on the 8x8 chess board."""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def is_valid(self) -> bool:
        """Check if position is within board bounds."""
        return 0 <= self.row < 8 and 0 <= self.col < 8

    def to_notation(self) -> str:
        """Convert to algebraic notation (e.g., 'e4')."""
        return f"{COL_NAMES[self.col]}{8 - self.row}"

    @staticmethod
    def from_notation(notation: str) -> "Position":
        """Create Position from algebraic notation."""
        col = COL_NAMES.index(notation[0])
        row = 8 - int(notation[1])
        return Position(row, col)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __repr__(self) -> str:
        return self.to_notation()
