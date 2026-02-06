"""User entity for the Digital Wallet System."""


class User:
    """Represents a user in the wallet system."""

    _counter = 0

    def __init__(self, name):
        User._counter += 1
        self.id = f"U-{User._counter:03d}"
        self.name = name
        self.wallet = None
        self.referred_by = None

    def __str__(self):
        balance = f"{self.wallet.balance:.2f}" if self.wallet else "No wallet"
        return f"User({self.id}, {self.name}, Balance: {balance})"
