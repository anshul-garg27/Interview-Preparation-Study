"""
Request class for the Elevator System.
Represents a passenger request from a source floor to a destination floor.
"""

from enums import Direction


class Request:
    """A request to travel from one floor to another."""

    _counter: int = 0

    def __init__(self, source_floor: int, destination_floor: int) -> None:
        Request._counter += 1
        self.request_id: int = Request._counter
        self.source_floor: int = source_floor
        self.destination_floor: int = destination_floor
        self.direction: Direction = (
            Direction.UP if destination_floor > source_floor else Direction.DOWN
        )

    @classmethod
    def reset_counter(cls) -> None:
        """Reset the request counter (useful between scenarios)."""
        cls._counter = 0

    def __repr__(self) -> str:
        return (f"Request#{self.request_id}(Floor {self.source_floor} -> "
                f"Floor {self.destination_floor}, {self.direction.value})")
