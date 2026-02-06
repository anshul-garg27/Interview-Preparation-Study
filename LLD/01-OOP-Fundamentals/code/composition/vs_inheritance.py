"""Composition vs Inheritance - Same problem, two approaches."""


# === INHERITANCE APPROACH (less flexible) ===

class InheritanceRobot:
    """Base robot with walk."""
    def walk(self) -> str:
        return "Walking"


class FlyingRobot(InheritanceRobot):
    """Robot that can also fly."""
    def fly(self) -> str:
        return "Flying"


class SwimmingRobot(InheritanceRobot):
    """Robot that can also swim."""
    def swim(self) -> str:
        return "Swimming"


# Problem: What if we need a robot that flies AND swims?
# Multiple inheritance gets messy and rigid.
class FlyingSwimmingRobot(FlyingRobot, SwimmingRobot):
    """Works but creates rigid hierarchy. What about swim+talk? fly+talk?"""
    pass


# === COMPOSITION APPROACH (flexible) ===

class WalkAbility:
    def walk(self) -> str:
        return "Walking"


class FlyAbility:
    def fly(self) -> str:
        return "Flying"


class SwimAbility:
    def swim(self) -> str:
        return "Swimming"


class TalkAbility:
    def talk(self) -> str:
        return "Talking"


class ComposedRobot:
    """Mix and match ANY abilities without changing class hierarchy."""

    def __init__(self, name: str, abilities: list):
        self.name = name
        self.abilities = {type(a).__name__: a for a in abilities}

    def perform(self, action: str) -> str:
        for ability in self.abilities.values():
            if hasattr(ability, action):
                return getattr(ability, action)()
        return f"{self.name} can't {action}"

    def describe(self) -> str:
        names = list(self.abilities.keys())
        return f"{self.name}: {', '.join(names)}"


if __name__ == "__main__":
    print("=== Composition vs Inheritance ===\n")

    print("--- Inheritance (rigid) ---")
    r1 = FlyingSwimmingRobot()
    print(f"  walk: {r1.walk()}, fly: {r1.fly()}, swim: {r1.swim()}")
    print("  Problem: Need new class for each combination!")
    print(f"  MRO: {[c.__name__ for c in FlyingSwimmingRobot.__mro__]}")

    print("\n--- Composition (flexible) ---")
    scout = ComposedRobot("Scout", [WalkAbility(), FlyAbility()])
    diver = ComposedRobot("Diver", [WalkAbility(), SwimAbility()])
    ambassador = ComposedRobot("Ambassador", [WalkAbility(), TalkAbility(), FlyAbility()])

    for robot in [scout, diver, ambassador]:
        print(f"  {robot.describe()}")
        print(f"    fly:  {robot.perform('fly')}")
        print(f"    swim: {robot.perform('swim')}")
        print(f"    talk: {robot.perform('talk')}")
        print()

    print("Winner: Composition. Add new abilities without changing existing code.")
