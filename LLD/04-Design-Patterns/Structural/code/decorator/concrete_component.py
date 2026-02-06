"""Concrete base coffees."""

from component import Coffee


class Espresso(Coffee):
    def get_description(self) -> str:
        return "Espresso"

    def get_cost(self) -> float:
        return 2.00


class Latte(Coffee):
    def get_description(self) -> str:
        return "Latte"

    def get_cost(self) -> float:
        return 3.50
