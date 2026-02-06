"""
Machine Coding Round - Reusable Template
=========================================
Use this as a starting point for any machine coding problem.
Copy this template and modify the entities, services, and demo.

Structure:
1. Enums          - All constants and types
2. Models         - Data classes / entities
3. Repository     - In-memory storage
4. Service        - Business logic
5. Controller     - Input parsing & orchestration
6. Demo/Main      - Driver code to showcase features
"""

from enum import Enum, auto
from abc import ABC, abstractmethod
from datetime import datetime
from collections import defaultdict
import uuid


# =============================================================================
# 1. ENUMS - Define all constants here
# =============================================================================

class EntityStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class EntityType(Enum):
    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"


# =============================================================================
# 2. MODELS - Data classes for your domain entities
# =============================================================================

class BaseEntity:
    """Base class for all entities with common fields."""

    def __init__(self, name):
        self.id = self._generate_id()
        self.name = name
        self.status = EntityStatus.ACTIVE
        self.created_at = datetime.now()

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())[:8]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    def __repr__(self):
        return self.__str__()


class User(BaseEntity):
    """User entity."""

    def __init__(self, name, email):
        super().__init__(name)
        self.email = email


class Item(BaseEntity):
    """Generic domain entity - rename to match your problem."""

    def __init__(self, name, item_type, owner_id=None):
        super().__init__(name)
        self.item_type = item_type
        self.owner_id = owner_id


# =============================================================================
# 3. REPOSITORY - In-memory storage with CRUD operations
# =============================================================================

class InMemoryRepository:
    """Generic in-memory repository with indexing support."""

    def __init__(self):
        self._store = {}                      # id -> entity
        self._index_by_type = defaultdict(list)  # type -> [ids]

    def save(self, entity):
        self._store[entity.id] = entity
        if hasattr(entity, 'item_type'):
            self._index_by_type[entity.item_type].append(entity.id)
        return entity

    def find_by_id(self, entity_id):
        return self._store.get(entity_id)

    def find_all(self):
        return list(self._store.values())

    def find_by_status(self, status):
        return [e for e in self._store.values() if e.status == status]

    def find_by_type(self, entity_type):
        ids = self._index_by_type.get(entity_type, [])
        return [self._store[eid] for eid in ids if eid in self._store]

    def find_by_predicate(self, predicate):
        return [e for e in self._store.values() if predicate(e)]

    def delete(self, entity_id):
        entity = self._store.get(entity_id)
        if entity:
            entity.status = EntityStatus.DELETED
            return True
        return False

    def count(self):
        return len([e for e in self._store.values()
                    if e.status != EntityStatus.DELETED])


# =============================================================================
# 4. SERVICE - Business logic layer
# =============================================================================

class EntityService:
    """Core business logic - rename and modify for your problem."""

    def __init__(self):
        self._user_repo = InMemoryRepository()
        self._item_repo = InMemoryRepository()

    # --- User Operations ---
    def create_user(self, name, email):
        user = User(name, email)
        self._user_repo.save(user)
        print(f"[SUCCESS] User created: {user.name} (ID: {user.id})")
        return user

    def get_user(self, user_id):
        user = self._user_repo.find_by_id(user_id)
        if not user:
            print(f"[ERROR] User not found: {user_id}")
        return user

    # --- Item Operations ---
    def create_item(self, name, item_type, owner_id):
        owner = self.get_user(owner_id)
        if not owner:
            return None

        item = Item(name, item_type, owner_id)
        self._item_repo.save(item)
        print(f"[SUCCESS] Item created: {item.name} (ID: {item.id})")
        return item

    def get_item(self, item_id):
        item = self._item_repo.find_by_id(item_id)
        if not item:
            print(f"[ERROR] Item not found: {item_id}")
        return item

    def get_all_items(self):
        return self._item_repo.find_by_status(EntityStatus.ACTIVE)

    def get_items_by_type(self, item_type):
        return self._item_repo.find_by_type(item_type)

    def delete_item(self, item_id):
        if self._item_repo.delete(item_id):
            print(f"[SUCCESS] Item deleted: {item_id}")
            return True
        print(f"[ERROR] Item not found: {item_id}")
        return False


# =============================================================================
# 5. STRATEGY PATTERN - For pluggable algorithms (if needed)
# =============================================================================

class ProcessingStrategy(ABC):
    """Base strategy - implement for different processing algorithms."""

    @abstractmethod
    def process(self, item):
        pass


class DefaultStrategy(ProcessingStrategy):
    def process(self, item):
        print(f"  Processing {item.name} with default strategy")
        return True


class PriorityStrategy(ProcessingStrategy):
    def process(self, item):
        print(f"  Processing {item.name} with priority strategy")
        return True


# =============================================================================
# 6. OUTPUT FORMATTER - Clean display
# =============================================================================

class OutputFormatter:
    """Utility for formatted console output."""

    @staticmethod
    def header(title):
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    @staticmethod
    def section(title):
        print(f"\n--- {title} ---")

    @staticmethod
    def table(headers, rows):
        if not rows:
            print("  (no data)")
            return
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
        print(f"  {header_line}")
        print(f"  {'-' * len(header_line)}")
        for row in rows:
            line = " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
            print(f"  {line}")

    @staticmethod
    def success(msg):
        print(f"[SUCCESS] {msg}")

    @staticmethod
    def error(msg):
        print(f"[ERROR] {msg}")


# =============================================================================
# 7. DEMO / MAIN - Driver code
# =============================================================================

def main():
    """Demo showcasing all features of the system."""

    fmt = OutputFormatter()
    service = EntityService()

    # --- Setup ---
    fmt.header("MACHINE CODING TEMPLATE DEMO")

    # --- Feature 1: Create Users ---
    fmt.section("Creating Users")
    alice = service.create_user("Alice", "alice@example.com")
    bob = service.create_user("Bob", "bob@example.com")

    # --- Feature 2: Create Items ---
    fmt.section("Creating Items")
    item1 = service.create_item("Item Alpha", EntityType.TYPE_A, alice.id)
    item2 = service.create_item("Item Beta", EntityType.TYPE_B, alice.id)
    item3 = service.create_item("Item Gamma", EntityType.TYPE_A, bob.id)

    # --- Feature 3: Query Items ---
    fmt.section("All Active Items")
    items = service.get_all_items()
    rows = [[i.id, i.name, i.item_type.value, i.status.value] for i in items]
    fmt.table(["ID", "Name", "Type", "Status"], rows)

    # --- Feature 4: Filter by Type ---
    fmt.section("Items of TYPE_A")
    type_a_items = service.get_items_by_type(EntityType.TYPE_A)
    rows = [[i.id, i.name, i.owner_id] for i in type_a_items]
    fmt.table(["ID", "Name", "Owner ID"], rows)

    # --- Feature 5: Delete Item ---
    fmt.section("Deleting an Item")
    service.delete_item(item2.id)

    # --- Feature 6: Show Final State ---
    fmt.section("Final State - Active Items")
    items = service.get_all_items()
    rows = [[i.id, i.name, i.item_type.value, i.status.value] for i in items]
    fmt.table(["ID", "Name", "Type", "Status"], rows)

    # --- Error Handling Demo ---
    fmt.section("Error Handling")
    service.get_user("nonexistent-id")
    service.delete_item("nonexistent-id")
    service.create_item("Orphan Item", EntityType.TYPE_A, "bad-owner-id")

    fmt.header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
