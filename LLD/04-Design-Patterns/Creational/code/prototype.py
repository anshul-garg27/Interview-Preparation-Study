"""
Prototype Pattern - Creates new objects by cloning existing ones.
Useful when object creation is expensive or complex.

Examples:
1. Shape prototypes: Circle, Rectangle with clone()
2. Deep copy vs shallow copy demonstration
3. Game character prototype registry
"""
import copy
from abc import ABC, abstractmethod


# --- Shape Prototype ---
class Shape(ABC):
    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Circle(Shape):
    def __init__(self, radius, color="red", center=(0, 0)):
        self.radius = radius
        self.color = color
        self.center = list(center)  # Mutable to show deep/shallow copy

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"Circle(r={self.radius}, color={self.color}, center={self.center})"


class Rectangle(Shape):
    def __init__(self, width, height, color="blue"):
        self.width = width
        self.height = height
        self.color = color
        self.tags = []  # Mutable list

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"Rect({self.width}x{self.height}, color={self.color}, tags={self.tags})"


# --- Deep vs Shallow Copy ---
class Config:
    def __init__(self, settings: dict):
        self.settings = settings

    def shallow_clone(self):
        return copy.copy(self)

    def deep_clone(self):
        return copy.deepcopy(self)


# --- Game Character Registry ---
class GameCharacter:
    def __init__(self, name, hp, attack, defense, skills):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.skills = list(skills)

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return (f"{self.name}: HP={self.hp}, ATK={self.attack}, "
                f"DEF={self.defense}, Skills={self.skills}")


class PrototypeRegistry:
    def __init__(self):
        self._prototypes = {}

    def register(self, name, prototype):
        self._prototypes[name] = prototype

    def create(self, proto_name, **overrides):
        proto = self._prototypes[proto_name].clone()
        for key, val in overrides.items():
            setattr(proto, key, val)
        return proto


if __name__ == "__main__":
    print("=" * 60)
    print("PROTOTYPE PATTERN DEMO")
    print("=" * 60)

    # Shape cloning
    print("\n--- Shape Cloning ---")
    circle = Circle(5, "red", (10, 20))
    cloned = circle.clone()
    cloned.color = "green"
    cloned.center[0] = 99
    print(f"  Original: {circle}")
    print(f"  Clone:    {cloned}")
    print(f"  Independent? {circle.center != cloned.center}")

    # Deep vs Shallow copy
    print("\n--- Deep vs Shallow Copy ---")
    original = Config({"theme": "dark", "plugins": ["vim", "git"]})

    shallow = original.shallow_clone()
    shallow.settings["theme"] = "light"
    print(f"  Original after shallow clone mutation: {original.settings}")
    print(f"  (Shallow copy shares nested objects!)")

    original2 = Config({"theme": "dark", "plugins": ["vim", "git"]})
    deep = original2.deep_clone()
    deep.settings["theme"] = "light"
    print(f"  Original after deep clone mutation: {original2.settings}")
    print(f"  (Deep copy is fully independent)")

    # Game Character Registry
    print("\n--- Game Character Registry ---")
    registry = PrototypeRegistry()
    registry.register("warrior", GameCharacter("Warrior", 100, 15, 10, ["slash", "block"]))
    registry.register("mage", GameCharacter("Mage", 60, 25, 5, ["fireball", "heal"]))
    registry.register("archer", GameCharacter("Archer", 80, 20, 7, ["arrow", "dodge"]))

    hero1 = registry.create("warrior", name="Aragorn", hp=120)
    hero2 = registry.create("mage", name="Gandalf")
    hero3 = registry.create("warrior", name="Boromir")
    hero3.skills.append("charge")

    print(f"  {hero1}")
    print(f"  {hero2}")
    print(f"  {hero3}")
    print(f"  Base warrior unchanged? {'charge' not in registry._prototypes['warrior'].skills}")
