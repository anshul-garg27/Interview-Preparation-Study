"""Concrete house builders."""

from builder import HouseBuilder


class SimpleHouseBuilder(HouseBuilder):
    def build_foundation(self):
        self._house.foundation = "concrete slab"

    def build_walls(self):
        self._house.walls = "wood frame"

    def build_roof(self):
        self._house.roof = "asphalt shingles"

    def build_rooms(self, count: int):
        self._house.rooms = count


class LuxuryHouseBuilder(HouseBuilder):
    def build_foundation(self):
        self._house.foundation = "reinforced concrete"

    def build_walls(self):
        self._house.walls = "brick and stone"

    def build_roof(self):
        self._house.roof = "clay tiles"

    def build_rooms(self, count: int):
        self._house.rooms = count
        self._house.garage = True
        self._house.pool = True
        self._house.garden = True
