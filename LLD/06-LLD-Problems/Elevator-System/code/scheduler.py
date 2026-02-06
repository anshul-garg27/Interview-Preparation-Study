"""
Abstract Scheduler base class for the Elevator System.
Defines the interface for elevator scheduling strategies (Strategy pattern).
"""

from abc import ABC, abstractmethod

from enums import Direction


class Scheduler(ABC):
    """Abstract base for elevator scheduling algorithms."""

    @abstractmethod
    def select_elevator(self, elevators: list, request_floor: int,
                        direction: Direction) -> object:
        """Select the best elevator to handle a request.

        Args:
            elevators: List of available Elevator instances.
            request_floor: The floor the request originates from.
            direction: The desired direction of travel.

        Returns:
            The selected Elevator instance.
        """
        pass
