"""Demo: Observer pattern - stock price notifications."""

from stock import Stock
from displays import PriceAlert, MobileApp, EmailNotifier


def main():
    print("=" * 50)
    print("OBSERVER PATTERN")
    print("=" * 50)

    apple = Stock("AAPL", 150.00)

    alert = PriceAlert(155.00)
    mobile = MobileApp("Alice")
    email = EmailNotifier("bob@email.com")

    apple.attach(alert)
    apple.attach(mobile)
    apple.attach(email)

    print("\n--- Price Changes ---")
    apple.price = 152.00
    apple.price = 156.00  # Triggers alert

    # Detach email, change price again
    print("\n--- After removing email observer ---")
    apple.detach(email)
    apple.price = 148.00


if __name__ == "__main__":
    main()
