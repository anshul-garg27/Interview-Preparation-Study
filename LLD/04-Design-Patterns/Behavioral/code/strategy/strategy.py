"""Abstract PaymentStrategy interface."""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """All payment methods must implement this."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass
