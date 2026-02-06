"""
Tic-Tac-Toe (Extensible NxN) - Low Level Design Implementation

Design Patterns Used:
- Command Pattern: Move as command (undo/redo/replay)
- Strategy Pattern: Win checking algorithms
- Factory Pattern: Player creation (Human, Computer)
- Observer Pattern: Game event notifications
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Dict, Tuple
from collections import defaultdict
import random


# ============================================================
# Enums
# ============================================================

class GameState(Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    DRAW = "draw"


# ============================================================
# Observer Pattern: Game Events
# ============================================================

class GameObserver(ABC):
    @abstractmethod
    def on_move(self, player: "Player", row: int, col: int):
        pass
    @abstractmethod
    def on_win(self, player: "Player"):
        pass
    @abstractmethod
    def on_draw(self):
        pass
    @abstractmethod
    def on_undo(self, player: "Player", row: int, col: int):
        pass


class ConsoleDisplay(GameObserver):
    def on_move(self, player, row, col):
        print(f"  {player.name} ({player.piece}) placed at ({row}, {col})")

    def on_win(self, player):
        print(f"\n  *** {player.name} ({player.piece}) WINS! ***")

    def on_draw(self):
        print(f"\n  *** DRAW! No winner. ***")

    def on_undo(self, player, row, col):
        print(f"  Undo: {player.name}'s move at ({row}, {col}) removed")


# ============================================================
# Board with O(1) Win Detection
# ============================================================

class Board:
    def __init__(self, size: int = 3):
        self.size = size
        self.grid: List[List[Optional[str]]] = [[None] * size for _ in range(size)]
        self.moves_count = 0
        # Counters for O(1) win detection
        self.row_counts: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.col_counts: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.diag_counts: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def is_valid_move(self, row: int, col: int) -> bool:
        return (0 <= row < self.size and 0 <= col < self.size
                and self.grid[row][col] is None)

    def place_piece(self, row: int, col: int, piece: str) -> bool:
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = piece
        self.moves_count += 1
        self.row_counts[row][piece] += 1
        self.col_counts[col][piece] += 1
        if row == col:
            self.diag_counts[0][piece] += 1
        if row + col == self.size - 1:
            self.diag_counts[1][piece] += 1
        return True

    def remove_piece(self, row: int, col: int) -> Optional[str]:
        piece = self.grid[row][col]
        if piece is None:
            return None
        self.grid[row][col] = None
        self.moves_count -= 1
        self.row_counts[row][piece] -= 1
        self.col_counts[col][piece] -= 1
        if row == col:
            self.diag_counts[0][piece] -= 1
        if row + col == self.size - 1:
            self.diag_counts[1][piece] -= 1
        return piece

    def check_winner(self, row: int, col: int, piece: str) -> bool:
        """O(1) win detection using counters."""
        if self.row_counts[row][piece] == self.size:
            return True
        if self.col_counts[col][piece] == self.size:
            return True
        if row == col and self.diag_counts[0][piece] == self.size:
            return True
        if row + col == self.size - 1 and self.diag_counts[1][piece] == self.size:
            return True
        return False

    def is_full(self) -> bool:
        return self.moves_count == self.size * self.size

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is None:
                    cells.append((r, c))
        return cells

    def display(self) -> str:
        lines = []
        col_header = "     " + "   ".join(str(c) for c in range(self.size))
        lines.append(col_header)
        separator = "   " + "+".join(["---"] * self.size)

        for r in range(self.size):
            row_str = f" {r}  "
            cells = []
            for c in range(self.size):
                piece = self.grid[r][c]
                cells.append(f" {piece if piece else '.'} ")
            row_str += "|".join(cells)
            lines.append(row_str)
            if r < self.size - 1:
                lines.append(separator)

        return "\n".join(lines)


# ============================================================
# Players
# ============================================================

class Player(ABC):
    def __init__(self, name: str, piece: str):
        self.name = name
        self.piece = piece

    @abstractmethod
    def get_move(self, board: Board) -> Tuple[int, int]:
        pass


class HumanPlayer(Player):
    """In demo mode, moves are pre-scripted."""
    def __init__(self, name: str, piece: str, moves: Optional[List[Tuple[int, int]]] = None):
        super().__init__(name, piece)
        self._moves = moves or []
        self._move_idx = 0

    def get_move(self, board: Board) -> Tuple[int, int]:
        if self._move_idx < len(self._moves):
            move = self._moves[self._move_idx]
            self._move_idx += 1
            return move
        # Fallback: first empty cell
        empty = board.get_empty_cells()
        return empty[0] if empty else (-1, -1)


class ComputerPlayer(Player):
    """Simple AI: takes center, then corners, then random."""
    def get_move(self, board: Board) -> Tuple[int, int]:
        center = board.size // 2
        if board.is_valid_move(center, center):
            return center, center
        # Try corners
        corners = [(0, 0), (0, board.size - 1),
                   (board.size - 1, 0), (board.size - 1, board.size - 1)]
        random.shuffle(corners)
        for r, c in corners:
            if board.is_valid_move(r, c):
                return r, c
        # Random empty
        empty = board.get_empty_cells()
        return random.choice(empty) if empty else (-1, -1)


class PlayerFactory:
    @staticmethod
    def create_player(name: str, piece: str, player_type: str = "human",
                      moves: Optional[List[Tuple[int, int]]] = None) -> Player:
        if player_type == "computer":
            return ComputerPlayer(name, piece)
        return HumanPlayer(name, piece, moves)


# ============================================================
# Command Pattern: MoveCommand
# ============================================================

class MoveCommand:
    def __init__(self, player: Player, row: int, col: int):
        self.player = player
        self.row = row
        self.col = col

    def execute(self, board: Board) -> bool:
        return board.place_piece(self.row, self.col, self.player.piece)

    def undo(self, board: Board):
        board.remove_piece(self.row, self.col)


# ============================================================
# Game
# ============================================================

class Game:
    def __init__(self, board_size: int = 3, players: Optional[List[Player]] = None):
        self.board = Board(board_size)
        self.players = players or []
        self.current_player_idx = 0
        self.move_history: List[MoveCommand] = []
        self.state = GameState.IN_PROGRESS
        self.winner: Optional[Player] = None
        self._observers: List[GameObserver] = []

        # Validate unique pieces
        pieces = [p.piece for p in self.players]
        if len(pieces) != len(set(pieces)):
            raise ValueError("Each player must have a unique piece.")

    def add_observer(self, observer: GameObserver):
        self._observers.append(observer)

    def _notify_move(self, player, row, col):
        for obs in self._observers:
            obs.on_move(player, row, col)

    def _notify_win(self, player):
        for obs in self._observers:
            obs.on_win(player)

    def _notify_draw(self):
        for obs in self._observers:
            obs.on_draw()

    def _notify_undo(self, player, row, col):
        for obs in self._observers:
            obs.on_undo(player, row, col)

    def get_current_player(self) -> Player:
        return self.players[self.current_player_idx]

    def make_move(self, row: int, col: int) -> str:
        if self.state != GameState.IN_PROGRESS:
            return "Game is already over."

        player = self.get_current_player()
        if not self.board.is_valid_move(row, col):
            return f"Invalid move ({row}, {col}). Cell occupied or out of bounds."

        cmd = MoveCommand(player, row, col)
        cmd.execute(self.board)
        self.move_history.append(cmd)
        self._notify_move(player, row, col)

        # Check win
        if self.board.check_winner(row, col, player.piece):
            self.state = GameState.WON
            self.winner = player
            self._notify_win(player)
            return f"{player.name} wins!"

        # Check draw
        if self.board.is_full():
            self.state = GameState.DRAW
            self._notify_draw()
            return "Draw!"

        # Next player
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        return "Move accepted."

    def undo_move(self) -> str:
        if not self.move_history:
            return "No moves to undo."

        cmd = self.move_history.pop()
        cmd.undo(self.board)
        self._notify_undo(cmd.player, cmd.row, cmd.col)

        # Reset game state if was won/drawn
        if self.state != GameState.IN_PROGRESS:
            self.state = GameState.IN_PROGRESS
            self.winner = None

        # Find the index of the player whose move was undone
        for i, p in enumerate(self.players):
            if p == cmd.player:
                self.current_player_idx = i
                break

        return f"Undid {cmd.player.name}'s move at ({cmd.row}, {cmd.col})."

    def play_auto(self) -> None:
        """Auto-play using players' get_move methods."""
        while self.state == GameState.IN_PROGRESS:
            player = self.get_current_player()
            row, col = player.get_move(self.board)
            self.make_move(row, col)

    def replay(self) -> None:
        """Replay the game from the beginning."""
        print("\n  --- GAME REPLAY ---")
        replay_board = Board(self.board.size)
        for i, cmd in enumerate(self.move_history):
            replay_board.place_piece(cmd.row, cmd.col, cmd.player.piece)
            print(f"\n  Move {i + 1}: {cmd.player.name} ({cmd.player.piece}) -> ({cmd.row}, {cmd.col})")
            print(replay_board.display())

    def is_over(self) -> bool:
        return self.state != GameState.IN_PROGRESS


