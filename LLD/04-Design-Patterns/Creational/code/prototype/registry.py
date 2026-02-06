"""Prototype Registry for managing pre-configured prototypes."""

from prototype import Prototype


class PrototypeRegistry:
    """Stores pre-configured prototypes and clones them on demand."""

    def __init__(self):
        self._prototypes = {}

    def register(self, name: str, prototype: Prototype):
        self._prototypes[name] = prototype

    def unregister(self, name: str):
        del self._prototypes[name]

    def clone(self, name: str) -> Prototype:
        if name not in self._prototypes:
            raise KeyError(f"Prototype '{name}' not found")
        return self._prototypes[name].clone()

    def list_prototypes(self) -> list:
        return list(self._prototypes.keys())
