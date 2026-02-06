"""Coffee decorators that add toppings."""

from component import Coffee


class CoffeeDecorator(Coffee):
    """Base decorator wrapping a Coffee."""

    def __init__(self, coffee: Coffee):
        self._coffee = coffee


class Milk(CoffeeDecorator):
    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Milk"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.50


class Sugar(CoffeeDecorator):
    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Sugar"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.25


class WhippedCream(CoffeeDecorator):
    def get_description(self) -> str:
        return f"{self._coffee.get_description()} + Whipped Cream"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.75
