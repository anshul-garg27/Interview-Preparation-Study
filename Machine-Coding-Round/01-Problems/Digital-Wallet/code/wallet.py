"""Wallet entity for the Digital Wallet System."""

from enums import WalletStatus


class Wallet:
    """Represents a digital wallet with balance management."""

    _counter = 0

    def __init__(self, user_id):
        Wallet._counter += 1
        self.id = f"W-{Wallet._counter:03d}"
        self.user_id = user_id
        self.balance = 0.0
        self.status = WalletStatus.ACTIVE
        self.first_topup_done = False

    def credit(self, amount):
        """Add money to the wallet. Returns new balance."""
        self.balance += amount
        return self.balance

    def debit(self, amount):
        """Remove money from the wallet. Returns new balance or None if insufficient."""
        if amount > self.balance:
            return None
        self.balance -= amount
        return self.balance

    def is_active(self):
        return self.status == WalletStatus.ACTIVE

    def __str__(self):
        return f"Wallet({self.id}, Balance: {self.balance:.2f}, Status: {self.status.value})"
