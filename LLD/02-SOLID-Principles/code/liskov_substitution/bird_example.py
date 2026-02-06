"""LSP - Classic Bird/Penguin example: violation and fix."""

from abc import ABC, abstractmethod


# === VIOLATION ===

class BadBird:
    def fly(self) -> str:
        return "Flying high!"


class BadPenguin(BadBird):
    def fly(self) -> str:
        raise NotImplementedError("Penguins can't fly!")  # Breaks contract!


# === FIX: Separate flying from non-flying birds ===

class Bird(ABC):
    """All birds can do these things."""

    @abstractmethod
    def eat(self) -> str:
        pass

    @abstractmethod
    def move(self) -> str:
        pass


class FlyingBird(Bird):
    """Only flying birds have fly()."""

    def move(self) -> str:
        return self.fly()

    @abstractmethod
    def fly(self) -> str:
        pass


class NonFlyingBird(Bird):
    """Birds that walk/swim instead of fly."""

    def move(self) -> str:
        return self.walk()

    @abstractmethod
    def walk(self) -> str:
        pass


class Eagle(FlyingBird):
    def eat(self) -> str:
        return "Eagle hunts fish"

    def fly(self) -> str:
        return "Eagle soars through the sky"


class Penguin(NonFlyingBird):
    def eat(self) -> str:
        return "Penguin catches fish underwater"

    def walk(self) -> str:
        return "Penguin waddles on ice"


def observe_birds(birds: list[Bird]) -> None:
    """Works with ANY bird - no exceptions thrown."""
    for bird in birds:
        print(f"  {bird.__class__.__name__}: {bird.move()} | {bird.eat()}")


if __name__ == "__main__":
    print("=== Bird/Penguin LSP Example ===\n")

    # Violation
    print("BAD DESIGN:")
    bad_penguin = BadPenguin()
    try:
        bad_penguin.fly()
    except NotImplementedError as e:
        print(f"  BadPenguin.fly() -> {e}\n")

    # Fixed
    print("GOOD DESIGN:")
    birds: list[Bird] = [Eagle(), Penguin()]
    observe_birds(birds)

    print("\nKey: Penguin was never asked to fly. It moves by walking.")
