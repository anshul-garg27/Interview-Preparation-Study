"""
Refactoring Techniques Demo
============================
Runnable Python demo showing 5 key refactorings with BEFORE (bad) and AFTER (good) code.
Each refactoring prints clear output demonstrating the improvement.

Run: python refactoring_demo.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import re


# ============================================================================
# 1. EXTRACT METHOD
# ============================================================================

def demo_extract_method():
    print("=" * 60)
    print("REFACTORING #1: Extract Method")
    print("=" * 60)

    # BEFORE: One long method doing everything
    print("\n--- BEFORE (monolithic method) ---")

    def print_invoice_before(customer, items):
        """One big method -- hard to read, hard to test."""
        output = []
        output.append("=" * 40)
        output.append("INVOICE")
        output.append(f"Customer: {customer}")
        output.append("=" * 40)
        total = 0
        for name, qty, price in items:
            amount = qty * price
            total += amount
            output.append(f"  {name}: {qty} x ${price:.2f} = ${amount:.2f}")
        tax = total * 0.08
        grand = total + tax
        output.append("-" * 40)
        output.append(f"  Subtotal: ${total:.2f}")
        output.append(f"  Tax:      ${tax:.2f}")
        output.append(f"  TOTAL:    ${grand:.2f}")
        return "\n".join(output)

    items = [("Widget", 3, 9.99), ("Gadget", 1, 24.99), ("Gizmo", 2, 14.99)]
    print(print_invoice_before("Alice", items))

    # AFTER: Extracted into focused methods
    print("\n--- AFTER (extracted methods) ---")

    def format_header(customer):
        return f"{'=' * 40}\nINVOICE\nCustomer: {customer}\n{'=' * 40}"

    def format_line_items(items):
        lines = []
        total = 0
        for name, qty, price in items:
            amount = qty * price
            total += amount
            lines.append(f"  {name}: {qty} x ${price:.2f} = ${amount:.2f}")
        return "\n".join(lines), total

    def format_totals(subtotal, tax_rate=0.08):
        tax = subtotal * tax_rate
        grand = subtotal + tax
        return f"{'-' * 40}\n  Subtotal: ${subtotal:.2f}\n  Tax:      ${tax:.2f}\n  TOTAL:    ${grand:.2f}"

    def print_invoice_after(customer, items):
        """Composed of small, testable, reusable methods."""
        line_items, total = format_line_items(items)
        return f"{format_header(customer)}\n{line_items}\n{format_totals(total)}"

    print(print_invoice_after("Alice", items))
    print("\n[Benefit: Each method is independently testable and reusable]")


# ============================================================================
# 2. REPLACE CONDITIONAL WITH POLYMORPHISM
# ============================================================================

def demo_replace_conditional():
    print("\n" + "=" * 60)
    print("REFACTORING #2: Replace Conditional with Polymorphism")
    print("=" * 60)

    # BEFORE: Switch on type string
    print("\n--- BEFORE (if/elif chain) ---")

    def calculate_shipping_before(package_type, weight):
        """Every new package type means modifying this function."""
        if package_type == "standard":
            cost = weight * 2.5
            days = 7
        elif package_type == "express":
            cost = weight * 5.0
            days = 3
        elif package_type == "overnight":
            cost = weight * 10.0 + 15.0
            days = 1
        else:
            raise ValueError(f"Unknown type: {package_type}")
        return cost, days

    for ptype in ["standard", "express", "overnight"]:
        cost, days = calculate_shipping_before(ptype, 5.0)
        print(f"  {ptype:>10}: ${cost:.2f}, {days} days")

    # AFTER: Polymorphism
    print("\n--- AFTER (polymorphic classes) ---")

    class ShippingMethod(ABC):
        @abstractmethod
        def calculate(self, weight: float) -> tuple:
            pass

        @abstractmethod
        def name(self) -> str:
            pass

    class StandardShipping(ShippingMethod):
        def name(self):
            return "standard"

        def calculate(self, weight):
            return weight * 2.5, 7

    class ExpressShipping(ShippingMethod):
        def name(self):
            return "express"

        def calculate(self, weight):
            return weight * 5.0, 3

    class OvernightShipping(ShippingMethod):
        def name(self):
            return "overnight"

        def calculate(self, weight):
            return weight * 10.0 + 15.0, 1

    methods = [StandardShipping(), ExpressShipping(), OvernightShipping()]
    for method in methods:
        cost, days = method.calculate(5.0)
        print(f"  {method.name():>10}: ${cost:.2f}, {days} days")

    print("\n[Benefit: Adding 'SameDay' shipping = new class, zero changes to existing code]")


# ============================================================================
# 3. INTRODUCE PARAMETER OBJECT
# ============================================================================

def demo_parameter_object():
    print("\n" + "=" * 60)
    print("REFACTORING #3: Introduce Parameter Object")
    print("=" * 60)

    # BEFORE: Too many parameters
    print("\n--- BEFORE (long parameter list) ---")

    def search_before(query, min_price, max_price, category, in_stock,
                      sort_by, sort_order, page, page_size):
        """9 parameters -- easy to mix up, hard to extend."""
        print(f"  Searching '{query}' in {category}, "
              f"${min_price}-${max_price}, stock={in_stock}, "
              f"sort={sort_by} {sort_order}, page {page}/{page_size}")

    search_before("laptop", 500, 2000, "electronics", True,
                  "price", "asc", 1, 20)

    # AFTER: Parameter object
    print("\n--- AFTER (parameter object) ---")

    @dataclass
    class PriceRange:
        min_price: float = 0
        max_price: float = float("inf")

        def __str__(self):
            return f"${self.min_price}-${self.max_price}"

    @dataclass
    class Pagination:
        page: int = 1
        page_size: int = 20

        @property
        def offset(self):
            return (self.page - 1) * self.page_size

    @dataclass
    class SearchCriteria:
        query: str
        price_range: PriceRange = None
        category: str = None
        in_stock: bool = True
        sort_by: str = "relevance"
        sort_order: str = "desc"
        pagination: Pagination = None

        def __post_init__(self):
            if self.price_range is None:
                self.price_range = PriceRange()
            if self.pagination is None:
                self.pagination = Pagination()

    def search_after(criteria: SearchCriteria):
        """Single parameter -- clear, extensible, self-documenting."""
        print(f"  Searching '{criteria.query}' in {criteria.category}, "
              f"{criteria.price_range}, stock={criteria.in_stock}, "
              f"sort={criteria.sort_by} {criteria.sort_order}, "
              f"page {criteria.pagination.page}/{criteria.pagination.page_size}")

    criteria = SearchCriteria(
        query="laptop",
        price_range=PriceRange(500, 2000),
        category="electronics",
        sort_by="price",
        sort_order="asc",
    )
    search_after(criteria)

    print("\n[Benefit: Self-documenting calls, defaults built in, easy to add new filters]")


# ============================================================================
# 4. EXTRACT CLASS (God Class -> Focused Classes)
# ============================================================================

def demo_extract_class():
    print("\n" + "=" * 60)
    print("REFACTORING #4: Extract Class (God Class Fix)")
    print("=" * 60)

    # BEFORE: God class
    print("\n--- BEFORE (God Class) ---")

    class GodEmployee:
        """Does everything: pay, taxes, display, serialization."""
        def __init__(self, name, salary, tax_rate, department):
            self.name = name
            self.salary = salary
            self.tax_rate = tax_rate
            self.department = department

        def calculate_monthly_pay(self):
            return self.salary / 12

        def calculate_tax(self):
            return self.salary * self.tax_rate

        def calculate_net_pay(self):
            gross = self.calculate_monthly_pay()
            tax = self.calculate_tax() / 12
            return gross - tax

        def to_json(self):
            return f'{{"name": "{self.name}", "salary": {self.salary}}}'

        def to_csv(self):
            return f"{self.name},{self.salary},{self.department}"

        def display_badge(self):
            return f"[{self.department}] {self.name}"

        def display_payslip(self):
            return (f"Payslip for {self.name}\n"
                    f"  Gross: ${self.calculate_monthly_pay():.2f}\n"
                    f"  Tax:   ${self.calculate_tax()/12:.2f}\n"
                    f"  Net:   ${self.calculate_net_pay():.2f}")

    emp = GodEmployee("Alice", 120000, 0.25, "Engineering")
    print(f"  Badge: {emp.display_badge()}")
    print(f"  JSON: {emp.to_json()}")
    print(f"  {emp.display_payslip()}")

    # AFTER: Focused classes
    print("\n--- AFTER (Focused Classes) ---")

    class Employee:
        """Core employee data only."""
        def __init__(self, name, salary, tax_rate, department):
            self.name = name
            self.salary = salary
            self.tax_rate = tax_rate
            self.department = department

    class PayrollCalculator:
        """All pay-related logic."""
        def monthly_gross(self, emp: Employee):
            return emp.salary / 12

        def monthly_tax(self, emp: Employee):
            return emp.salary * emp.tax_rate / 12

        def monthly_net(self, emp: Employee):
            return self.monthly_gross(emp) - self.monthly_tax(emp)

    class EmployeeSerializer:
        """All serialization logic."""
        def to_json(self, emp: Employee):
            return f'{{"name": "{emp.name}", "salary": {emp.salary}}}'

        def to_csv(self, emp: Employee):
            return f"{emp.name},{emp.salary},{emp.department}"

    class EmployeeDisplay:
        """All display logic."""
        def __init__(self, payroll: PayrollCalculator):
            self.payroll = payroll

        def badge(self, emp: Employee):
            return f"[{emp.department}] {emp.name}"

        def payslip(self, emp: Employee):
            return (f"Payslip for {emp.name}\n"
                    f"  Gross: ${self.payroll.monthly_gross(emp):.2f}\n"
                    f"  Tax:   ${self.payroll.monthly_tax(emp):.2f}\n"
                    f"  Net:   ${self.payroll.monthly_net(emp):.2f}")

    emp = Employee("Alice", 120000, 0.25, "Engineering")
    payroll = PayrollCalculator()
    display = EmployeeDisplay(payroll)
    serializer = EmployeeSerializer()

    print(f"  Badge: {display.badge(emp)}")
    print(f"  JSON: {serializer.to_json(emp)}")
    print(f"  {display.payslip(emp)}")

    print("\n[Benefit: Each class has one reason to change. Easy to test independently.]")


# ============================================================================
# 5. REPLACE PRIMITIVE WITH OBJECT
# ============================================================================

def demo_replace_primitive():
    print("\n" + "=" * 60)
    print("REFACTORING #5: Replace Primitive with Value Object")
    print("=" * 60)

    # BEFORE: Strings everywhere
    print("\n--- BEFORE (primitives) ---")

    def create_user_before(name, email, phone):
        # Validation scattered, repeated everywhere
        if "@" not in email:
            print(f"  ERROR: Invalid email '{email}'")
            return None
        digits = re.sub(r"\D", "", phone)
        if len(digits) != 10:
            print(f"  ERROR: Invalid phone '{phone}'")
            return None
        print(f"  Created user: {name}, {email}, ({digits[:3]}) {digits[3:6]}-{digits[6:]}")
        return {"name": name, "email": email, "phone": phone}

    create_user_before("Alice", "alice@example.com", "555-123-4567")
    create_user_before("Bob", "invalid-email", "555-123-4567")
    create_user_before("Charlie", "charlie@x.com", "12345")

    # AFTER: Value objects
    print("\n--- AFTER (value objects) ---")

    @dataclass(frozen=True)
    class Email:
        value: str

        def __post_init__(self):
            if not re.match(r"^[\w.+-]+@[\w.-]+\.\w+$", self.value):
                raise ValueError(f"Invalid email: {self.value}")

        def __str__(self):
            return self.value

        @property
        def domain(self):
            return self.value.split("@")[1]

    @dataclass(frozen=True)
    class PhoneNumber:
        _raw: str

        def __post_init__(self):
            digits = re.sub(r"\D", "", self._raw)
            if len(digits) != 10:
                raise ValueError(f"Invalid phone: {self._raw}")
            object.__setattr__(self, "_digits", digits)

        def formatted(self):
            d = self._digits
            return f"({d[:3]}) {d[3:6]}-{d[6:]}"

        def __str__(self):
            return self.formatted()

    @dataclass
    class User:
        name: str
        email: Email
        phone: PhoneNumber

        def __str__(self):
            return f"{self.name}, {self.email}, {self.phone}"

    def create_user_after(name, email_str, phone_str):
        try:
            user = User(name, Email(email_str), PhoneNumber(phone_str))
            print(f"  Created user: {user}")
            return user
        except ValueError as e:
            print(f"  ERROR: {e}")
            return None

    create_user_after("Alice", "alice@example.com", "555-123-4567")
    create_user_after("Bob", "invalid-email", "555-123-4567")
    create_user_after("Charlie", "charlie@x.com", "12345")

    # Show value object benefits
    print("\n  Value Object Extras:")
    email = Email("dev@example.com")
    print(f"    Email domain: {email.domain}")
    print(f"    Equality: {Email('a@b.com') == Email('a@b.com')}")  # True (frozen dataclass)

    print("\n[Benefit: Validation at construction, impossible to have invalid state, rich behavior]")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "#" * 60)
    print("# REFACTORING TECHNIQUES - INTERACTIVE DEMO")
    print("#" * 60)

    demo_extract_method()
    demo_replace_conditional()
    demo_parameter_object()
    demo_extract_class()
    demo_replace_primitive()

    print("\n" + "#" * 60)
    print("# SUMMARY")
    print("#" * 60)
    print("""
    1. Extract Method        -> Break long methods into named pieces
    2. Replace Conditional   -> Use polymorphism instead of if/elif
    3. Parameter Object      -> Group related params into a class
    4. Extract Class         -> Split God Class into focused classes
    5. Replace Primitive     -> Use value objects for domain concepts

    Key Insight: Refactoring preserves behavior while improving structure.
    In interviews, START simple, IDENTIFY smells, then REFACTOR with named techniques.
    """)


if __name__ == "__main__":
    main()
