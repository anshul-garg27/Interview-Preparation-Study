"""Python Protocol - Structural subtyping (interfaces without inheritance)."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Repository(Protocol):
    """Interface for any data repository."""

    def save(self, data: dict) -> str: ...
    def find(self, id: str) -> dict | None: ...
    def delete(self, id: str) -> bool: ...


# These classes satisfy the Protocol WITHOUT inheriting from it

class InMemoryRepo:
    def __init__(self):
        self._store: dict[str, dict] = {}

    def save(self, data: dict) -> str:
        id = data.get("id", str(len(self._store)))
        self._store[id] = data
        return f"Saved to memory: {id}"

    def find(self, id: str) -> dict | None:
        return self._store.get(id)

    def delete(self, id: str) -> bool:
        if id in self._store:
            del self._store[id]
            return True
        return False


class FileRepo:
    def save(self, data: dict) -> str:
        return f"Saved to file: {data.get('id', 'unknown')}"

    def find(self, id: str) -> dict | None:
        return {"id": id, "source": "file"}

    def delete(self, id: str) -> bool:
        return True


def process_data(repo: Repository, data: dict) -> None:
    """Accepts ANY object matching the Repository protocol."""
    print(f"  {repo.save(data)}")
    found = repo.find(data.get("id", ""))
    print(f"  Found: {found}")


if __name__ == "__main__":
    print("=== Protocol (Structural Subtyping) ===\n")

    # Both satisfy Repository protocol - no inheritance needed
    memory = InMemoryRepo()
    file = FileRepo()

    print("--- InMemoryRepo ---")
    process_data(memory, {"id": "u1", "name": "Alice"})

    print("\n--- FileRepo ---")
    process_data(file, {"id": "u2", "name": "Bob"})

    # Runtime protocol check
    print(f"\nInMemoryRepo is Repository? {isinstance(memory, Repository)}")
    print(f"FileRepo is Repository?     {isinstance(file, Repository)}")
    print(f"str is Repository?          {isinstance('hello', Repository)}")
