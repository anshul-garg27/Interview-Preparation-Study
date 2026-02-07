"""Game class representing a full 10-frame bowling game for one player."""

from typing import List, Optional

from enums import GameStatus
from player import Player
from frame import Frame


class Game:
    """Represents a complete 10-frame bowling game for a single player.

    Manages frame progression, roll processing, and score calculation
    including strike/spare bonuses.

    Attributes:
        player: The player for this game.
        frames: List of 10 frames.
        current_frame_idx: Index of the current frame (0-9).
        status: Current game status.
    """

    TOTAL_FRAMES = 10

    def __init__(self, player: Player) -> None:
        """Initialize a Game.

        Args:
            player: The player for this game.
        """
        self.player = player
        self.frames: List[Frame] = [Frame(i + 1) for i in range(self.TOTAL_FRAMES)]
        self.current_frame_idx: int = 0
        self.status: GameStatus = GameStatus.NOT_STARTED

    @property
    def current_frame(self) -> Optional[Frame]:
        """Get the current frame."""
        if self.current_frame_idx < self.TOTAL_FRAMES:
            return self.frames[self.current_frame_idx]
        return None

    @property
    def is_complete(self) -> bool:
        """Check if the game is complete (all frames done)."""
        return all(f.is_complete for f in self.frames)

    def roll(self, pins: int) -> str:
        """Record a roll for the current frame.

        Args:
            pins: Number of pins knocked down.

        Returns:
            Description of the roll result.

        Raises:
            ValueError: If game is complete or pins are invalid.
        """
        if self.is_complete:
            raise ValueError("Game is already complete.")

        if self.status == GameStatus.NOT_STARTED:
            self.status = GameStatus.IN_PROGRESS

        frame = self.frames[self.current_frame_idx]
        frame.roll(pins)

        # Determine description
        desc = f"Frame {frame.frame_number}: {self.player.name} rolls {pins}"
        if frame.is_strike:
            desc += " (Strike!)"
        elif frame.is_spare:
            desc += " (Spare!)"
        elif frame.is_complete and not frame.is_tenth_frame:
            desc += f" (Open: {frame.pins_down})"

        # Move to next frame if current is complete
        if frame.is_complete and self.current_frame_idx < self.TOTAL_FRAMES - 1:
            self.current_frame_idx += 1

        # Check if game is complete
        if self.is_complete:
            self.status = GameStatus.COMPLETED

        return desc

    def get_all_rolls(self) -> List[int]:
        """Get a flat list of all rolls in the game."""
        rolls = []
        for frame in self.frames:
            rolls.extend(frame.rolls)
        return rolls

    def _get_future_rolls(self, frame_idx: int) -> List[int]:
        """Get all rolls after a given frame index.

        Args:
            frame_idx: The frame index to get rolls after.

        Returns:
            List of roll values from subsequent frames.
        """
        rolls = []
        for i in range(frame_idx + 1, self.TOTAL_FRAMES):
            rolls.extend(self.frames[i].rolls)
        return rolls

    def get_frame_scores(self) -> List[Optional[int]]:
        """Calculate cumulative scores for each frame.

        Returns:
            List of cumulative scores (None if pending bonus).
        """
        scores: List[Optional[int]] = []
        cumulative = 0

        for i, frame in enumerate(self.frames):
            future_rolls = self._get_future_rolls(i)
            frame_score = frame.score(future_rolls)

            if frame_score == -1:
                scores.append(None)
            else:
                cumulative += frame_score
                scores.append(cumulative)

        return scores

    def get_score(self) -> int:
        """Get the current total score.

        Returns:
            Total score (counting only resolved frames).
        """
        scores = self.get_frame_scores()
        resolved = [s for s in scores if s is not None]
        return resolved[-1] if resolved else 0

    def __str__(self) -> str:
        return f"Game({self.player.name}) - Score: {self.get_score()} ({self.status.value})"
