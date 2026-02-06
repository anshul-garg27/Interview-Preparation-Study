"""OCP Violation - Adding new discount type requires modifying existing code."""


class DiscountCalculator:
    """BAD: Every new customer type means modifying this method.
    Adding 'premium' requires changing existing, tested code."""

    def calculate(self, customer_type: str, amount: float) -> float:
        if customer_type == "regular":
            return amount * 0.0
        elif customer_type == "silver":
            return amount * 0.10
        elif customer_type == "gold":
            return amount * 0.20
        elif customer_type == "employee":
            return amount * 0.30
        # To add "platinum" discount, we MUST modify this method!
        else:
            raise ValueError(f"Unknown customer type: {customer_type}")


if __name__ == "__main__":
    print("BAD DESIGN: Open/Closed Violation\n")

    calc = DiscountCalculator()
    amount = 100.0

    for ctype in ["regular", "silver", "gold", "employee"]:
        discount = calc.calculate(ctype, amount)
        print(f"  {ctype:10s}: ${amount:.0f} - ${discount:.0f} = ${amount - discount:.0f}")

    print("\nPROBLEMS:")
    print("  1. Adding 'platinum' requires MODIFYING calculate()")
    print("  2. Every modification risks breaking existing logic")
    print("  3. if/elif chain grows endlessly")
    print("  4. Cannot add new types without touching existing code")

    # This will crash - type not handled
    try:
        calc.calculate("platinum", amount)
    except ValueError as e:
        print(f"\n  Error adding new type: {e}")
