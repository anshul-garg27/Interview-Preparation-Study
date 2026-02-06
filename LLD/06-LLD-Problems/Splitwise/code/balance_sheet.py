"""
BalanceSheet - Tracks who owes whom and provides debt simplification.
Uses a greedy algorithm to minimize the number of transactions.
"""

from user import User


class BalanceSheet:
    """Tracks and simplifies debts between users."""

    @staticmethod
    def simplify_debts(net_balances: dict[str, float],
                       user_map: dict[str, User]) -> list[tuple[User, User, float]]:
        """
        Greedy algorithm: match largest debtor with largest creditor
        to minimize total number of settlement transactions.

        Args:
            net_balances: Dict of user_id -> net balance.
            user_map: Dict of user_id -> User for lookup.

        Returns:
            List of (from_user, to_user, amount) settlement transactions.
        """
        creditors: list[list] = []  # [amount, user_id] - people owed money
        debtors: list[list] = []    # [amount, user_id] - people who owe money

        for uid, balance in net_balances.items():
            if balance > 0.01:
                creditors.append([balance, uid])
            elif balance < -0.01:
                debtors.append([-balance, uid])

        creditors.sort(reverse=True)
        debtors.sort(reverse=True)
        transactions: list[tuple[User, User, float]] = []

        i, j = 0, 0
        while i < len(creditors) and j < len(debtors):
            settle_amount = min(creditors[i][0], debtors[j][0])
            settle_amount = round(settle_amount, 2)
            if settle_amount > 0.01:
                from_user = user_map[debtors[j][1]]
                to_user = user_map[creditors[i][1]]
                transactions.append((from_user, to_user, settle_amount))
            creditors[i][0] = round(creditors[i][0] - settle_amount, 2)
            debtors[j][0] = round(debtors[j][0] - settle_amount, 2)
            if creditors[i][0] < 0.01:
                i += 1
            if debtors[j][0] < 0.01:
                j += 1

        return transactions
