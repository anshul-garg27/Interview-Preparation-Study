"""
Receipt generator for ATM transactions.
Provides formatted output for printing or display.
"""

from transaction import Transaction


class ReceiptGenerator:
    """Generates formatted receipts from transaction records."""

    @staticmethod
    def generate(transaction: Transaction, atm_id: str) -> str:
        """
        Create a receipt string from a transaction.

        Args:
            transaction: The completed transaction.
            atm_id: ATM identifier for the receipt header.

        Returns:
            Formatted receipt string.
        """
        return transaction.generate_receipt(atm_id)

    @staticmethod
    def print_receipt(transaction: Transaction, atm_id: str) -> None:
        """Print the receipt to stdout."""
        print(ReceiptGenerator.generate(transaction, atm_id))
