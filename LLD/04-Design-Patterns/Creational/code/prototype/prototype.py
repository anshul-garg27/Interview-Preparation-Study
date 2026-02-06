"""Abstract Prototype interface."""

from abc import ABC, abstractmethod
import copy


class Prototype(ABC):
    """Objects that support cloning themselves."""

    @abstractmethod
    def clone(self):
        """Return a deep copy of this object."""
        pass

    def deep_clone(self):
        """Default deep clone using copy module."""
        return copy.deepcopy(self)
