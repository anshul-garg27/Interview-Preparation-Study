"""Transaction service - core business logic for wallet operations."""

from user import User
from wallet import Wallet
from transaction import Transaction
from enums import TransactionType, TransactionCategory, TransactionStatus


class TransactionService:
    """Handles all wallet transactions: top-up, transfer, withdraw."""

    def __init__(self):
        self._users = {}          # user_id -> User
        self._wallets = {}        # wallet_id -> Wallet
        self._transactions = {}   # txn_id -> Transaction
        self._user_by_name = {}   # name -> User (for convenience)

    def create_user(self, name):
        """Create a new user with a wallet."""
        if name in self._user_by_name:
            print(f"[ERROR] User '{name}' already exists")
            return None

        user = User(name)
        wallet = Wallet(user.id)
        user.wallet = wallet

        self._users[user.id] = user
        self._wallets[wallet.id] = wallet
        self._user_by_name[name] = user

        print(f"[SUCCESS] User {name} created with wallet {wallet.id} "
              f"(Balance: {wallet.balance:.2f})")
        return user

    def add_money(self, user_id, amount):
        """Add money to a user's wallet (top-up)."""
        user = self._users.get(user_id)
        if not user:
            print(f"[ERROR] User '{user_id}' not found")
            return None

        if amount <= 0:
            print(f"[ERROR] Amount must be positive, got {amount:.2f}")
            return None

        wallet = user.wallet
        if not wallet.is_active():
            print(f"[ERROR] Wallet {wallet.id} is {wallet.status.value}")
            return None

        new_balance = wallet.credit(amount)
        txn = Transaction(
            wallet.id, TransactionType.CREDIT, TransactionCategory.TOP_UP,
            amount, description=f"Top-up by {user.name}",
            balance_after=new_balance
        )
        self._transactions[txn.id] = txn

        print(f"[SUCCESS] Added {amount:.2f} to {user.name}'s wallet. "
              f"New balance: {new_balance:.2f}")

        # Check for first top-up cashback
        is_first = not wallet.first_topup_done
        wallet.first_topup_done = True

        return txn, is_first

    def transfer(self, from_user_id, to_user_id, amount):
        """Transfer money between two users."""
        from_user = self._users.get(from_user_id)
        to_user = self._users.get(to_user_id)

        if not from_user:
            print(f"[ERROR] Sender '{from_user_id}' not found")
            return None
        if not to_user:
            print(f"[ERROR] Recipient '{to_user_id}' not found")
            return None
        if from_user_id == to_user_id:
            print(f"[ERROR] Cannot transfer to yourself")
            return None
        if amount <= 0:
            print(f"[ERROR] Amount must be positive, got {amount:.2f}")
            return None

        from_wallet = from_user.wallet
        to_wallet = to_user.wallet

        if not from_wallet.is_active():
            print(f"[ERROR] Sender's wallet is {from_wallet.status.value}")
            return None
        if not to_wallet.is_active():
            print(f"[ERROR] Recipient's wallet is {to_wallet.status.value}")
            return None

        # Check balance
        if from_wallet.balance < amount:
            print(f"[ERROR] Insufficient balance. {from_user.name} has "
                  f"{from_wallet.balance:.2f}, tried to transfer {amount:.2f}")
            # Record failed transaction
            failed_txn = Transaction(
                from_wallet.id, TransactionType.DEBIT,
                TransactionCategory.TRANSFER_OUT, amount,
                description=f"Failed transfer to {to_user.name}",
                balance_after=from_wallet.balance
            )
            failed_txn.mark_failed("Insufficient balance")
            self._transactions[failed_txn.id] = failed_txn
            return None

        # Execute transfer
        old_from = from_wallet.balance
        old_to = to_wallet.balance

        from_wallet.debit(amount)
        to_wallet.credit(amount)

        # Record debit transaction
        debit_txn = Transaction(
            from_wallet.id, TransactionType.DEBIT,
            TransactionCategory.TRANSFER_OUT, amount,
            description=f"Transfer to {to_user.name}",
            balance_after=from_wallet.balance
        )
        self._transactions[debit_txn.id] = debit_txn

        # Record credit transaction
        credit_txn = Transaction(
            to_wallet.id, TransactionType.CREDIT,
            TransactionCategory.TRANSFER_IN, amount,
            description=f"Transfer from {from_user.name}",
            balance_after=to_wallet.balance
        )
        self._transactions[credit_txn.id] = credit_txn

        print(f"[SUCCESS] Transferred {amount:.2f} from {from_user.name} to {to_user.name}")
        print(f"  {from_user.name}'s balance: {old_from:.2f} -> {from_wallet.balance:.2f}")
        print(f"  {to_user.name}'s balance: {old_to:.2f} -> {to_wallet.balance:.2f}")

        return debit_txn, credit_txn

    def withdraw(self, user_id, amount):
        """Withdraw money from a user's wallet."""
        user = self._users.get(user_id)
        if not user:
            print(f"[ERROR] User '{user_id}' not found")
            return None

        if amount <= 0:
            print(f"[ERROR] Amount must be positive, got {amount:.2f}")
            return None

        wallet = user.wallet
        if not wallet.is_active():
            print(f"[ERROR] Wallet {wallet.id} is {wallet.status.value}")
            return None

        if wallet.balance < amount:
            print(f"[ERROR] Insufficient balance. {user.name} has "
                  f"{wallet.balance:.2f}, tried to withdraw {amount:.2f}")
            return None

        old_balance = wallet.balance
        wallet.debit(amount)

        txn = Transaction(
            wallet.id, TransactionType.DEBIT,
            TransactionCategory.WITHDRAWAL, amount,
            description=f"Withdrawal by {user.name}",
            balance_after=wallet.balance
        )
        self._transactions[txn.id] = txn

        print(f"[SUCCESS] Withdrawn {amount:.2f} from {user.name}'s wallet. "
              f"Balance: {old_balance:.2f} -> {wallet.balance:.2f}")
        return txn

    def credit_to_wallet(self, wallet, amount, category, description):
        """Internal: credit amount and record transaction."""
        new_balance = wallet.credit(amount)
        txn = Transaction(
            wallet.id, TransactionType.CREDIT, category,
            amount, description=description,
            balance_after=new_balance
        )
        self._transactions[txn.id] = txn
        return txn

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_user_by_name(self, name):
        return self._user_by_name.get(name)

    def get_all_users(self):
        return list(self._users.values())

    def get_transactions_for_wallet(self, wallet_id):
        """Get all transactions for a wallet, sorted by timestamp."""
        txns = [t for t in self._transactions.values() if t.wallet_id == wallet_id]
        return sorted(txns, key=lambda t: t.timestamp)
