"""
Building class for the Elevator System.
Represents a building with a number of floors and an elevator system.
"""

from elevator_controller import ElevatorController
from scheduler import Scheduler
from fcfs_scheduler import FCFSScheduler


class Building:
    """A building containing floors and an elevator system."""

    def __init__(self, name: str, num_floors: int, num_elevators: int,
                 strategy: Scheduler | None = None) -> None:
        self._name = name
        self._num_floors = num_floors
        self._controller = ElevatorController(
            num_elevators=num_elevators,
            num_floors=num_floors,
            strategy=strategy or FCFSScheduler(),
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def controller(self) -> ElevatorController:
        return self._controller

    def __repr__(self) -> str:
        return (f"Building('{self._name}', floors={self._num_floors}, "
                f"elevators={len(self._controller.elevators)})")
