# Mock Interview: Chess Game Design

## Interview Setup
- **Level:** SDE-2 / L4
- **Duration:** 45 minutes
- **Interviewer:** Principal Engineer, 15 years experience
- **Format:** OOP-focused with deep polymorphism discussion

---

## The Interview Transcript

### [0:00 - 0:02] Opening

**INTERVIEWER:** "Design an online chess game. I'm particularly interested in your OOP design and how you model the pieces."

**CANDIDATE:** "Great. Chess is a rich domain for OOP - lots of different pieces with different behaviors. Let me ask some questions first."

---

### [0:02 - 0:08] Requirement Gathering Phase

**CANDIDATE:** "

1. **Is this a two-player game on the same machine, or networked?**"

**INTERVIEWER:** "Let's start with two players on the same system."

**CANDIDATE:** "2. **Do we need to implement all standard chess rules?** Castling, en passant, pawn promotion?"

**INTERVIEWER:** "Yes, all standard rules."

**CANDIDATE:** "3. **Do we need check, checkmate, and stalemate detection?**"

**INTERVIEWER:** "Yes, that's core functionality."

**CANDIDATE:** "4. **Should we support undo/redo of moves?**"

**INTERVIEWER:** "Include undo. We can skip redo."

**CANDIDATE:** "5. **Do we need a move timer (like blitz chess)?**"

**INTERVIEWER:** "Not for now."

**CANDIDATE:** "6. **Should we save/load game state?**"

**INTERVIEWER:** "Not for now, but keep the design extensible for it."

**CANDIDATE:** "7. **Any AI opponent, or strictly two human players?**"

**INTERVIEWER:** "Two humans, but I'd love to hear how you'd add AI later."

**CANDIDATE:** "Summary of requirements:

