"""Single Inheritance - One parent, one child. Method overriding basics."""


class Animal:
    def __init__(self, name: str, sound: str = "..."):
        self.name = name
        self.sound = sound

    def speak(self) -> str:
        return f"{self.name} says: {self.sound}"

    def describe(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name, sound="Woof!")
        self.breed = breed

    def fetch(self) -> str:
        return f"{self.name} fetches the ball!"

    # Override parent method
    def describe(self) -> str:
        return f"Dog(name={self.name}, breed={self.breed})"


class Cat(Animal):
    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name, sound="Meow!")
        self.indoor = indoor

    def purr(self) -> str:
        return f"{self.name} purrs..."

    def describe(self) -> str:
        loc = "indoor" if self.indoor else "outdoor"
        return f"Cat(name={self.name}, {loc})"


if __name__ == "__main__":
    print("=== Single Inheritance ===\n")

    animals: list[Animal] = [
        Dog("Rex", "German Shepherd"),
        Cat("Whiskers", indoor=True),
        Animal("Unknown", "???"),
    ]

    for a in animals:
        print(f"{a.describe()} -> {a.speak()}")

    # Child-specific methods
    dog = Dog("Buddy", "Labrador")
    print(f"\n{dog.fetch()}")

    cat = Cat("Luna")
    print(cat.purr())

    # isinstance checks
    print(f"\nDog is Animal? {isinstance(dog, Animal)}")
    print(f"Cat is Animal? {isinstance(cat, Animal)}")
    print(f"Dog is Cat?    {isinstance(dog, Cat)}")
