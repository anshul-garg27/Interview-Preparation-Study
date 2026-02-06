"""Multilevel Inheritance - Grandparent -> Parent -> Child chain."""


class Animal:
    def __init__(self, name: str):
        self.name = name

    def breathe(self) -> str:
        return f"{self.name} is breathing"

    def info(self) -> str:
        return f"Animal: {self.name}"


class Mammal(Animal):
    def __init__(self, name: str, warm_blooded: bool = True):
        super().__init__(name)
        self.warm_blooded = warm_blooded

    def feed_young(self) -> str:
        return f"{self.name} feeds milk to young"

    def info(self) -> str:
        return f"Mammal: {self.name} (warm-blooded={self.warm_blooded})"


class Dog(Mammal):
    def __init__(self, name: str, breed: str):
        super().__init__(name, warm_blooded=True)
        self.breed = breed

    def bark(self) -> str:
        return f"{self.name} says: Woof!"

    def info(self) -> str:
        return f"Dog: {self.name} ({self.breed})"


if __name__ == "__main__":
    print("=== Multilevel Inheritance ===\n")
    print("Chain: Animal -> Mammal -> Dog\n")

    dog = Dog("Rex", "German Shepherd")

    # Methods from all levels
    print(dog.breathe())       # From Animal
    print(dog.feed_young())    # From Mammal
    print(dog.bark())          # From Dog
    print(dog.info())          # Overridden at each level

    # MRO (Method Resolution Order)
    print(f"\nMRO: {[c.__name__ for c in Dog.__mro__]}")
    # Output: ['Dog', 'Mammal', 'Animal', 'object']

    # isinstance checks through the chain
    print(f"\nDog is Mammal? {isinstance(dog, Mammal)}")
    print(f"Dog is Animal? {isinstance(dog, Animal)}")
