"""Scoring engine that processes each ball and updates all statistics."""

from typing import Optional

from enums import BallType, WicketType, InningsStatus
from player import Player
from ball import Ball
from innings import Innings
from match import Match


class ScoringEngine:
    """Processes each delivery and updates match state accordingly.

    Handles runs, wickets, extras, strike rotation, over management,
    and innings transitions.

    Attributes:
        match: The match being scored.
    """

    def __init__(self, match: Match) -> None:
        """Initialize the ScoringEngine.

        Args:
            match: The match to score.
        """
        self.match = match

    def process_ball(
        self,
        ball_type: BallType,
        runs: int,
        is_wicket: bool = False,
        wicket_type: Optional[WicketType] = None,
        fielder: Optional[str] = None,
    ) -> str:
        """Process a single delivery and update all statistics.

        Args:
            ball_type: Type of delivery.
            runs: Runs scored on this ball.
            is_wicket: Whether a wicket fell.
            wicket_type: Type of dismissal.
            fielder: Fielder involved in dismissal.

        Returns:
            Description of what happened on the ball.

        Raises:
            ValueError: If no active innings or invalid state.
        """
        innings = self.match.current_innings
        if innings is None or innings.status != InningsStatus.IN_PROGRESS:
            raise ValueError("No active innings to score.")
        if innings.current_bowler is None:
            raise ValueError("No bowler set. Call set_bowler first.")
        if innings.striker is None:
            raise ValueError("No striker at crease.")

        bowler = innings.current_bowler
        striker = innings.striker

        # Create ball object
        ball = Ball(
            ball_type=ball_type,
            runs_scored=runs,
            bowler=bowler.player,
            batsman=striker.player,
            is_wicket=is_wicket,
            wicket_type=wicket_type,
            fielder=fielder,
        )
        description = str(ball)

        # Add ball to current over
        if innings.current_over:
            innings.current_over.add_ball(ball)

        # Handle by ball type
        if ball_type == BallType.WIDE:
            innings.extras["wide"] += 1 + runs
            innings.total_runs += 1 + runs
            bowler.add_extra_runs(1 + runs)
            # Wide: no legal ball, no runs to batsman, no strike rotation
            self._check_innings_end(innings)
            return description

        if ball_type == BallType.NO_BALL:
            innings.extras["no_ball"] += 1
            innings.total_runs += 1 + runs
            bowler.add_extra_runs(1)
            if runs > 0:
                striker.add_runs(runs)
                striker.face_ball()
                if runs % 2 == 1:
                    innings._rotate_strike()
            else:
                striker.face_ball()
            self._check_innings_end(innings)
            return description

        # Legal delivery (NORMAL, BYE, LEG_BYE)
        if ball_type in (BallType.BYE, BallType.LEG_BYE):
            key = "bye" if ball_type == BallType.BYE else "leg_bye"
            innings.extras[key] += runs
            innings.total_runs += runs
            striker.face_ball()
            bowler.add_legal_ball(0, is_wicket)
        else:
            # Normal ball
            innings.total_runs += runs
            striker.face_ball()
            if not is_wicket:
                striker.add_runs(runs)
            bowler.add_legal_ball(runs, is_wicket)

        # Handle wicket
        if is_wicket and wicket_type:
            innings.wickets += 1
            striker.dismiss(wicket_type, bowler.player.name, fielder)
            # Bring in next batsman
            next_bat = innings._bring_next_batsman()
            if next_bat:
                innings.striker = next_bat
            else:
                innings.striker = None
            self._check_innings_end(innings)
            return description

        # Strike rotation on odd runs (for BYE/LEG_BYE too)
        if runs % 2 == 1:
            innings._rotate_strike()

        # Check if over is complete
        if innings.current_over and innings.current_over.is_complete:
            # End of over: rotate strike
            innings._rotate_strike()

        self._check_innings_end(innings)
        return description

    def _check_innings_end(self, innings: Innings) -> None:
        """Check if the innings should end and handle transition."""
        if innings.is_innings_over():
            innings.status = InningsStatus.COMPLETED

    def change_bowler(self, bowler: Player) -> None:
        """Change the current bowler (start new over).

        Args:
            bowler: The new bowler.
        """
        innings = self.match.current_innings
        if innings is None:
            raise ValueError("No active innings.")
        innings.set_bowler(bowler)
