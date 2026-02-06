"""Demo: Strategy pattern - multiple payment methods."""

from context import ShoppingCart
from credit_card import CreditCardPayment
from paypal import PayPalPayment
from upi import UPIPayment


def main():
    print("=" * 50)
    print("STRATEGY PATTERN")
    print("=" * 50)

    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99)
    print(f"\nCart total: ${cart.get_total():.2f}")

    # Pay with credit card
    print("\n--- Credit Card ---")
    cart.set_payment_strategy(CreditCardPayment("1234567890123456", "Alice"))
    print(f"  {cart.checkout()}")

    # Pay with PayPal
    print("\n--- PayPal ---")
    cart.set_payment_strategy(PayPalPayment("alice@email.com"))
    print(f"  {cart.checkout()}")

    # Pay with UPI
    print("\n--- UPI ---")
    cart.set_payment_strategy(UPIPayment("alice@upi"))
    print(f"  {cart.checkout()}")

    print("\nSame cart, different payment strategies!")


if __name__ == "__main__":
    main()
