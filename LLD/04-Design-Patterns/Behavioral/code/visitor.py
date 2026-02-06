"""
Visitor Pattern - Separates an algorithm from the object structure
it operates on. Lets you add new operations without modifying the classes.

Examples:
1. Shopping Cart: Book, Electronics, Clothing with Tax, Shipping, Discount visitors
2. AST: NumberNode, AddNode, MultiplyNode with Print, Eval visitors
"""
from abc import ABC, abstractmethod


# --- Shopping Cart ---
class CartItem(ABC):
    def __init__(self, name: str, price: float, weight: float):
        self.name = name
        self.price = price
        self.weight = weight

    @abstractmethod
    def accept(self, visitor: 'CartVisitor'):
        pass


class Book(CartItem):
    def __init__(self, name, price, weight, pages: int):
        super().__init__(name, price, weight)
        self.pages = pages

    def accept(self, visitor):
        return visitor.visit_book(self)


class Electronics(CartItem):
    def __init__(self, name, price, weight, warranty_years: int):
        super().__init__(name, price, weight)
        self.warranty_years = warranty_years

    def accept(self, visitor):
        return visitor.visit_electronics(self)


class Clothing(CartItem):
    def __init__(self, name, price, weight, size: str):
        super().__init__(name, price, weight)
        self.size = size

    def accept(self, visitor):
        return visitor.visit_clothing(self)


class CartVisitor(ABC):
    @abstractmethod
    def visit_book(self, book: Book) -> float: pass
    @abstractmethod
    def visit_electronics(self, item: Electronics) -> float: pass
    @abstractmethod
    def visit_clothing(self, item: Clothing) -> float: pass


class TaxVisitor(CartVisitor):
    def visit_book(self, book):
        return book.price * 0.05  # 5% tax on books

    def visit_electronics(self, item):
        return item.price * 0.18  # 18% on electronics

    def visit_clothing(self, item):
        return item.price * 0.12  # 12% on clothing


class ShippingCostVisitor(CartVisitor):
    def visit_book(self, book):
        return book.weight * 2.0  # $2/kg for books (media mail)

    def visit_electronics(self, item):
        return item.weight * 5.0 + 3.0  # $5/kg + $3 insurance

    def visit_clothing(self, item):
        return 4.99  # Flat rate for clothing


class DiscountVisitor(CartVisitor):
    def visit_book(self, book):
        return book.price * 0.10 if book.price > 20 else 0  # 10% off books over $20

    def visit_electronics(self, item):
        return item.price * 0.05 if item.warranty_years >= 2 else 0

    def visit_clothing(self, item):
        return item.price * 0.20  # 20% off all clothing


# --- AST Visitor ---
class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor'):
        pass


class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_number(self)


class AddNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_add(self)


class MultiplyNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_multiply(self)


class ASTVisitor(ABC):
    @abstractmethod
    def visit_number(self, node: NumberNode): pass
    @abstractmethod
    def visit_add(self, node: AddNode): pass
    @abstractmethod
    def visit_multiply(self, node: MultiplyNode): pass


class PrintVisitor(ASTVisitor):
    def visit_number(self, node):
        return str(int(node.value))

    def visit_add(self, node):
        return f"({node.left.accept(self)} + {node.right.accept(self)})"

    def visit_multiply(self, node):
        return f"({node.left.accept(self)} * {node.right.accept(self)})"


class EvalVisitor(ASTVisitor):
    def visit_number(self, node):
        return node.value

    def visit_add(self, node):
        return node.left.accept(self) + node.right.accept(self)

    def visit_multiply(self, node):
        return node.left.accept(self) * node.right.accept(self)


if __name__ == "__main__":
    print("=" * 60)
    print("VISITOR PATTERN DEMO")
    print("=" * 60)

    # Shopping Cart
    print("\n--- Shopping Cart ---")
    cart = [
        Book("Design Patterns", 45.00, 0.8, 395),
        Electronics("Headphones", 199.99, 0.3, 2),
        Clothing("T-Shirt", 25.00, 0.2, "M"),
    ]

    tax_visitor = TaxVisitor()
    shipping_visitor = ShippingCostVisitor()

    print(f"  {'Item':<20} {'Price':>8} {'Tax':>8} {'Shipping':>10}")
    print(f"  {'-'*48}")
    total_price, total_tax, total_ship = 0, 0, 0
    for item in cart:
        tax = item.accept(tax_visitor)
        ship = item.accept(shipping_visitor)
        print(f"  {item.name:<20} ${item.price:>7.2f} ${tax:>7.2f} ${ship:>9.2f}")
        total_price += item.price
        total_tax += tax
        total_ship += ship

    print(f"  {'-'*48}")
    print(f"  {'TOTAL':<20} ${total_price:>7.2f} ${total_tax:>7.2f} ${total_ship:>9.2f}")
    print(f"  Grand Total: ${total_price + total_tax + total_ship:.2f}")

    # AST
    print("\n--- AST Visitor ---")
    # Expression: (3 + 5) * (2 + 4)
    ast = MultiplyNode(
        AddNode(NumberNode(3), NumberNode(5)),
        AddNode(NumberNode(2), NumberNode(4))
    )

    printer = PrintVisitor()
    evaluator = EvalVisitor()
    print(f"  Expression: {ast.accept(printer)}")
    print(f"  Result:     {ast.accept(evaluator)}")

    # Expression: 2 * (3 + 7)
    ast2 = MultiplyNode(NumberNode(2), AddNode(NumberNode(3), NumberNode(7)))
    print(f"  Expression: {ast2.accept(printer)}")
    print(f"  Result:     {ast2.accept(evaluator)}")
