"""Demo: Composite pattern - file system tree."""

from file import File
from directory import Directory


def main():
    print("=" * 50)
    print("COMPOSITE PATTERN")
    print("=" * 50)

    # Build file tree
    root = Directory("root")
    src = Directory("src")
    tests = Directory("tests")

    src.add(File("main.py", 1500))
    src.add(File("utils.py", 800))
    src.add(File("config.py", 300))

    tests.add(File("test_main.py", 1200))
    tests.add(File("test_utils.py", 600))

    root.add(src)
    root.add(tests)
    root.add(File("README.md", 200))
    root.add(File("setup.py", 400))

    print("\n--- File Tree ---")
    root.display()

    print(f"\n--- Sizes ---")
    print(f"  root/ total: {root.get_size()} bytes")
    print(f"  src/  total: {src.get_size()} bytes")
    print(f"  tests/ total: {tests.get_size()} bytes")


if __name__ == "__main__":
    main()
