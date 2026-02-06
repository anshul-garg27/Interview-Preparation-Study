"""Abstract Subject with attach/detach/notify."""

from abc import ABC, abstractmethod
from observer import Observer


class Subject(ABC):
    """Observable that maintains a list of observers."""

    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, symbol: str, price: float):
        for observer in self._observers:
            observer.update(symbol, price)
