"""Encapsulation - Real-world BankAccount with private balance and validation."""


class BankAccount:
    """Account with encapsulated balance - no direct manipulation allowed."""

    def __init__(self, owner: str, initial_balance: float = 0):
        self._owner = owner
        self.__balance = initial_balance
        self.__transaction_log: list[str] = []

    @property
    def balance(self) -> float:
        """Read-only access to balance."""
        return self.__balance

    @property
    def owner(self) -> str:
        return self._owner

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount
        self.__log(f"Deposited ${amount:,.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.__balance:
            raise ValueError(f"Insufficient funds (balance: ${self.__balance:,.2f})")
        self.__balance -= amount
        self.__log(f"Withdrew ${amount:,.2f}")

    def __log(self, message: str) -> None:
        """Private method - only called internally."""
        self.__transaction_log.append(message)

    def print_statement(self) -> None:
        print(f"\n--- Statement for {self._owner} ---")
        for entry in self.__transaction_log:
            print(f"  {entry}")
        print(f"  Current Balance: ${self.__balance:,.2f}")


if __name__ == "__main__":
    print("=== Encapsulation: Bank Account ===\n")

    acct = BankAccount("Alice", 1000)

    # Can read balance via property
    print(f"Balance: ${acct.balance:,.2f}")

    # Cannot set balance directly (no setter defined)
    try:
        acct.balance = 999999  # type: ignore
    except AttributeError:
        print("Cannot set balance directly - no setter!")

    # Must use controlled methods
    acct.deposit(500)
    acct.withdraw(200)

    # Validation prevents bad operations
    try:
        acct.withdraw(5000)
    except ValueError as e:
        print(f"Blocked: {e}")

    try:
        acct.deposit(-100)
    except ValueError as e:
        print(f"Blocked: {e}")

    acct.print_statement()
