"""Over class representing a collection of 6 legal deliveries."""

from typing import List, Optional

from ball import Ball
from player import Player


class Over:
    """Represents a single over (6 legal deliveries) in cricket.

    Attributes:
        over_number: The over number (0-indexed).
        bowler: The bowler for this over.
        balls: List of all deliveries in this over.
    """

    def __init__(self, over_number: int, bowler: Player) -> None:
        """Initialize an Over.

        Args:
            over_number: The over number.
            bowler: The bowler for this over.
        """
        self.over_number = over_number
        self.bowler = bowler
        self.balls: List[Ball] = []

    @property
    def legal_balls(self) -> int:
        """Count of legal deliveries in this over."""
        return sum(1 for b in self.balls if b.is_legal)

    @property
    def is_complete(self) -> bool:
        """Check if this over is complete (6 legal deliveries)."""
        return self.legal_balls >= 6

    @property
    def total_runs(self) -> int:
        """Total runs scored in this over (including extras)."""
        total = 0
        for ball in self.balls:
            total += ball.runs_scored
            if ball.ball_type.value in ("wide", "no-ball"):
                total += 1  # extra run for wide/no-ball
        return total

    @property
    def is_maiden(self) -> bool:
        """Check if this is a maiden over (0 runs off bat, complete over)."""
        if not self.is_complete:
            return False
        return all(b.runs_scored == 0 for b in self.balls if b.is_legal)

    def add_ball(self, ball: Ball) -> None:
        """Add a delivery to this over.

        Args:
            ball: The ball to add.
        """
        self.balls.append(ball)

    def __str__(self) -> str:
        ball_strs = []
        for b in self.balls:
            if b.is_wicket:
                ball_strs.append("W")
            elif b.ball_type.value == "wide":
                ball_strs.append("Wd")
            elif b.ball_type.value == "no-ball":
                ball_strs.append("Nb")
            else:
                ball_strs.append(str(b.runs_scored))
        return f"Over {self.over_number + 1} ({self.bowler.name}): {' '.join(ball_strs)}"
