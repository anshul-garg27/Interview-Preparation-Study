"""Demo: Adapter pattern - legacy XML to JSON conversion."""

from adaptee import LegacyXMLSystem
from adapter import XMLtoJSONAdapter


def display_data(provider):
    """Client works with JSONDataProvider interface."""
    data = provider.get_json_data()
    count = provider.get_record_count()
    print(f"  Records: {count}")
    for user in data["users"]:
        print(f"  - {user['name']}, age {user['age']}")


def main():
    print("=" * 50)
    print("ADAPTER PATTERN")
    print("=" * 50)

    legacy = LegacyXMLSystem()
    print(f"\n--- Legacy XML Output ---")
    print(f"  {legacy.fetch_xml()[:60]}...")

    print(f"\n--- Adapted JSON Output ---")
    adapter = XMLtoJSONAdapter(legacy)
    display_data(adapter)

    print("\nLegacy XML seamlessly used as JSON!")


if __name__ == "__main__":
    main()
