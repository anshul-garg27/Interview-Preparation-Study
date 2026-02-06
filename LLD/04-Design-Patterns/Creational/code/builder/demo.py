"""Demo: Builder pattern with Director."""

from concrete_builders import SimpleHouseBuilder, LuxuryHouseBuilder
from director import Director


def main():
    print("=" * 50)
    print("BUILDER PATTERN")
    print("=" * 50)

    # Simple house
    simple = SimpleHouseBuilder()
    director = Director(simple)

    print("\n--- Simple Starter Home ---")
    director.build_starter_home()
    print(simple.get_result())

    print("\n--- Simple Family Home ---")
    director.build_family_home()
    print(simple.get_result())

    # Luxury house
    luxury = LuxuryHouseBuilder()
    director.builder = luxury

    print("\n--- Luxury Mansion ---")
    director.build_mansion()
    print(luxury.get_result())

    # Builder without director
    print("\n--- Custom Build (no Director) ---")
    luxury.build_foundation()
    luxury.build_walls()
    luxury.build_rooms(3)
    print(luxury.get_result())


if __name__ == "__main__":
    main()
