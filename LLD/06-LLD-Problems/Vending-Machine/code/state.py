"""Abstract state interface for the Vending Machine (State Pattern)."""

from abc import ABC, abstractmethod


class VendingMachineState(ABC):
    """Abstract state defining all vending machine actions."""

    @abstractmethod
    def insert_coin(self, machine: "VendingMachine", value: int) -> None:
        """Handle coin/note insertion."""
        pass

    @abstractmethod
    def select_product(self, machine: "VendingMachine", code: str) -> None:
        """Handle product selection."""
        pass

    @abstractmethod
    def dispense(self, machine: "VendingMachine") -> None:
        """Handle product dispensing."""
        pass

    @abstractmethod
    def cancel(self, machine: "VendingMachine") -> None:
        """Handle transaction cancellation."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return human-readable state name."""
        pass
