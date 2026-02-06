"""Demo: Facade pattern - simple home theater API."""

from home_theater_facade import HomeTheaterFacade


def main():
    print("=" * 50)
    print("FACADE PATTERN")
    print("=" * 50)

    theater = HomeTheaterFacade()

    print("\n--- Watch Movie ---")
    for step in theater.watch_movie("Inception"):
        print(f"  {step}")

    print("\n--- End Movie ---")
    for step in theater.end_movie():
        print(f"  {step}")

    print("\nOne method call hides 5+ subsystem operations!")


if __name__ == "__main__":
    main()
