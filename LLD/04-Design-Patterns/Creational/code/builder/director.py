"""Director orchestrates the building process."""

from builder import HouseBuilder


class Director:
    """Knows the recipe for building different house configurations."""

    def __init__(self, builder: HouseBuilder):
        self._builder = builder

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder: HouseBuilder):
        self._builder = builder

    def build_starter_home(self):
        self._builder.build_foundation()
        self._builder.build_walls()
        self._builder.build_roof()
        self._builder.build_rooms(2)

    def build_family_home(self):
        self._builder.build_foundation()
        self._builder.build_walls()
        self._builder.build_roof()
        self._builder.build_rooms(4)

    def build_mansion(self):
        self._builder.build_foundation()
        self._builder.build_walls()
        self._builder.build_roof()
        self._builder.build_rooms(8)
