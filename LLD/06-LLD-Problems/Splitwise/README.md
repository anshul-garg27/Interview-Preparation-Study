# Splitwise / Expense Splitter - Low Level Design

## Problem Statement
Design a system like Splitwise that allows users to split expenses among groups. Users can add expenses with different split strategies, track balances, and settle debts with a minimum number of transactions.

---

## Functional Requirements
1. **User Management** - Add/remove users with unique IDs
2. **Group Management** - Create groups, add/remove members
3. **Add Expenses** - Support equal, exact amount, and percentage splits
4. **Track Balances** - Maintain who owes whom and how much
5. **Simplify Debts** - Minimize the number of transactions needed to settle
6. **Settlement** - Record payments between users to settle debts
7. **Expense History** - View past expenses for a user or group

## Non-Functional Requirements
- Consistent balance tracking (no money leaks)
- Handle concurrent expense additions
- Scale to thousands of users per group
- Accurate floating-point handling for currency

---

## Design Patterns Used

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Strategy** | Split strategies (Equal, Exact, Percentage) | Different split algorithms without changing expense logic |
| **Observer** | Balance update notifications | Notify users when their balance changes |
| **Facade** | SplitwiseService | Simplify complex subsystem interactions |

### Strategy Pattern - Split Strategies
The core challenge is supporting multiple split types. Each strategy implements the same interface but computes shares differently:
- **EqualSplit**: Divides equally among all participants
- **ExactSplit**: Each person pays a specified exact amount
- **PercentageSplit**: Each person pays a percentage of the total

### Observer Pattern - Balance Updates
When an expense is added, all affected users are notified of their updated balances. This decouples the expense logic from notification logic.

---

## Class Diagram

```mermaid
classDiagram
    class User {
        -String id
        -String name
        -String email
        -Map~String, float~ balances
        +update_balance(user_id, amount)
        +get_balance(user_id) float
        +get_total_owed() float
        +get_total_owes() float
    }

    class Group {
        -String id
        -String name
        -List~User~ members
        -List~Expense~ expenses
        +add_member(user)
        +remove_member(user)
        +add_expense(expense)
        +get_group_balances() Map
    }

    class Expense {
        -String id
        -float amount
        -User paid_by
        -String description
        -SplitStrategy strategy
        -List~Split~ splits
        -datetime created_at
        +calculate_splits() List~Split~
    }

    class Split {
        -User user
        -float amount
    }

    class SplitStrategy {
        <<interface>>
        +calculate(amount, users, params) List~Split~
        +validate(amount, users, params) bool
    }

    class EqualSplitStrategy {
        +calculate(amount, users, params) List~Split~
        +validate(amount, users, params) bool
    }

    class ExactSplitStrategy {
        +calculate(amount, users, params) List~Split~
        +validate(amount, users, params) bool
    }

    class PercentageSplitStrategy {
        +calculate(amount, users, params) List~Split~
        +validate(amount, users, params) bool
    }

    class BalanceObserver {
        <<interface>>
        +on_balance_update(user, changes)
    }

    class NotificationObserver {
        +on_balance_update(user, changes)
    }

    class DebtSimplifier {
        +simplify(balances) List~Transaction~
    }

    class SplitwiseService {
        -Map~String, User~ users
        -Map~String, Group~ groups
        -List~BalanceObserver~ observers
        +add_user(name, email) User
        +create_group(name, members) Group
        +add_expense(paid_by, amount, users, strategy, params)
        +get_balances(user_id) Map
        +simplify_debts(group_id) List~Transaction~
        +settle(from_user, to_user, amount)
    }

    SplitStrategy <|.. EqualSplitStrategy
    SplitStrategy <|.. ExactSplitStrategy
    SplitStrategy <|.. PercentageSplitStrategy
    BalanceObserver <|.. NotificationObserver
    Expense --> SplitStrategy
    Expense --> Split
    Expense --> User
    Group --> User
    Group --> Expense
    SplitwiseService --> User
    SplitwiseService --> Group
    SplitwiseService --> DebtSimplifier
    SplitwiseService --> BalanceObserver
```

---

## Sequence Diagram - Adding an Expense

```mermaid
sequenceDiagram
    participant C as Client
    participant S as SplitwiseService
    participant E as Expense
    participant St as SplitStrategy
    participant U as User (payer)
    participant U2 as User (participant)
    participant O as Observer

    C->>S: add_expense(paid_by, amount, users, EQUAL, params)
    S->>St: validate(amount, users, params)
    St-->>S: True
    S->>E: new Expense(amount, paid_by, strategy)
    S->>St: calculate(amount, users, params)
    St-->>S: [Split(u1, 50), Split(u2, 50)]
    S->>U: update_balance(u2.id, +50)
    S->>U2: update_balance(u1.id, -50)
    S->>O: on_balance_update(user, changes)
    O-->>C: notification sent
    S-->>C: Expense created
```

## Sequence Diagram - Debt Simplification

```mermaid
sequenceDiagram
    participant C as Client
    participant S as SplitwiseService
    participant D as DebtSimplifier
    participant G as Group

    C->>S: simplify_debts(group_id)
    S->>G: get_group_balances()
    G-->>S: {u1: +100, u2: -60, u3: -40}
    S->>D: simplify(net_balances)
    Note over D: Separate into creditors [+100]<br/>and debtors [-60, -40]
    Note over D: Match: u2 pays u1 $60<br/>u3 pays u1 $40
    D-->>S: [Transaction(u2→u1, 60), Transaction(u3→u1, 40)]
    S-->>C: Simplified transactions
```

---

## Debt Simplification Algorithm

The key algorithmic challenge. Given N users with net balances, find minimum transactions to settle all debts:

1. **Calculate net balances** - For each user, sum all amounts owed minus all amounts they owe
2. **Separate into creditors (+) and debtors (-)**
3. **Greedy matching** - Match the largest debtor with the largest creditor
4. **Reduce** - The smaller amount is fully settled, continue with remainder

> **Note**: The optimal solution (minimum transactions) is NP-hard. The greedy approach gives a good approximation. For exact minimum, you'd use subset-sum based approaches.

---

## Edge Cases
1. **Rounding errors** - $100 split 3 ways = $33.33 + $33.33 + $33.34 (last person absorbs remainder)
2. **Self-expense** - User pays and is also a participant
3. **Zero-amount splits** - Validate that all split amounts are positive
4. **Percentage doesn't sum to 100%** - Reject the expense
5. **Exact amounts don't sum to total** - Reject the expense
6. **Empty group** - Cannot add expenses
7. **User not in group** - Cannot split with non-members
8. **Concurrent settlements** - Two users settling simultaneously

## Extensions
- Support for multiple currencies with exchange rates
- Recurring expenses (monthly rent, subscriptions)
- Expense categories and spending analytics
- Receipt image attachment
- Export to CSV/PDF
- Integration with payment gateways for direct settlement

---

## Interview Tips

1. **Start with the Strategy pattern** - This is the most natural fit for split types and interviewers expect it
2. **Discuss the simplification algorithm** - Shows algorithmic thinking beyond just OOP
3. **Mention rounding** - A subtle but important production concern
4. **Draw the class diagram first** - Show User, Group, Expense, SplitStrategy hierarchy
5. **Mention thread safety** - Balance updates should be atomic in production
6. **Common follow-up**: "How would you handle millions of users?" - Discuss sharding by user/group, eventual consistency
