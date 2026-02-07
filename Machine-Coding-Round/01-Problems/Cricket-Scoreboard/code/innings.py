"""Innings class tracking the full batting innings of a team."""

from typing import List, Dict, Optional

from enums import InningsStatus, BallType, WicketType
from player import Player
from team import Team
from batsman_stats import BatsmanStats
from bowler_stats import BowlerStats
from over import Over
from ball import Ball


class Innings:
    """Represents a single innings in a cricket match.

    Manages batting order, bowling, overs, and all statistics.

    Attributes:
        batting_team: The team batting.
        bowling_team: The team bowling.
        max_overs: Maximum overs in the innings.
        status: Current status of the innings.
    """

    def __init__(
        self,
        batting_team: Team,
        bowling_team: Team,
        max_overs: int,
        target: Optional[int] = None,
    ) -> None:
        """Initialize an Innings.

        Args:
            batting_team: The team batting.
            bowling_team: The team bowling.
            max_overs: Max overs for the innings.
            target: Target score to chase (None for 1st innings).
        """
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.max_overs = max_overs
        self.target = target
        self.status: InningsStatus = InningsStatus.NOT_STARTED

        self.total_runs: int = 0
        self.wickets: int = 0
        self.overs: List[Over] = []
        self.extras: Dict[str, int] = {"wide": 0, "no_ball": 0, "bye": 0, "leg_bye": 0}

        # Batting card
        self._batting_card: Dict[str, BatsmanStats] = {}
        self._batting_order: List[BatsmanStats] = []
        self._next_batsman_idx: int = 2  # first 2 are opener
        self.striker: Optional[BatsmanStats] = None
        self.non_striker: Optional[BatsmanStats] = None

        # Bowling card
        self._bowling_card: Dict[str, BowlerStats] = {}
        self.current_bowler: Optional[BowlerStats] = None
        self.current_over: Optional[Over] = None

    def start(self) -> None:
        """Start the innings with the first two batsmen."""
        self.status = InningsStatus.IN_PROGRESS
        players = self.batting_team.players
        self.striker = self._get_or_create_batsman(players[0])
        self.non_striker = self._get_or_create_batsman(players[1])

    def set_bowler(self, bowler: Player) -> None:
        """Set the current bowler and start a new over.

        Args:
            bowler: The bowler to bowl.
        """
        if bowler.name not in self._bowling_card:
            self._bowling_card[bowler.name] = BowlerStats(bowler)
        self.current_bowler = self._bowling_card[bowler.name]
        self.current_over = Over(len(self.overs), bowler)
        self.overs.append(self.current_over)

    def _get_or_create_batsman(self, player: Player) -> BatsmanStats:
        """Get existing or create new batsman stats."""
        if player.name not in self._batting_card:
            stats = BatsmanStats(player)
            self._batting_card[player.name] = stats
            self._batting_order.append(stats)
        return self._batting_card[player.name]

    def _rotate_strike(self) -> None:
        """Swap striker and non-striker."""
        self.striker, self.non_striker = self.non_striker, self.striker

    def _bring_next_batsman(self) -> Optional[BatsmanStats]:
        """Bring the next batsman in the order."""
        if self._next_batsman_idx >= len(self.batting_team.players):
            return None
        player = self.batting_team.players[self._next_batsman_idx]
        self._next_batsman_idx += 1
        return self._get_or_create_batsman(player)

    @property
    def overs_display(self) -> str:
        """Display current overs bowled."""
        completed = sum(1 for o in self.overs if o.is_complete)
        current_balls = 0
        if self.current_over and not self.current_over.is_complete:
            current_balls = self.current_over.legal_balls
        if current_balls == 0:
            return f"{completed}.0"
        return f"{completed}.{current_balls}"

    @property
    def completed_overs(self) -> int:
        """Number of fully completed overs."""
        return sum(1 for o in self.overs if o.is_complete)

    @property
    def run_rate(self) -> float:
        """Current run rate."""
        total_overs = self.completed_overs
        if self.current_over and not self.current_over.is_complete:
            total_overs += self.current_over.legal_balls / 6.0
        if total_overs == 0:
            return 0.0
        return round(self.total_runs / total_overs, 2)

    @property
    def batting_card(self) -> List[BatsmanStats]:
        """Return batting card in batting order."""
        return list(self._batting_order)

    @property
    def bowling_card(self) -> List[BowlerStats]:
        """Return bowling card."""
        return list(self._bowling_card.values())

    @property
    def extras_total(self) -> int:
        """Total extras."""
        return sum(self.extras.values())

    def is_innings_over(self) -> bool:
        """Check if the innings should end."""
        if self.wickets >= len(self.batting_team.players) - 1:
            return True
        if self.completed_overs >= self.max_overs:
            return True
        if self.target and self.total_runs >= self.target:
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.batting_team.name}: {self.total_runs}/{self.wickets} "
            f"({self.overs_display} ov)"
        )
