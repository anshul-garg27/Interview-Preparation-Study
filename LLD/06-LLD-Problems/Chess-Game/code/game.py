"""Chess game controller managing turns, check, and checkmate."""

from enums import Color, GameStatus
from board import Board
from move import Move
from player import Player
from position import Position


class Game:
    """Manages a chess game between two players."""

    def __init__(self, white_name: str = "White", black_name: str = "Black"):
        self.board = Board()
        self.players = {
            Color.WHITE: Player(white_name, Color.WHITE),
            Color.BLACK: Player(black_name, Color.BLACK),
        }
        self.current_turn = Color.WHITE
        self.status = GameStatus.ACTIVE
        self.move_history: list[Move] = []
        self.winner: Player | None = None

    def switch_turn(self) -> None:
        self.current_turn = (
            Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        )

    def make_move(self, from_notation: str, to_notation: str) -> bool:
        """Play a move using algebraic notation (e.g., 'e2' to 'e4')."""
        from_r, from_c = Board.notation_to_pos(from_notation)
        to_r, to_c = Board.notation_to_pos(to_notation)

        piece = self.board.get_piece(from_r, from_c)
        if not piece:
            print(f"  [Invalid] No piece at {from_notation}")
            return False
        if piece.color != self.current_turn:
            print(f"  [Invalid] Not {piece.color.value}'s turn")
            return False
        if not self.board.is_valid_move(from_r, from_c, to_r, to_c):
            print(f"  [Invalid] {piece.symbol()} cannot move "
                  f"{from_notation}->{to_notation}")
            return False

        captured = self.board.move_piece(from_r, from_c, to_r, to_c)
        move = Move(piece, Position.from_notation(from_notation),
                    Position.from_notation(to_notation), captured)
        self.move_history.append(move)

        if captured:
            self.players[self.current_turn].add_capture(captured)

        move_num = len(self.move_history)
        capture_str = f" captures {captured.symbol()}" if captured else ""
        print(f"  Move {move_num}: {piece.color.value} "
              f"{piece.__class__.__name__}({piece.symbol()}) "
              f"{from_notation}->{to_notation}{capture_str}")

        # Check game state for opponent
        opponent = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        if self.board.is_in_check(opponent):
            if not self.board.has_legal_moves(opponent):
                print(f"\n  *** CHECKMATE! {self.current_turn.value} wins! ***")
                self.status = GameStatus.CHECKMATE
                self.winner = self.players[self.current_turn]
                return True
            print(f"  ** {opponent.value} is in CHECK! **")
            self.status = GameStatus.CHECK
        elif not self.board.has_legal_moves(opponent):
            print(f"\n  *** STALEMATE! Game is a draw. ***")
            self.status = GameStatus.STALEMATE
            return True
        else:
            self.status = GameStatus.ACTIVE

        self.switch_turn()
        return True

    def is_check(self) -> bool:
        """Check if current player is in check."""
        return self.board.is_in_check(self.current_turn)

    def is_checkmate(self) -> bool:
        """Check if current player is in checkmate."""
        return (self.board.is_in_check(self.current_turn)
                and not self.board.has_legal_moves(self.current_turn))
