"""Concrete observers - different notification channels."""

from observer import Observer


class PriceAlert(Observer):
    """Triggers an alert when price crosses a threshold."""

    def __init__(self, threshold: float):
        self._threshold = threshold

    def update(self, symbol: str, price: float):
        if price >= self._threshold:
            print(f"    [ALERT] {symbol} hit ${price:.2f} (threshold: ${self._threshold:.2f})")


class MobileApp(Observer):
    """Sends push notification to mobile app."""

    def __init__(self, user: str):
        self._user = user

    def update(self, symbol: str, price: float):
        print(f"    [PUSH -> {self._user}] {symbol} is now ${price:.2f}")


class EmailNotifier(Observer):
    """Sends email notification."""

    def __init__(self, email: str):
        self._email = email

    def update(self, symbol: str, price: float):
        print(f"    [EMAIL -> {self._email}] {symbol} price update: ${price:.2f}")
