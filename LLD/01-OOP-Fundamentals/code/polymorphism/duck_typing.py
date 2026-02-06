"""Duck Typing - 'If it walks like a duck and quacks like a duck...'"""


class Duck:
    def walk(self) -> str:
        return "Duck walking"

    def quack(self) -> str:
        return "Quack!"


class Person:
    def walk(self) -> str:
        return "Person walking"

    def quack(self) -> str:
        return "I'm quacking like a duck!"


class Robot:
    def walk(self) -> str:
        return "Robot walking mechanically"

    def quack(self) -> str:
        return "QUACK (synthesized)"


class Cat:
    """Cat can walk but cannot quack - will fail duck test."""
    def walk(self) -> str:
        return "Cat walking"


def duck_test(thing) -> None:
    """Doesn't care about type - only cares about behavior."""
    print(f"  {thing.__class__.__name__}:")
    print(f"    walk:  {thing.walk()}")
    print(f"    quack: {thing.quack()}")


# Practical example: len() works with any object that has __len__
class Playlist:
    def __init__(self, songs: list[str]):
        self.songs = songs

    def __len__(self) -> int:
        return len(self.songs)

    def __iter__(self):
        return iter(self.songs)


if __name__ == "__main__":
    print("=== Duck Typing ===\n")
    print("'If it walks like a duck and quacks like a duck, it IS a duck.'\n")

    # All three pass the duck test (no inheritance needed!)
    for thing in [Duck(), Person(), Robot()]:
        duck_test(thing)
        print()

    # Cat fails - no quack method
    print("--- Cat fails duck test ---")
    try:
        duck_test(Cat())
    except AttributeError as e:
        print(f"  Cat failed: {e}")

    # Built-in duck typing: len() works with any __len__
    print("\n--- Built-in Duck Typing ---")
    playlist = Playlist(["Song A", "Song B", "Song C"])
    print(f"  len(list):     {len([1, 2, 3])}")
    print(f"  len(str):      {len('hello')}")
    print(f"  len(playlist): {len(playlist)}")
