"""Demo: Abstract Factory - cross-platform UI creation."""

from windows_factory import WindowsFactory
from mac_factory import MacFactory


def build_ui(factory):
    """Client code works with any factory without knowing the platform."""
    button = factory.create_button()
    checkbox = factory.create_checkbox()

    print(f"  {button.render()}")
    print(f"  {button.on_click('submit_form')}")
    print(f"  {checkbox.render()}")
    print(f"  {checkbox.toggle()}")


def main():
    print("=" * 50)
    print("ABSTRACT FACTORY PATTERN")
    print("=" * 50)

    print("\n--- Windows UI ---")
    build_ui(WindowsFactory())

    print("\n--- Mac UI ---")
    build_ui(MacFactory())

    print("\nSame client code, different platform components!")


if __name__ == "__main__":
    main()
