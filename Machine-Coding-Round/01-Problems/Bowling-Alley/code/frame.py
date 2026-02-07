"""Frame class representing a single frame in a bowling game."""

from typing import List

from enums import FrameType


class Frame:
    """Represents a single frame (1 of 10) in a bowling game.

    Handles regular frames (1-9) and the special 10th frame with
    up to 3 rolls. Calculates strike/spare detection and scoring
    with bonus from future rolls.

    Attributes:
        frame_number: Frame number (1-10).
        rolls: List of pins knocked down per roll in this frame.
    """

    def __init__(self, frame_number: int) -> None:
        """Initialize a Frame.

        Args:
            frame_number: The frame number (1-10).

        Raises:
            ValueError: If frame_number is not between 1 and 10.
        """
        if not 1 <= frame_number <= 10:
            raise ValueError(f"Frame number must be 1-10, got {frame_number}.")
        self.frame_number = frame_number
        self.rolls: List[int] = []

    @property
    def is_tenth_frame(self) -> bool:
        """Check if this is the special 10th frame."""
        return self.frame_number == 10

    @property
    def is_strike(self) -> bool:
        """Check if the first roll is a strike."""
        return len(self.rolls) >= 1 and self.rolls[0] == 10

    @property
    def is_spare(self) -> bool:
        """Check if the first two rolls make a spare (not a strike)."""
        if self.is_strike:
            return False
        return len(self.rolls) >= 2 and self.rolls[0] + self.rolls[1] == 10

    @property
    def frame_type(self) -> FrameType:
        """Determine the frame type."""
        if not self.is_complete:
            return FrameType.IN_PROGRESS
        if self.is_strike:
            return FrameType.STRIKE
        if self.is_spare:
            return FrameType.SPARE
        return FrameType.OPEN

    @property
    def pins_down(self) -> int:
        """Total pins knocked down in this frame (excluding bonus)."""
        return sum(self.rolls)

    @property
    def is_complete(self) -> bool:
        """Check if this frame is complete (no more rolls allowed)."""
        if self.is_tenth_frame:
            if len(self.rolls) >= 3:
                return True
            if len(self.rolls) == 2:
                # Need 3rd roll only if strike or spare
                if self.rolls[0] == 10 or (self.rolls[0] + self.rolls[1] >= 10):
                    return False
                return True
            return False
        else:
            if len(self.rolls) == 0:
                return False
            if self.rolls[0] == 10:  # Strike
                return True
            return len(self.rolls) >= 2

    def roll(self, pins: int) -> None:
        """Record a roll in this frame.

        Args:
            pins: Number of pins knocked down.

        Raises:
            ValueError: If the frame is complete or pins are invalid.
        """
        if self.is_complete:
            raise ValueError(f"Frame {self.frame_number} is already complete.")
        if pins < 0 or pins > 10:
            raise ValueError(f"Pins must be between 0 and 10, got {pins}.")

        if self.is_tenth_frame:
            self._validate_tenth_frame_roll(pins)
        else:
            if len(self.rolls) == 1 and self.rolls[0] + pins > 10:
                raise ValueError(
                    f"Cannot knock down {pins} pins; only "
                    f"{10 - self.rolls[0]} remaining."
                )

        self.rolls.append(pins)

    def _validate_tenth_frame_roll(self, pins: int) -> None:
        """Validate a roll for the 10th frame.

        Args:
            pins: Pins knocked down.

        Raises:
            ValueError: If the roll is invalid for 10th frame state.
        """
        if len(self.rolls) == 0:
            return  # First roll: 0-10 always valid
        if len(self.rolls) == 1:
            if self.rolls[0] == 10:
                return  # After strike, pins reset: 0-10 valid
            if self.rolls[0] + pins > 10:
                raise ValueError(
                    f"Cannot knock down {pins} pins; only "
                    f"{10 - self.rolls[0]} remaining."
                )
        if len(self.rolls) == 2:
            # After two rolls in 10th frame
            if self.rolls[0] == 10 and self.rolls[1] == 10:
                return  # Two strikes, pins reset: 0-10 valid
            if self.rolls[0] == 10:
                # Strike then non-strike: check remaining
                if self.rolls[1] + pins > 10:
                    raise ValueError(
                        f"Cannot knock down {pins} pins; only "
                        f"{10 - self.rolls[1]} remaining."
                    )
            # Spare: pins reset, 0-10 valid
            return

    def score(self, next_rolls: List[int]) -> int:
        """Calculate the score for this frame including bonuses.

        For frames 1-9:
        - Strike: 10 + next 2 rolls
        - Spare: 10 + next 1 roll
        - Open: sum of rolls

        For frame 10:
        - Sum of all rolls (no bonus from future frames)

        Args:
            next_rolls: List of rolls from subsequent frames.

        Returns:
            Score for this frame, or -1 if bonuses are pending.
        """
        if not self.is_complete:
            return -1

        if self.is_tenth_frame:
            return sum(self.rolls)

        if self.is_strike:
            if len(next_rolls) < 2:
                return -1  # Bonus pending
            return 10 + next_rolls[0] + next_rolls[1]

        if self.is_spare:
            if len(next_rolls) < 1:
                return -1  # Bonus pending
            return 10 + next_rolls[0]

        return self.rolls[0] + self.rolls[1]

    def display_rolls(self) -> str:
        """Return formatted string of rolls for scorecard display."""
        if self.is_tenth_frame:
            return self._display_tenth_frame()
        return self._display_regular_frame()

    def _display_regular_frame(self) -> str:
        """Format rolls for frames 1-9."""
        if len(self.rolls) == 0:
            return "   "
        if self.is_strike:
            return " X "
        if len(self.rolls) == 1:
            r1 = str(self.rolls[0]) if self.rolls[0] > 0 else "-"
            return f" {r1}  "
        r1 = str(self.rolls[0]) if self.rolls[0] > 0 else "-"
        if self.is_spare:
            return f"{r1} /"
        r2 = str(self.rolls[1]) if self.rolls[1] > 0 else "-"
        return f"{r1} {r2}"

    def _display_tenth_frame(self) -> str:
        """Format rolls for the 10th frame."""
        parts = []
        for i, r in enumerate(self.rolls):
            if r == 10:
                # Strike: show X
                if i == 0:
                    parts.append("X")
                elif i == 1:
                    if self.rolls[0] == 10:
                        parts.append("X")
                    else:
                        parts.append("/")  # spare in 10th
                elif i == 2:
                    if len(self.rolls) >= 2 and self.rolls[1] == 10:
                        parts.append("X")
                    elif i >= 1 and self.rolls[0] != 10 and self.rolls[0] + self.rolls[1] == 10:
                        parts.append("X")  # after spare
                    else:
                        parts.append("X")
            elif i == 1 and self.rolls[0] != 10 and self.rolls[0] + r == 10:
                parts.append("/")
            elif i == 2 and len(self.rolls) >= 2:
                if self.rolls[1] != 10 and self.rolls[0] == 10 and self.rolls[1] + r == 10:
                    parts.append("/")
                else:
                    parts.append(str(r) if r > 0 else "-")
            else:
                parts.append(str(r) if r > 0 else "-")

        while len(parts) < 3:
            parts.append(" ")
        return " ".join(parts[:3])

    def __str__(self) -> str:
        return f"Frame {self.frame_number}: {self.rolls} ({self.frame_type.value})"
