"""
FCFS (First Come First Serve) Scheduler for the Elevator System.
Assigns requests to the least busy elevator.
"""

from enums import Direction
from scheduler import Scheduler


class FCFSScheduler(Scheduler):
    """First Come First Serve - assign to the elevator with fewest pending requests."""

    def select_elevator(self, elevators: list, request_floor: int,
                        direction: Direction) -> object:
        return min(elevators, key=lambda e: len(e.pending_requests))
