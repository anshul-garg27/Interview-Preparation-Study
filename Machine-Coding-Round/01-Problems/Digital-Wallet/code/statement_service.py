"""Statement service - transaction history and filtering."""

from enums import TransactionType, TransactionStatus


class StatementService:
    """Generates wallet statements and filters transaction history."""

    def __init__(self, transaction_service):
        self._txn_service = transaction_service

    def get_statement(self, user_id, txn_type_filter=None):
        """
        Get transaction statement for a user.

        Args:
            user_id: The user whose statement to generate
            txn_type_filter: Optional TransactionType to filter (CREDIT or DEBIT)
        """
        user = self._txn_service.get_user(user_id)
        if not user:
            print(f"[ERROR] User '{user_id}' not found")
            return []

        transactions = self._txn_service.get_transactions_for_wallet(user.wallet.id)

        if txn_type_filter:
            transactions = [t for t in transactions if t.txn_type == txn_type_filter]

        return transactions

    def display_statement(self, user_id, txn_type_filter=None, title=None):
        """Display formatted statement for a user."""
        user = self._txn_service.get_user(user_id)
        if not user:
            print(f"[ERROR] User '{user_id}' not found")
            return

        filter_label = ""
        if txn_type_filter:
            filter_label = f" ({txn_type_filter.value} only)"

        header = title or f"Transaction History: {user.name}{filter_label}"
        print(f"\n  {header}")
        print(f"  {'=' * 75}")

        transactions = self.get_statement(user_id, txn_type_filter)

        if not transactions:
            print("  (no transactions)")
        else:
            for txn in transactions:
                print(f"  {txn}")

        print(f"  {'=' * 75}")
        print(f"  Current Balance: {user.wallet.balance:.2f}")

    def display_wallet_summary(self, users=None):
        """Display balance summary for all or specified users."""
        if users is None:
            users = self._txn_service.get_all_users()

        print(f"\n  Wallet Summary")
        print(f"  {'-' * 40}")
        for user in users:
            status = user.wallet.status.value
            print(f"  {user.name:<15} {user.wallet.balance:>10.2f}  [{status}]")
        print(f"  {'-' * 40}")
