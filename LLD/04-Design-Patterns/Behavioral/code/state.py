"""
State Pattern - Allows an object to alter its behavior when its internal
state changes. The object will appear to change its class.

Examples:
1. Vending Machine: Idle, HasMoney, Dispensing, SoldOut
2. Document Workflow: Draft, Review, Approved, Published
"""
from abc import ABC, abstractmethod


# --- Vending Machine ---
class VendingState(ABC):
    @abstractmethod
    def insert_money(self, machine, amount: float) -> str:
        pass

    @abstractmethod
    def select_product(self, machine, product: str) -> str:
        pass

    @abstractmethod
    def dispense(self, machine) -> str:
        pass


class IdleState(VendingState):
    def insert_money(self, machine, amount):
        machine.balance = amount
        machine.state = HasMoneyState()
        return f"  Accepted ${amount:.2f}. Balance: ${machine.balance:.2f}"

    def select_product(self, machine, product):
        return "  Please insert money first"

    def dispense(self, machine):
        return "  Please insert money and select a product"


class HasMoneyState(VendingState):
    def insert_money(self, machine, amount):
        machine.balance += amount
        return f"  Added ${amount:.2f}. Balance: ${machine.balance:.2f}"

    def select_product(self, machine, product):
        if product not in machine.inventory:
            return f"  '{product}' not available"
        price = machine.prices[product]
        if machine.balance < price:
            return f"  Not enough money. Need ${price:.2f}, have ${machine.balance:.2f}"
        if machine.inventory[product] <= 0:
            machine.state = SoldOutState()
            return f"  '{product}' is sold out!"
        machine.selected = product
        machine.state = DispensingState()
        return f"  Selected '{product}' (${price:.2f})"

    def dispense(self, machine):
        return "  Please select a product first"


class DispensingState(VendingState):
    def insert_money(self, machine, amount):
        return "  Please wait, dispensing..."

    def select_product(self, machine, product):
        return "  Please wait, dispensing..."

    def dispense(self, machine):
        product = machine.selected
        price = machine.prices[product]
        machine.inventory[product] -= 1
        machine.balance -= price
        change = machine.balance
        result = f"  Dispensed: {product}!"
        if change > 0:
            result += f" Change: ${change:.2f}"
            machine.balance = 0
        machine.selected = None
        machine.state = IdleState()
        return result


class SoldOutState(VendingState):
    def insert_money(self, machine, amount):
        return "  Machine is sold out. Returning money."

    def select_product(self, machine, product):
        return "  Machine is sold out."

    def dispense(self, machine):
        return "  Machine is sold out."


class VendingMachine:
    def __init__(self):
        self.state: VendingState = IdleState()
        self.inventory = {"Cola": 2, "Chips": 1, "Water": 3}
        self.prices = {"Cola": 1.50, "Chips": 2.00, "Water": 1.00}
        self.balance = 0.0
        self.selected = None

    def insert_money(self, amount):
        return self.state.insert_money(self, amount)

    def select_product(self, product):
        return self.state.select_product(self, product)

    def dispense(self):
        return self.state.dispense(self)

    def status(self):
        return f"  [State: {type(self.state).__name__}, Balance: ${self.balance:.2f}]"


# --- Document Workflow ---
class DocState(ABC):
    @abstractmethod
    def edit(self, doc) -> str: pass
    @abstractmethod
    def review(self, doc) -> str: pass
    @abstractmethod
    def approve(self, doc) -> str: pass
    @abstractmethod
    def publish(self, doc) -> str: pass


class DraftState(DocState):
    def edit(self, doc):    return "  Editing draft..."
    def review(self, doc):
        doc.state = ReviewState()
        return "  Submitted for review"
    def approve(self, doc): return "  Cannot approve a draft"
    def publish(self, doc): return "  Cannot publish a draft"


class ReviewState(DocState):
    def edit(self, doc):
        doc.state = DraftState()
        return "  Sent back to draft for edits"
    def review(self, doc):  return "  Already in review"
    def approve(self, doc):
        doc.state = ApprovedState()
        return "  Document approved!"
    def publish(self, doc): return "  Must be approved first"


class ApprovedState(DocState):
    def edit(self, doc):
        doc.state = DraftState()
        return "  Reopened as draft"
    def review(self, doc):  return "  Already approved"
    def approve(self, doc): return "  Already approved"
    def publish(self, doc):
        doc.state = PublishedState()
        return "  Document published!"


class PublishedState(DocState):
    def edit(self, doc):    return "  Cannot edit published document"
    def review(self, doc):  return "  Cannot review published document"
    def approve(self, doc): return "  Already published"
    def publish(self, doc): return "  Already published"


class Document:
    def __init__(self, title):
        self.title = title
        self.state: DocState = DraftState()

    def status(self):
        return f"  [{self.title}: {type(self.state).__name__}]"


if __name__ == "__main__":
    print("=" * 60)
    print("STATE PATTERN DEMO")
    print("=" * 60)

    # Vending Machine
    print("\n--- Vending Machine ---")
    vm = VendingMachine()
    actions = [
        lambda: vm.select_product("Cola"),    # No money
        lambda: vm.insert_money(2.00),
        lambda: vm.select_product("Cola"),
        lambda: vm.dispense(),                 # Get cola + change
        lambda: vm.insert_money(1.00),
        lambda: vm.select_product("Water"),
        lambda: vm.dispense(),
    ]
    for action in actions:
        print(action())
        print(vm.status())

    # Document Workflow
    print("\n--- Document Workflow ---")
    doc = Document("API Spec")
    for action_name, action in [
        ("edit", doc.state.edit), ("review", doc.state.review),
    ]:
        print(action(doc)); print(doc.status())
    print(doc.state.approve(doc)); print(doc.status())
    print(doc.state.publish(doc)); print(doc.status())
    print(doc.state.edit(doc))  # Can't edit published