**Core:**
- 8x8 board, standard chess setup
- Two players, turn-based
- All piece movement rules including castling, en passant, pawn promotion
- Check, checkmate, stalemate detection
- Move validation (can't move into check)
- Undo functionality
- Move history

**Out of Scope:**
- Networking, AI, timers, save/load (but design for extensibility)"

> *INTERVIEWER NOTE: Good scope definition. Asking about special rules (castling, en passant) shows domain knowledge. Score: 4/5 - could have asked about draw conditions (50-move rule, threefold repetition).*

---

### [0:08 - 0:20] Design Phase - The OOP Deep Dive

**CANDIDATE:** "Let me identify the core entities:

1. `Game` - Orchestrates the entire game flow
2. `Board` - 8x8 grid of cells
3. `Cell` / `Square` - Individual position on the board
4. `Piece` - Abstract base class for all pieces
5. `Player` - Represents a player with their color
6. `Move` - Encapsulates a move (from, to, captured piece)
7. `MoveValidator` - Validates if a move is legal
8. `GameStatus` - Enum: ACTIVE, CHECK, CHECKMATE, STALEMATE, RESIGNED

Let me focus on the piece hierarchy since that's the core OOP challenge."

**INTERVIEWER:** "Yes, please walk me through how you'd model the pieces."

**CANDIDATE:** "Here's my approach:

```
Piece (Abstract Base Class)
  |-- King
  |-- Queen
  |-- Rook
  |-- Bishop
  |-- Knight
  |-- Pawn
```

The `Piece` abstract class defines:
- `color: Color` - WHITE or BLACK
- `position: tuple[int, int]` - current row, col
- `has_moved: bool` - needed for castling and pawn's first double move
- `get_possible_moves(board) -> list[Move]` - abstract method
- `symbol: str` - for display

Each subclass implements `get_possible_moves()` with its specific movement logic."

**INTERVIEWER:** "Interesting. Why not store the movement pattern as data instead of behavior? For example, a Knight could store `[(2,1), (2,-1), ...]` as its move offsets."

**CANDIDATE:** "That works for simple pieces like Knight and King where moves are fixed offsets. But it breaks down for:

1. **Sliding pieces** (Queen, Rook, Bishop): They move in a direction until blocked. That's not a fixed offset list - it's a ray-casting algorithm.
2. **Pawn:** Has completely irregular rules - moves forward, captures diagonally, has en passant, double move on first turn, and promotion. No offset list captures this.
3. **King:** Has castling which involves another piece moving too.

So I use a **hybrid approach**:
- Fixed-offset pieces (Knight, King basic moves) use offset data
- Sliding pieces use a shared `_slide()` helper method
- Special moves are handled by override methods"

> *INTERVIEWER NOTE: Excellent analysis. Candidate didn't just agree or disagree - they analyzed which approach works for which pieces. This shows engineering judgment.*

**CANDIDATE:** "Let me show the hierarchy in more detail:

```python
class Piece(ABC):
    def __init__(self, color: Color, position: tuple[int, int]):
        self._color = color
        self._position = position
        self._has_moved = False

    @abstractmethod
    def get_possible_moves(self, board: 'Board') -> list['Move']:
        pass

    def _slide(self, board, directions) -> list[tuple[int, int]]:
        \"\"\"Shared by Queen, Rook, Bishop - slide in a direction until blocked.\"\"\"
        moves = []
        for dr, dc in directions:
            r, c = self._position
            while True:
                r, c = r + dr, c + dc
                if not board.is_valid(r, c):
                    break
                target = board.get_piece(r, c)
                if target is None:
                    moves.append((r, c))
                elif target.color != self._color:
                    moves.append((r, c))  # Capture
                    break
                else:
                    break  # Blocked by own piece
        return moves
```

The `_slide()` method is defined in the base class and reused by Queen, Rook, and Bishop. This is the Template Method pattern in action."

**INTERVIEWER:** "How would you add a new piece type? Say we're implementing a chess variant with a piece called 'Archbishop' that moves like a Bishop + Knight."

**CANDIDATE:** "This is where OCP shines. I simply create a new subclass:

```python
class Archbishop(Piece):
    @property
    def symbol(self) -> str:
        return 'A' if self._color == Color.WHITE else 'a'

    def get_possible_moves(self, board: 'Board') -> list['Move']:
        moves = []
        # Bishop moves (sliding diagonals)
        moves.extend(self._slide(board, [
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]))
        # Knight moves (fixed offsets)
        knight_offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_offsets:
            r, c = self._position[0] + dr, self._position[1] + dc
            if board.is_valid(r, c):
                target = board.get_piece(r, c)
                if target is None or target.color != self._color:
                    moves.append((r, c))
        return moves
```

No existing code was modified. The Board doesn't care what type of piece it holds - it just calls `get_possible_moves()`. This is polymorphism doing the heavy lifting."

> *INTERVIEWER NOTE: Clean OCP demonstration. The Archbishop example perfectly shows why the abstract base class approach was right. Score: 5/5 for extensibility.*

**INTERVIEWER:** "Now, how do you handle check and checkmate?"

**CANDIDATE:** "This is the most complex part. Let me think through it:

**Check Detection:**
A king is in check if any opponent piece's `get_possible_moves()` includes the king's position.

```python
def is_in_check(self, color: Color) -> bool:
    king_pos = self._find_king(color)
    opponent = Color.BLACK if color == Color.WHITE else Color.WHITE
    for piece in self._get_pieces(opponent):
        possible = piece.get_possible_moves(self)
        if king_pos in [m.to_pos for m in possible]:
            return True
    return False
```

**Move Validation:**
A move is legal only if, after making it, the moving player's king is NOT in check. This means:
1. Temporarily make the move on the board
2. Check if own king is in check
3. Undo the temporary move
4. If king would be in check, the move is illegal

```python
def is_legal_move(self, move: Move) -> bool:
    # Make temporary move
    self._apply_move(move)
    # Check if own king is in check
    in_check = self.is_in_check(move.piece.color)
    # Undo
    self._undo_move(move)
    return not in_check
```

**Checkmate Detection:**
A player is in checkmate if:
1. Their king is currently in check, AND
2. They have NO legal moves (no piece can make any move that gets out of check)

```python
def is_checkmate(self, color: Color) -> bool:
    if not self.is_in_check(color):
        return False
    # Check if any legal move exists
    for piece in self._get_pieces(color):
        for move in piece.get_possible_moves(self):
            if self.is_legal_move(move):
                return False  # Found an escape
    return True  # No escape exists
```

**Stalemate:**
Same as checkmate but the king is NOT in check."

**INTERVIEWER:** "What's the time complexity of checkmate detection?"

**CANDIDATE:** "Let me analyze:
- We iterate all pieces of the current player: O(16) worst case
- For each piece, `get_possible_moves()` is at most O(27) for a queen
- For each possible move, `is_legal_move()` makes a temporary move and checks if any of the opponent's ~16 pieces can attack the king
- So: O(16 pieces * 27 moves * 16 opponent pieces * 27 moves) = O(16 * 27 * 16 * 27) ~ O(186,624)

That's about 200K operations per checkmate check - fast enough for a chess game."

> *INTERVIEWER NOTE: Complexity analysis was thorough and correct. Good sign.*

---

### [0:20 - 0:35] Full Code Implementation

**CANDIDATE:** "Let me write the complete code."

```python
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import copy


class Color(Enum):
    WHITE = "white"
    BLACK = "black"

    @property
    def opponent(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class GameStatus(Enum):
    ACTIVE = "active"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    RESIGNED = "resigned"
    DRAW = "draw"


@dataclass
class Move:
    piece: 'Piece'
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]
    captured: Optional['Piece'] = None
    is_castling: bool = False
    is_en_passant: bool = False
    promotion_piece: Optional[type] = None

    def __repr__(self):
        cols = "abcdefgh"
        fr = f"{cols[self.from_pos[1]]}{self.from_pos[0] + 1}"
        to = f"{cols[self.to_pos[1]]}{self.to_pos[0] + 1}"
        return f"{self.piece.symbol}: {fr} -> {to}"


# ---- Piece Hierarchy ----
class Piece(ABC):
    def __init__(self, color: Color, position: tuple[int, int]):
        self._color = color
        self._position = position
        self._has_moved = False

    @property
    def color(self) -> Color:
        return self._color

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, pos: tuple[int, int]):
        self._position = pos

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    @has_moved.setter
    def has_moved(self, val: bool):
        self._has_moved = val

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass

    @abstractmethod
    def get_possible_moves(self, board: 'Board') -> list[Move]:
        pass

    def _slide(self, board: 'Board',
               directions: list[tuple[int, int]]) -> list[Move]:
        moves = []
        for dr, dc in directions:
            r, c = self._position
            while True:
                r, c = r + dr, c + dc
                if not board.is_valid(r, c):
                    break
                target = board.get_piece(r, c)
                if target is None:
                    moves.append(Move(self, self._position, (r, c)))
                elif target.color != self._color:
                    moves.append(Move(self, self._position, (r, c),
                                      captured=target))
                    break
                else:
                    break
        return moves

    def _offset_moves(self, board: 'Board',
                      offsets: list[tuple[int, int]]) -> list[Move]:
        moves = []
        for dr, dc in offsets:
            r = self._position[0] + dr
            c = self._position[1] + dc
            if board.is_valid(r, c):
                target = board.get_piece(r, c)
                if target is None or target.color != self._color:
                    moves.append(Move(self, self._position, (r, c),
                                      captured=target))
        return moves


class King(Piece):
    OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1, 0), (1, 1)]

    @property
    def symbol(self) -> str:
        return 'K' if self._color == Color.WHITE else 'k'

    def get_possible_moves(self, board: 'Board') -> list[Move]:
        moves = self._offset_moves(board, self.OFFSETS)
        # Castling
        if not self._has_moved:
            moves.extend(self._castling_moves(board))
        return moves

    def _castling_moves(self, board: 'Board') -> list[Move]:
        moves = []
        row = self._position[0]

        # King-side castling
        rook = board.get_piece(row, 7)
        if (isinstance(rook, Rook) and not rook.has_moved
                and rook.color == self._color):
            if (board.get_piece(row, 5) is None
                    and board.get_piece(row, 6) is None):
                # Check that king doesn't pass through check
                if not board.is_square_attacked((row, 4), self._color.opponent) \
                   and not board.is_square_attacked((row, 5), self._color.opponent) \
                   and not board.is_square_attacked((row, 6), self._color.opponent):
                    moves.append(Move(self, self._position, (row, 6),
                                      is_castling=True))

        # Queen-side castling
        rook = board.get_piece(row, 0)
        if (isinstance(rook, Rook) and not rook.has_moved
                and rook.color == self._color):
            if (board.get_piece(row, 1) is None
                    and board.get_piece(row, 2) is None
                    and board.get_piece(row, 3) is None):
                if not board.is_square_attacked((row, 4), self._color.opponent) \
                   and not board.is_square_attacked((row, 3), self._color.opponent) \
                   and not board.is_square_attacked((row, 2), self._color.opponent):
                    moves.append(Move(self, self._position, (row, 2),
                                      is_castling=True))
        return moves


class Queen(Piece):
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]

    @property
    def symbol(self) -> str:
        return 'Q' if self._color == Color.WHITE else 'q'

    def get_possible_moves(self, board: 'Board') -> list[Move]:
        return self._slide(board, self.DIRECTIONS)


class Rook(Piece):
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    @property
    def symbol(self) -> str:
        return 'R' if self._color == Color.WHITE else 'r'

    def get_possible_moves(self, board: 'Board') -> list[Move]:
        return self._slide(board, self.DIRECTIONS)


class Bishop(Piece):
    DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    @property
    def symbol(self) -> str:
        return 'B' if self._color == Color.WHITE else 'b'

    def get_possible_moves(self, board: 'Board') -> list[Move]:
        return self._slide(board, self.DIRECTIONS)


class Knight(Piece):
    OFFSETS = [(2, 1), (2, -1), (-2, 1), (-2, -1),
               (1, 2), (1, -2), (-1, 2), (-1, -2)]

    @property
    def symbol(self) -> str:
        return 'N' if self._color == Color.WHITE else 'n'

    def get_possible_moves(self, board: 'Board') -> list[Move]:
        return self._offset_moves(board, self.OFFSETS)


class Pawn(Piece):
    @property
    def symbol(self) -> str:
        return 'P' if self._color == Color.WHITE else 'p'

    def get_possible_moves(self, board: 'Board') -> list[Move]:
        moves = []
        direction = 1 if self._color == Color.WHITE else -1
        r, c = self._position

        # Forward one
        nr = r + direction
        if board.is_valid(nr, c) and board.get_piece(nr, c) is None:
            moves.append(Move(self, self._position, (nr, c)))
            # Forward two on first move
            nnr = r + 2 * direction
            if not self._has_moved and board.get_piece(nnr, c) is None:
                moves.append(Move(self, self._position, (nnr, c)))

        # Diagonal captures
        for dc in [-1, 1]:
            nc = c + dc
            if board.is_valid(nr, nc):
                target = board.get_piece(nr, nc)
                if target and target.color != self._color:
                    moves.append(Move(self, self._position, (nr, nc),
                                      captured=target))

        # En passant
        if board.last_move:
            last = board.last_move
            if (isinstance(last.piece, Pawn)
                    and abs(last.from_pos[0] - last.to_pos[0]) == 2
                    and last.to_pos[0] == r
                    and abs(last.to_pos[1] - c) == 1):
                ep_col = last.to_pos[1]
                moves.append(Move(self, self._position,
                                  (nr, ep_col), captured=last.piece,
                                  is_en_passant=True))

        return moves


# ---- Board ----
class Board:
    def __init__(self):
        self._grid: list[list[Optional[Piece]]] = [
            [None] * 8 for _ in range(8)
        ]
        self.last_move: Optional[Move] = None
        self._setup_pieces()

    def _setup_pieces(self):
        # White pieces (rows 0-1)
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, cls in enumerate(order):
            self._grid[0][col] = cls(Color.WHITE, (0, col))
        for col in range(8):
            self._grid[1][col] = Pawn(Color.WHITE, (1, col))

        # Black pieces (rows 6-7)
        for col, cls in enumerate(order):
            self._grid[7][col] = cls(Color.BLACK, (7, col))
        for col in range(8):
            self._grid[6][col] = Pawn(Color.BLACK, (6, col))

    def is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        return self._grid[row][col]

    def set_piece(self, row: int, col: int, piece: Optional[Piece]):
        self._grid[row][col] = piece

    def get_pieces(self, color: Color) -> list[Piece]:
        pieces = []
        for row in self._grid:
            for piece in row:
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

    def find_king(self, color: Color) -> King:
        for piece in self.get_pieces(color):
            if isinstance(piece, King):
                return piece
        raise ValueError(f"No {color.value} king found")

    def is_square_attacked(self, pos: tuple[int, int],
                           by_color: Color) -> bool:
        for piece in self.get_pieces(by_color):
            for move in piece.get_possible_moves(self):
                if move.to_pos == pos:
                    return True
        return False

    def is_in_check(self, color: Color) -> bool:
        king = self.find_king(color)
        return self.is_square_attacked(king.position, color.opponent)

    def apply_move(self, move: Move):
        r1, c1 = move.from_pos
        r2, c2 = move.to_pos

        # Handle castling - move the rook too
        if move.is_castling:
            if c2 == 6:  # King-side
                rook = self._grid[r1][7]
                self._grid[r1][7] = None
                self._grid[r1][5] = rook
                rook.position = (r1, 5)
                rook.has_moved = True
            elif c2 == 2:  # Queen-side
                rook = self._grid[r1][0]
                self._grid[r1][0] = None
                self._grid[r1][3] = rook
                rook.position = (r1, 3)
                rook.has_moved = True

        # Handle en passant - remove captured pawn
        if move.is_en_passant:
            self._grid[r1][c2] = None

        # Move the piece
        self._grid[r2][c2] = move.piece
        self._grid[r1][c1] = None
        move.piece.position = (r2, c2)
        move.piece.has_moved = True

        # Handle pawn promotion
        if move.promotion_piece:
            promoted = move.promotion_piece(move.piece.color, (r2, c2))
            self._grid[r2][c2] = promoted

        self.last_move = move

    def display(self) -> str:
        lines = []
        lines.append("  a b c d e f g h")
        for row in range(7, -1, -1):
            row_str = f"{row + 1} "
            for col in range(8):
                piece = self._grid[row][col]
                row_str += (piece.symbol if piece else '.') + ' '
            lines.append(row_str)
        return '\n'.join(lines)


# ---- Game ----
class Player:
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color


class Game:
    def __init__(self, white_name: str, black_name: str):
        self._board = Board()
        self._players = {
            Color.WHITE: Player(white_name, Color.WHITE),
            Color.BLACK: Player(black_name, Color.BLACK),
        }
        self._current_turn = Color.WHITE
        self._status = GameStatus.ACTIVE
        self._move_history: list[Move] = []

    @property
    def status(self) -> GameStatus:
        return self._status

    def get_legal_moves(self, color: Color) -> list[Move]:
        legal = []
        for piece in self._board.get_pieces(color):
            for move in piece.get_possible_moves(self._board):
                if self._is_legal(move):
                    legal.append(move)
        return legal

    def _is_legal(self, move: Move) -> bool:
        # Simulate the move and check if own king is in check
        # Save state
        saved_grid = [row[:] for row in self._board._grid]
        saved_pos = move.piece.position
        saved_moved = move.piece.has_moved
        saved_last = self._board.last_move

        self._board.apply_move(move)
        in_check = self._board.is_in_check(move.piece.color)

        # Restore state
        self._board._grid = saved_grid
        move.piece.position = saved_pos
        move.piece.has_moved = saved_moved
        self._board.last_move = saved_last

        return not in_check

    def make_move(self, from_pos: tuple[int, int],
                  to_pos: tuple[int, int],
                  promotion: type = None) -> bool:
        piece = self._board.get_piece(*from_pos)
        if not piece or piece.color != self._current_turn:
            return False

        # Find the matching legal move
        legal_moves = self.get_legal_moves(self._current_turn)
        target_move = None
        for move in legal_moves:
            if move.from_pos == from_pos and move.to_pos == to_pos:
                target_move = move
                break

        if not target_move:
            return False

        # Handle pawn promotion
        if (isinstance(piece, Pawn)
                and to_pos[0] in (0, 7)):
            target_move.promotion_piece = promotion or Queen

        self._board.apply_move(target_move)
        self._move_history.append(target_move)

        # Switch turns and update game status
        self._current_turn = self._current_turn.opponent
        self._update_status()
        return True

    def _update_status(self):
        legal_moves = self.get_legal_moves(self._current_turn)
        in_check = self._board.is_in_check(self._current_turn)

        if not legal_moves:
            if in_check:
                self._status = GameStatus.CHECKMATE
            else:
                self._status = GameStatus.STALEMATE
        elif in_check:
            self._status = GameStatus.CHECK
        else:
            self._status = GameStatus.ACTIVE

    def undo(self) -> bool:
        if not self._move_history:
            return False
        # For full undo, we'd need a memento pattern or store board snapshots
        # Simplified: pop last move (full implementation would restore state)
        self._move_history.pop()
        self._current_turn = self._current_turn.opponent
        return True

    def resign(self):
        self._status = GameStatus.RESIGNED

    def display(self) -> str:
        header = f"Turn: {self._current_turn.value} | Status: {self._status.value}"
        return f"{header}\n{self._board.display()}"
```

---

### [0:35 - 0:40] Interviewer Deep-Dive Questions

**INTERVIEWER:** "I notice your `_is_legal` method makes a copy of the grid. Is there a cleaner way?"

**CANDIDATE:** "Yes, the **Memento pattern** would be cleaner. Instead of manually saving and restoring grid state, I'd create a `BoardMemento` class:

```python
class BoardMemento:
    def __init__(self, board: Board):
        self._state = copy.deepcopy(board._grid)
        self._last_move = board.last_move

    def restore(self, board: Board):
        board._grid = self._state
        board.last_move = self._last_move

# Usage in _is_legal:
memento = BoardMemento(self._board)
self._board.apply_move(move)
in_check = self._board.is_in_check(move.piece.color)
memento.restore(self._board)
```

The Memento encapsulates the save/restore logic and we don't expose Board internals."

**INTERVIEWER:** "How would you add an AI opponent?"

**CANDIDATE:** "I'd use the Strategy pattern for the player's move selection:

```python
class MoveStrategy(ABC):
    @abstractmethod
    def select_move(self, game: Game, color: Color) -> Move:
        pass

class HumanStrategy(MoveStrategy):
    def select_move(self, game, color):
        # Get input from UI
        pass

class MinimaxAIStrategy(MoveStrategy):
    def __init__(self, depth: int = 3):
        self._depth = depth

    def select_move(self, game, color):
        # Minimax with alpha-beta pruning
        best_move = None
        best_score = float('-inf')
        for move in game.get_legal_moves(color):
            score = self._minimax(game, move, self._depth,
                                   False, float('-inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _minimax(self, game, move, depth, is_maximizing, alpha, beta):
        # Standard minimax with alpha-beta pruning
        pass

class RandomAIStrategy(MoveStrategy):
    def select_move(self, game, color):
        import random
        moves = game.get_legal_moves(color)
        return random.choice(moves) if moves else None
```

The Player class gets a `strategy` field, and the Game loop calls `player.strategy.select_move()` instead of waiting for input."

**INTERVIEWER:** "What about the Observer pattern for the UI?"

**CANDIDATE:** "Yes, the Board or Game should notify observers when state changes:

```python
class GameObserver(ABC):
    @abstractmethod
    def on_move(self, move: Move): pass

    @abstractmethod
    def on_check(self, color: Color): pass

    @abstractmethod
    def on_game_over(self, status: GameStatus, winner: Color): pass

class ConsoleUI(GameObserver):
    def on_move(self, move):
        print(f"Move: {move}")

    def on_check(self, color):
        print(f"{color.value} is in CHECK!")

    def on_game_over(self, status, winner):
        print(f"Game over: {status.value}. Winner: {winner.value}")

class WebSocketUI(GameObserver):
    def on_move(self, move):
        self._ws.send(json.dumps({"type": "move", "data": str(move)}))
```

This decouples the game logic from the UI completely."

---

### [0:40 - 0:43] Edge Cases

**INTERVIEWER:** "What edge cases should we handle?"

**CANDIDATE:** "

1. **Stalemate vs Checkmate:** Already handled - both check if legal moves exist, but stalemate requires NOT being in check.

2. **Pawn promotion:** When a pawn reaches the last rank, must choose promotion piece. Default to Queen but allow Knight (sometimes Knight creates checkmate).

3. **En passant timing:** Only valid immediately after the opponent's double pawn move. My `last_move` tracking handles this.

4. **Castling through check:** King can't castle through or into check. My King._castling_moves checks all squares.

5. **Castling after rook moves:** The `has_moved` flag on Rook prevents this.

6. **50-move rule:** No pawn moves or captures for 50 moves = draw. Would need a counter.

7. **Threefold repetition:** Same position occurs 3 times = draw. Would need position hashing:

```python
def position_hash(self) -> str:
    # FEN-like representation for detecting repetition
    return ''.join(
        piece.symbol if piece else '.'
        for row in self._grid for piece in row
    ) + f'_{self._current_turn.value}'
```

8. **Insufficient material:** King vs King, King+Bishop vs King, etc. = draw.

9. **Invalid game state:** Multiple kings, impossible positions after undo."

---

## Interviewer Scoring

### Scoring Breakdown

| Criteria | Score (1-5) | Notes |
|----------|-------------|-------|
| **Requirements Gathering** | 4/5 | Good questions, missed draw conditions initially |
| **Object Identification** | 5/5 | Clean hierarchy, Move as first-class object |
| **Class Design & Relationships** | 5/5 | Piece hierarchy, _slide() shared method, Memento for undo |
| **Design Patterns** | 5/5 | Strategy (AI), Observer (UI), Memento (undo), Template Method (_slide) |
| **Code Quality** | 4/5 | Complete and clean, minor issue with _is_legal grid copy |
| **Communication** | 5/5 | Explained polymorphism tradeoffs beautifully |
| **Edge Cases** | 5/5 | Comprehensive chess knowledge, position hashing for repetition |

### Overall: **4.7/5 - Strong Hire**

### What Went Well
- Piece hierarchy was textbook polymorphism
- The _slide() method showed code reuse through inheritance correctly
- Archbishop extension showed OCP in practice
- Check/checkmate logic was well-reasoned with complexity analysis
- AI Strategy pattern was clean and practical
- Deep chess domain knowledge (en passant, castling rules)

### What Could Be Better
- _is_legal() initially used manual state save instead of Memento
- Undo implementation was incomplete (acknowledged by candidate)
- Could have discussed the Board as an 0x88 array for performance
- Missing draw conditions in initial requirements

### Key Differentiators
- **L3:** Would implement basic piece movement but struggle with check detection
- **L4 (shown):** Complete piece hierarchy, check/checkmate, multiple design patterns
- **L5:** Would discuss bitboard representation, Zobrist hashing, alpha-beta pruning details

---

## Key Takeaways for Candidates

1. **Chess is an OOP showcase** - Make the piece hierarchy your centerpiece
2. **Polymorphism is the star** - `get_possible_moves()` is the perfect abstract method
3. **Know the special rules** - Castling, en passant, promotion show domain knowledge
4. **Check detection is the hard part** - Practice the "simulate move, check, undo" pattern
5. **Design for extensibility** - The Archbishop example proves your design is open/closed
6. **Patterns come naturally** - Strategy for AI, Observer for UI, Memento for undo
