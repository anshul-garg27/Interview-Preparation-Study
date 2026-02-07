"""Ball class representing a single delivery in cricket."""

from typing import Optional

from enums import BallType, WicketType
from player import Player


class Ball:
    """Represents a single delivery (ball) in a cricket match.

    Attributes:
        ball_type: Type of delivery (normal, wide, no-ball, etc.).
        runs_scored: Runs scored on this delivery.
        is_wicket: Whether a wicket fell on this delivery.
        wicket_type: Type of dismissal (if wicket fell).
        bowler: The bowler who delivered.
        batsman: The batsman who faced.
        fielder: The fielder involved in dismissal (if applicable).
    """

    def __init__(
        self,
        ball_type: BallType,
        runs_scored: int,
        bowler: Player,
        batsman: Player,
        is_wicket: bool = False,
        wicket_type: Optional[WicketType] = None,
        fielder: Optional[str] = None,
    ) -> None:
        """Initialize a Ball.

        Args:
            ball_type: Type of delivery.
            runs_scored: Runs scored.
            bowler: The bowler.
            batsman: The batsman facing.
            is_wicket: Whether wicket fell.
            wicket_type: Type of dismissal.
            fielder: Fielder involved in dismissal.

        Raises:
            ValueError: If runs_scored is negative.
        """
        if runs_scored < 0:
            raise ValueError("Runs scored cannot be negative.")
        self.ball_type = ball_type
        self.runs_scored = runs_scored
        self.bowler = bowler
        self.batsman = batsman
        self.is_wicket = is_wicket
        self.wicket_type = wicket_type
        self.fielder = fielder

    @property
    def is_legal(self) -> bool:
        """Check if this is a legal delivery (counts towards over)."""
        return self.ball_type in (BallType.NORMAL, BallType.BYE, BallType.LEG_BYE)

    @property
    def is_extra(self) -> bool:
        """Check if this delivery resulted in extras."""
        return self.ball_type != BallType.NORMAL

    @property
    def is_boundary(self) -> bool:
        """Check if this was a boundary (4 or 6)."""
        return self.runs_scored in (4, 6) and self.ball_type == BallType.NORMAL

    def __str__(self) -> str:
        desc = f"{self.bowler.name} to {self.batsman.name}: "
        if self.is_wicket:
            desc += f"WICKET! ({self.wicket_type.value})"
        elif self.ball_type == BallType.WIDE:
            desc += f"WIDE (+{self.runs_scored})"
        elif self.ball_type == BallType.NO_BALL:
            desc += f"NO BALL (+{self.runs_scored})"
        elif self.runs_scored == 0:
            desc += "dot ball"
        elif self.runs_scored == 4:
            desc += "FOUR!"
        elif self.runs_scored == 6:
            desc += "SIX!"
        else:
            desc += f"{self.runs_scored} run{'s' if self.runs_scored > 1 else ''}"
        return desc
