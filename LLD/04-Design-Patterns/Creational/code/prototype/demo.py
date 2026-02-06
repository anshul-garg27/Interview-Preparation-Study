"""Demo: Prototype pattern with shapes and registry."""

from shapes import Circle, Rectangle
from registry import PrototypeRegistry


def main():
    print("=" * 50)
    print("PROTOTYPE PATTERN")
    print("=" * 50)

    # Direct cloning
    print("\n--- Direct Clone ---")
    original = Circle(5.0, "red")
    cloned = original.clone()
    cloned.color = "blue"
    print(f"Original: {original}")
    print(f"Cloned:   {cloned}")
    print(f"Independent? {original.color != cloned.color}")

    # Registry-based cloning
    print("\n--- Registry Clone ---")
    registry = PrototypeRegistry()
    registry.register("small_circle", Circle(2.0, "green"))
    registry.register("unit_rect", Rectangle(1.0, 1.0, "white"))
    registry.register("card", Rectangle(3.5, 2.5, "yellow"))

    print(f"Available: {registry.list_prototypes()}")

    c1 = registry.clone("small_circle")
    c2 = registry.clone("small_circle")
    c1.color = "purple"
    print(f"\nc1: {c1}")
    print(f"c2: {c2}")
    print(f"Independent? {c1.color != c2.color}")

    card = registry.clone("card")
    print(f"\nCard clone: {card}")


if __name__ == "__main__":
    main()