# ============================================================
# Demo
# ============================================================

def main():
    print("=" * 55)
    print("     TIC-TAC-TOE (NxN) - LOW LEVEL DESIGN DEMO")
    print("=" * 55)

    # ---- Game 1: Human vs Human (3x3, scripted moves) ----
    print("\n" + "=" * 55)
    print("GAME 1: Human vs Human (3x3) - X wins on diagonal")
    print("=" * 55)

    # Pre-scripted moves for demo: X wins on main diagonal
    player_x = PlayerFactory.create_player("Alice", "X", "human",
                                           moves=[(0, 0), (1, 1), (2, 2)])
    player_o = PlayerFactory.create_player("Bob", "O", "human",
                                           moves=[(0, 1), (1, 0)])

    game1 = Game(board_size=3, players=[player_x, player_o])
    game1.add_observer(ConsoleDisplay())

    game1.play_auto()
    print(f"\n{game1.board.display()}")

    # Replay
    game1.replay()

    # ---- Game 2: Demonstrating Undo ----
    print("\n" + "=" * 55)
    print("GAME 2: Demonstrating Undo Functionality")
    print("=" * 55)

    p1 = PlayerFactory.create_player("Player1", "X", "human",
                                     moves=[(1, 1), (0, 0), (0, 2), (2, 0)])
    p2 = PlayerFactory.create_player("Player2", "O", "human",
                                     moves=[(0, 1), (2, 2), (1, 0)])

    game2 = Game(board_size=3, players=[p1, p2])
    game2.add_observer(ConsoleDisplay())

    # Play a few moves
    for _ in range(4):
        player = game2.get_current_player()
        row, col = player.get_move(game2.board)
        game2.make_move(row, col)

    print(f"\n  Board after 4 moves:")
    print(game2.board.display())

    # Undo last 2 moves
    print(f"\n  {game2.undo_move()}")
    print(f"  {game2.undo_move()}")
    print(f"\n  Board after 2 undos:")
    print(game2.board.display())

    # Continue playing
    print(f"\n  Continue playing...")
    game2.play_auto()
    print(f"\n{game2.board.display()}")

    # ---- Game 3: Draw scenario ----
    print("\n" + "=" * 55)
    print("GAME 3: Draw Scenario (3x3)")
    print("=" * 55)

    # Classic draw: X O X / X X O / O X O
    px = PlayerFactory.create_player("Alice", "X", "human",
                                     moves=[(0, 0), (1, 0), (0, 2), (1, 1), (2, 1)])
    po = PlayerFactory.create_player("Bob", "O", "human",
                                     moves=[(0, 1), (1, 2), (2, 0), (2, 2)])

    game3 = Game(board_size=3, players=[px, po])
    game3.add_observer(ConsoleDisplay())
    game3.play_auto()
    print(f"\n{game3.board.display()}")

    # ---- Game 4: 4x4 Board ----
    print("\n" + "=" * 55)
    print("GAME 4: 4x4 Board - X wins on a row")
    print("=" * 55)

    px4 = PlayerFactory.create_player("Alice", "X", "human",
                                      moves=[(0, 0), (0, 1), (0, 2), (0, 3)])
    po4 = PlayerFactory.create_player("Bob", "O", "human",
                                      moves=[(1, 0), (1, 1), (1, 2)])

    game4 = Game(board_size=4, players=[px4, po4])
    game4.add_observer(ConsoleDisplay())
    game4.play_auto()
    print(f"\n{game4.board.display()}")

    # ---- Game 5: Computer vs Computer ----
    print("\n" + "=" * 55)
    print("GAME 5: Computer vs Computer (3x3)")
    print("=" * 55)

    random.seed(42)
    cpu1 = PlayerFactory.create_player("CPU-X", "X", "computer")
    cpu2 = PlayerFactory.create_player("CPU-O", "O", "computer")

    game5 = Game(board_size=3, players=[cpu1, cpu2])
    game5.add_observer(ConsoleDisplay())
    game5.play_auto()
    print(f"\n{game5.board.display()}")

    print(f"\n  Result: {game5.state.value}")
    if game5.winner:
        print(f"  Winner: {game5.winner.name}")

    # ---- Summary ----
    print("\n" + "=" * 55)
    print("SUMMARY")
    print("=" * 55)
    games = [("Game 1 (3x3 H vs H)", game1),
             ("Game 2 (3x3 with Undo)", game2),
             ("Game 3 (3x3 Draw)", game3),
             ("Game 4 (4x4 H vs H)", game4),
             ("Game 5 (3x3 CPU vs CPU)", game5)]
    for label, g in games:
        result = g.state.value
        winner = g.winner.name if g.winner else "None"
        moves = len(g.move_history)
        print(f"  {label}: {result} | Winner: {winner} | Moves: {moves}")


if __name__ == "__main__":
    main()
