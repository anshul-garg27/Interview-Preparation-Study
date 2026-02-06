"""Demo: Factory Method pattern with document creators."""

from concrete_creators import PDFCreator, WordCreator, ExcelCreator


def client_code(creator):
    """Client works with any creator without knowing the concrete product."""
    result = creator.create_document()
    doc = creator.factory_method()
    save_msg = doc.save("report")
    print(f"  {result}")
    print(f"  {save_msg}")
    print(f"  Extension: {doc.get_extension()}")


def main():
    print("=" * 50)
    print("FACTORY METHOD PATTERN")
    print("=" * 50)

    creators = {
        "PDF": PDFCreator(),
        "Word": WordCreator(),
        "Excel": ExcelCreator(),
    }

    for name, creator in creators.items():
        print(f"\n--- {name} Creator ---")
        client_code(creator)


if __name__ == "__main__":
    main()
