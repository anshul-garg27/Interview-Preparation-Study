"""
SCAN (Elevator Algorithm) Scheduler for the Elevator System.
Assigns requests to the nearest elevator moving in the same direction.
"""

from enums import Direction
from scheduler import Scheduler


class SCANScheduler(Scheduler):
    """SCAN / Elevator Algorithm - prefer nearest elevator going same direction."""

    def select_elevator(self, elevators: list, request_floor: int,
                        direction: Direction) -> object:
        best = None
        best_dist = float("inf")
        for e in elevators:
            dist = abs(e.current_floor - request_floor)
            # Prefer elevators going in the same direction or idle
            if e.direction == direction or e.direction == Direction.IDLE:
                if dist < best_dist:
                    best_dist = dist
                    best = e
        # Fallback to nearest elevator regardless of direction
        if best is None:
            best = min(elevators, key=lambda e: abs(e.current_floor - request_floor))
        return best
