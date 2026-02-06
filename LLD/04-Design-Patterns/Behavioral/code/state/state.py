"""Abstract VendingMachineState interface."""

from abc import ABC, abstractmethod


class VendingMachineState(ABC):
    """Each state handles the same actions differently."""

    @abstractmethod
    def insert_money(self, machine, amount: float) -> str:
        pass

    @abstractmethod
    def select_item(self, machine, item: str) -> str:
        pass

    @abstractmethod
    def dispense(self, machine) -> str:
        pass
