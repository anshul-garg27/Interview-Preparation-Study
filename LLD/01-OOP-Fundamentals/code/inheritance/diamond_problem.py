"""Diamond Problem - Multiple inheritance, MRO, and super() resolution."""


class A:
    def greet(self) -> str:
        return "Hello from A"

    def who(self) -> str:
        return "A"


class B(A):
    def greet(self) -> str:
        return "Hello from B"

    def who(self) -> str:
        return "B -> " + super().who()


class C(A):
    def greet(self) -> str:
        return "Hello from C"

    def who(self) -> str:
        return "C -> " + super().who()


class D(B, C):
    """Diamond: D inherits B and C, both inherit A.
         A
        / \\
       B   C
        \\ /
         D
    """
    def who(self) -> str:
        return "D -> " + super().who()


# Practical example: Cooperative multiple inheritance
class Loggable:
    def log(self, message: str) -> None:
        print(f"  [LOG] {self.__class__.__name__}: {message}")


class Serializable:
    def to_dict(self) -> dict:
        return {"class": self.__class__.__name__, **self.__dict__}


class User(Loggable, Serializable):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def save(self) -> None:
        self.log(f"Saving user {self.name}")
        print(f"  Serialized: {self.to_dict()}")


if __name__ == "__main__":
    print("=== Diamond Problem ===\n")

    d = D()
    # Python uses C3 linearization (MRO) to resolve
    print(f"d.greet(): {d.greet()}")  # Hello from B (B comes first in D(B,C))
    print(f"d.who():   {d.who()}")    # D -> B -> C -> A

    # MRO shows the resolution order
    print(f"\nMRO: {[c.__name__ for c in D.__mro__]}")
    # Output: ['D', 'B', 'C', 'A', 'object']

    # Key insight: super() follows MRO, not parent class
    print("\n--- Practical Multiple Inheritance ---")
    user = User("Alice", "alice@mail.com")
    user.save()
    print(f"  MRO: {[c.__name__ for c in User.__mro__]}")
