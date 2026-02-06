"""
ElevatorController for the Elevator System.
Manages multiple elevators, dispatches requests, and runs simulation.
"""

from elevator import Elevator
from request import Request
from scheduler import Scheduler
from fcfs_scheduler import FCFSScheduler


class ElevatorController:
    """Controller managing a bank of elevators with a scheduling strategy."""

    def __init__(self, num_elevators: int, num_floors: int,
                 strategy: Scheduler | None = None) -> None:
        self._num_floors = num_floors
        self._strategy = strategy or FCFSScheduler()
        self._elevators = [Elevator(i + 1, 0, num_floors) for i in range(num_elevators)]

    @property
    def elevators(self) -> list[Elevator]:
        return self._elevators

    def set_strategy(self, strategy: Scheduler) -> None:
        """Swap scheduling strategy at runtime."""
        self._strategy = strategy

    def request_elevator(self, request: Request) -> None:
        """Dispatch an elevator for the given request."""
        print(f"\n  >> {request}")
        elevator = self._strategy.select_elevator(
            self._elevators, request.source_floor, request.direction
        )
        elevator.add_request(request.source_floor)
        elevator.add_request(request.destination_floor)
        print(f"  >> Assigned to Elevator-{elevator.elevator_id}")

    def run_step(self) -> None:
        """Run one simulation step for all elevators."""
        for e in self._elevators:
            if not e.is_idle():
                e.step()

    def all_idle(self) -> bool:
        return all(e.is_idle() for e in self._elevators)

    def simulate(self, max_steps: int = 100) -> None:
        """Run until all elevators are idle or max_steps reached."""
        step = 0
        while not self.all_idle() and step < max_steps:
            step += 1
            self.run_step()
        print(f"\n  Simulation completed in {step} steps.")

    def display_status(self) -> None:
        """Print current status of all elevators."""
        print(f"\n  {'_'*50}")
        print(f"  Elevator System Status:")
        for e in self._elevators:
            print(f"    {e.status()}")
        print(f"  {'_'*50}")
