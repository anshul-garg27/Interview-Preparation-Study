"""Enumerations for the Cricket Scoreboard system."""

from enum import Enum


class WicketType(Enum):
    """Types of dismissals in cricket."""
    BOWLED = "bowled"
    CAUGHT = "caught"
    RUN_OUT = "run out"
    LBW = "lbw"
    STUMPED = "stumped"


class BallType(Enum):
    """Types of deliveries in cricket."""
    NORMAL = "normal"
    WIDE = "wide"
    NO_BALL = "no-ball"
    BYE = "bye"
    LEG_BYE = "leg-bye"


class InningsStatus(Enum):
    """Status of an innings."""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class MatchResult(Enum):
    """Result of the match."""
    TEAM1_WIN = "TEAM1_WIN"
    TEAM2_WIN = "TEAM2_WIN"
    TIE = "TIE"
    IN_PROGRESS = "IN_PROGRESS"
