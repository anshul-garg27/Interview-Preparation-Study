"""Abstract GUIFactory interface."""

from abc import ABC, abstractmethod
from button import Button
from checkbox import Checkbox


class GUIFactory(ABC):
    """Abstract factory for creating UI component families."""

    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
