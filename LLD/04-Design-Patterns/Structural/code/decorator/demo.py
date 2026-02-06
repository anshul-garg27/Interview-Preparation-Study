"""Demo: Decorator pattern - build complex coffees."""

from concrete_component import Espresso, Latte
from decorators import Milk, Sugar, WhippedCream


def main():
    print("=" * 50)
    print("DECORATOR PATTERN")
    print("=" * 50)

    # Plain espresso
    print("\n--- Plain Coffee ---")
    espresso = Espresso()
    print(f"  {espresso}")

    # Decorated espresso
    print("\n--- Espresso + Milk + Sugar ---")
    fancy = Sugar(Milk(Espresso()))
    print(f"  {fancy}")

    # Fully loaded latte
    print("\n--- Latte + Milk + Whipped Cream + Sugar ---")
    loaded = Sugar(WhippedCream(Milk(Latte())))
    print(f"  {loaded}")

    # Double milk
    print("\n--- Espresso + Double Milk ---")
    double = Milk(Milk(Espresso()))
    print(f"  {double}")

    print("\nDecorators stack costs: each adds to the total!")


if __name__ == "__main__":
    main()
