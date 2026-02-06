"""Basic Classes and Objects - Creating classes, attributes, and methods."""


class Person:
    """A simple Person class demonstrating class fundamentals."""

    # Class attribute (shared by all instances)
    species = "Homo sapiens"

    def __init__(self, name: str, age: int):
        # Instance attributes (unique to each object)
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

    def is_adult(self) -> bool:
        return self.age >= 18


class Dog:
    """Another simple class to show multiple objects."""

    def __init__(self, name: str, breed: str):
        self.name = name
        self.breed = breed

    def bark(self) -> str:
        return f"{self.name} says: Woof!"


if __name__ == "__main__":
    print("=== Basic Classes and Objects ===\n")

    # Creating objects (instances)
    alice = Person("Alice", 30)
    bob = Person("Bob", 17)

    print(alice.greet())           # Hi, I'm Alice and I'm 30 years old.
    print(bob.greet())             # Hi, I'm Bob and I'm 17 years old.

    print(f"Alice is adult: {alice.is_adult()}")  # True
    print(f"Bob is adult: {bob.is_adult()}")      # False

    # Class attribute accessed via class or instance
    print(f"Species: {Person.species}")
    print(f"Same via instance: {alice.species}")

    # Each object has its own identity
    print(f"\nalice is bob: {alice is bob}")     # False
    print(f"type(alice): {type(alice)}")          # <class '__main__.Person'>

    # Dog examples
    rex = Dog("Rex", "German Shepherd")
    print(f"\n{rex.bark()}")
    print(f"Breed: {rex.breed}")
