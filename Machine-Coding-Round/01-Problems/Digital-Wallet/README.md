# Digital Wallet System

## Problem Statement

Design and implement a **Digital Wallet System** that allows users to manage their
digital wallets, transfer money, view transaction history, and earn cashback offers.

**Time Limit**: 90 minutes

---

## Requirements

### Functional Requirements

1. **User & Wallet Management**
   - Create users with a unique wallet
   - Each user has exactly one wallet
   - Wallet starts with zero balance
   - Add money to wallet (top-up)

2. **Transactions**
   - Transfer money from one wallet to another
   - Withdraw money from wallet
   - All transactions are recorded with timestamp, type, amount, and status
   - Transactions can succeed or fail (insufficient balance)

3. **Statement & History**
   - View transaction history for a user
   - Filter transactions by type (CREDIT, DEBIT)
   - View wallet balance at any point

4. **Offers & Cashback**
   - First top-up gets 10% cashback (up to a max of 100)
   - Referral bonus: When User A refers User B, both get a fixed bonus (50)
   - Show all offers applied to a user

5. **Edge Cases**
   - Cannot transfer to self
   - Cannot transfer/withdraw more than available balance
   - Cannot add negative amounts
   - Invalid user IDs should show error messages

### Non-Functional Requirements
- In-memory storage
- Modular code with separate files
- Use enums for transaction types, wallet status
- Clear transaction receipts in output

---

## Sample Input/Output

```
=== Creating Users ===
[SUCCESS] User Alice created with wallet W-001 (Balance: 0.00)
[SUCCESS] User Bob created with wallet W-002 (Balance: 0.00)
[SUCCESS] User Charlie created with wallet W-003 (Balance: 0.00)

=== Adding Money ===
[SUCCESS] Added 1000.00 to Alice's wallet. New balance: 1000.00
[CASHBACK] First top-up bonus: 100.00 credited to Alice's wallet
[SUCCESS] Added 500.00 to Bob's wallet. New balance: 500.00
[CASHBACK] First top-up bonus: 50.00 credited to Bob's wallet

=== Transfer Money ===
[SUCCESS] Transferred 200.00 from Alice to Bob
  Alice's balance: 900.00 -> 700.00
  Bob's balance: 550.00 -> 750.00
[ERROR] Insufficient balance. Charlie has 0.00, tried to transfer 100.00

=== Transaction History: Alice ===
  TXN-001  CREDIT   +1000.00  TOP_UP          Balance: 1000.00
  TXN-002  CREDIT   +100.00   CASHBACK        Balance: 1100.00
  TXN-003  DEBIT    -200.00   TRANSFER_OUT    Balance: 900.00

=== Wallet Summary ===
  Alice:   900.00
  Bob:     750.00
  Charlie: 0.00
```

---

## Class Diagram

```
┌──────────────┐       ┌──────────────┐
│    User      │──────>│   Wallet     │
│              │  1:1  │              │
│ - id         │       │ - id         │
│ - name       │       │ - balance    │
│ - wallet     │       │ - status     │
└──────────────┘       │ - user_id    │
                       └──────┬───────┘
                              │ 0..*
                       ┌──────┴───────┐
                       │ Transaction  │
                       │              │
                       │ - id         │
                       │ - type       │
                       │ - amount     │
                       │ - timestamp  │
                       │ - status     │
                       │ - wallet_id  │
                       │ - description│
                       └──────────────┘

┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ TransactionService   │  │ StatementService    │  │ OfferService        │
│                      │  │                     │  │                     │
│ + add_money()        │  │ + get_statement()   │  │ + apply_first_topup│
│ + transfer()         │  │ + filter_by_type()  │  │ + apply_referral()  │
│ + withdraw()         │  │ + get_balance()     │  │ + get_offers()      │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘

Enums: TransactionType (CREDIT, DEBIT)
       TransactionCategory (TOP_UP, TRANSFER_IN, TRANSFER_OUT, WITHDRAWAL, CASHBACK, REFERRAL)
       WalletStatus (ACTIVE, FROZEN, CLOSED)
       TransactionStatus (SUCCESS, FAILED)
```

---

## File Structure

```
code/
├── enums.py                # TransactionType, WalletStatus, etc.
├── user.py                 # User entity
├── wallet.py               # Wallet with balance management
├── transaction.py          # Transaction record
├── transaction_service.py  # Core transfer/add/withdraw logic
├── statement_service.py    # Transaction history and filtering
├── offer_service.py        # Cashback and referral bonuses
└── demo.py                 # Full working demo
```

---

## Evaluation Criteria

| Criteria | Points | What They Look For |
|----------|--------|--------------------|
| Executable | 30 | demo.py runs, all transaction types work |
| Modularity | 25 | Separate files, Wallet doesn't know about Offers |
| Extensibility | 15 | Easy to add new offer types, transaction categories |
| Edge Cases | 15 | Insufficient balance, invalid transfer, negative amounts |
| Patterns | 10 | Strategy for offers, clean service separation |
| Bonus | 5 | Statement formatting, cashback calculation |

---

## Hints

1. **Wallet balance**: Store as float, always check >= 0 before debit
2. **Transaction recording**: Create a transaction BEFORE modifying balance, mark success/fail
3. **Cashback**: Use a flag on the wallet (first_topup_done) to track first top-up
4. **Referral**: Both referrer and referee get the bonus; create two transactions
5. **Statement**: Store transactions in a list per wallet; filter and sort by timestamp

---

## Extension Ideas (If You Finish Early)

- Transaction rollback on failure
- Daily/monthly spending limits
- Wallet freezing (admin action, no transactions while frozen)
- P2P payment requests (request money from another user)
- Transaction categories with budget tracking
