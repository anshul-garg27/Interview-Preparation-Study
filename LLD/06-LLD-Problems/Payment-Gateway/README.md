# Payment Gateway - Low Level Design

## Problem Statement
Design a payment gateway that processes payments through multiple methods (credit card, debit card, UPI, wallet), manages the full transaction lifecycle, supports refunds, implements retry with idempotency, and sends webhook notifications.

---

## Functional Requirements
1. **Process Payments** - Credit card, debit card, UPI, wallet
2. **Transaction Lifecycle** - Initiate → Authorize → Capture → Settle (or fail at any point)
3. **Refund Handling** - Full and partial refunds
4. **Idempotency** - Same request processed only once (using idempotency key)
5. **Retry Logic** - Automatic retry on transient failures
6. **Webhook Notifications** - Notify merchants of payment events
7. **Transaction Logging** - Audit trail for every state change

## Non-Functional Requirements
- Idempotent processing (critical for financial systems)
- Atomic state transitions
- Complete audit trail
- PCI DSS compliance awareness
- Sub-second processing time
- 99.99% availability

---

## Design Patterns Used

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **State** | Transaction lifecycle (Initiated → Authorized → Captured → Settled) | Enforce valid transitions, state-specific behavior |
| **Strategy** | Payment processors (CreditCard, UPI, Wallet) | Different processing logic per method |
| **Observer** | Webhook notifications | Decouple payment events from merchant notifications |
| **Command** | Transaction operations (for undo/retry) | Encapsulate operations for retry and reversal |

### State Pattern -- Transaction Lifecycle
This is the core of the payment gateway. Each state knows:
- Which transitions are valid
- What actions to perform
- How to handle failures

### Command Pattern -- Transaction Operations
Each operation (authorize, capture, refund) is encapsulated as a command. This enables:
- **Retry**: Re-execute the same command
- **Idempotency**: Check if command was already executed
- **Audit**: Log every command execution

---

## Class Diagram

```mermaid
classDiagram
    class Transaction {
        -String id
        -String idempotency_key
        -float amount
        -String currency
        -PaymentMethod method
        -TransactionState state
        -String merchant_id
        -float refunded_amount
        -List~AuditLog~ audit_trail
        -datetime created_at
        +authorize()
        +capture()
        +settle()
        +refund(amount)
        +fail(reason)
        +get_status() String
    }

    class TransactionState {
        <<interface>>
        +authorize(txn)
        +capture(txn)
        +settle(txn)
        +refund(txn, amount)
        +fail(txn, reason)
        +get_name() String
    }

    class InitiatedState {
        +authorize(txn)
        +fail(txn, reason)
    }

    class AuthorizedState {
        +capture(txn)
        +fail(txn, reason)
    }

    class CapturedState {
        +settle(txn)
        +refund(txn, amount)
        +fail(txn, reason)
    }

    class SettledState {
        +refund(txn, amount)
    }

    class RefundedState {
        +refund(txn, amount)
    }

    class FailedState {
        +authorize(txn)
    }

    class PaymentProcessor {
        <<interface>>
        +authorize(txn) bool
        +capture(txn) bool
        +refund(txn, amount) bool
    }

    class CreditCardProcessor {
        +authorize(txn) bool
        +capture(txn) bool
        +refund(txn, amount) bool
    }

    class UPIProcessor {
        +authorize(txn) bool
        +capture(txn) bool
        +refund(txn, amount) bool
    }

    class WalletProcessor {
        +authorize(txn) bool
        +capture(txn) bool
        +refund(txn, amount) bool
    }

    class WebhookNotifier {
        <<interface>>
        +on_event(event_type, transaction)
    }

    class MerchantWebhook {
        -String url
        -String secret
        +on_event(event_type, transaction)
    }

    class AuditLog {
        -String event
        -String from_state
        -String to_state
        -datetime timestamp
        -String details
    }

    class PaymentGateway {
        -Map~String, Transaction~ transactions
        -Map~String, String~ idempotency_cache
        -Map~String, PaymentProcessor~ processors
        -List~WebhookNotifier~ webhooks
        -int max_retries
        +create_payment(amount, method, merchant_id, idempotency_key) Transaction
        +authorize(txn_id)
        +capture(txn_id)
        +settle(txn_id)
        +refund(txn_id, amount)
        +get_transaction(txn_id) Transaction
    }

    TransactionState <|.. InitiatedState
    TransactionState <|.. AuthorizedState
    TransactionState <|.. CapturedState
    TransactionState <|.. SettledState
    TransactionState <|.. RefundedState
    TransactionState <|.. FailedState
    PaymentProcessor <|.. CreditCardProcessor
    PaymentProcessor <|.. UPIProcessor
    PaymentProcessor <|.. WalletProcessor
    WebhookNotifier <|.. MerchantWebhook
    Transaction --> TransactionState
    Transaction --> AuditLog
    PaymentGateway --> Transaction
    PaymentGateway --> PaymentProcessor
    PaymentGateway --> WebhookNotifier
```

---

## Sequence Diagram - Payment Flow

```mermaid
sequenceDiagram
    participant M as Merchant
    participant PG as PaymentGateway
    participant T as Transaction
    participant P as PaymentProcessor
    participant WH as Webhook

    M->>PG: create_payment(100, "credit_card", idem_key="abc")
    PG->>PG: Check idempotency cache
    alt Already processed
        PG-->>M: Return existing transaction
    else New request
        PG->>T: new Transaction(100, credit_card)
        PG->>PG: Cache idempotency_key → txn_id
    end

    M->>PG: authorize(txn_id)
    PG->>P: authorize(txn) [CreditCardProcessor]
    P-->>PG: success
    PG->>T: state = AuthorizedState
    PG->>T: add_audit_log("authorized")
    PG->>WH: on_event("payment.authorized", txn)
    WH-->>M: POST webhook

    M->>PG: capture(txn_id)
    PG->>P: capture(txn)
    P-->>PG: success
    PG->>T: state = CapturedState
    PG->>WH: on_event("payment.captured", txn)

    M->>PG: settle(txn_id)
    PG->>T: state = SettledState
    PG->>WH: on_event("payment.settled", txn)
    WH-->>M: POST webhook
```

## Sequence Diagram - Transaction State Machine

```mermaid
stateDiagram-v2
    [*] --> Initiated
    Initiated --> Authorized : authorize success
    Initiated --> Failed : authorize failed
    Authorized --> Captured : capture success
    Authorized --> Failed : capture failed
    Captured --> Settled : settle
    Captured --> Refunded : full refund
    Captured --> PartialRefund : partial refund
    Settled --> Refunded : full refund
    Settled --> PartialRefund : partial refund
    PartialRefund --> Refunded : remaining refunded
    Failed --> Authorized : retry authorize
    Refunded --> [*]
    Failed --> [*]
```

## Sequence Diagram - Retry with Idempotency

```mermaid
sequenceDiagram
    participant M as Merchant
    participant PG as PaymentGateway
    participant P as Processor

    M->>PG: authorize(txn, idem_key="xyz")
    PG->>P: authorize()
    Note over P: Network timeout
    P--xPG: timeout

    Note over PG: Retry attempt 1 (1s delay)
    PG->>P: authorize() [same idem_key]
    P-->>PG: success
    PG-->>M: authorized

    Note over M: Client retries same request
    M->>PG: authorize(txn, idem_key="xyz")
    PG->>PG: idem_key "xyz" found in cache
    PG-->>M: Return cached result (no re-processing)
```

---

## Edge Cases
1. **Duplicate payment** - Idempotency key prevents double charge
2. **Partial capture** - Capture less than authorized amount
3. **Refund > captured amount** - Reject with clear error
4. **Multiple partial refunds** - Track cumulative refunded amount
5. **Processor timeout** - Retry with exponential backoff
6. **State race condition** - Lock transaction before state transition
7. **Webhook delivery failure** - Queue and retry with backoff
8. **Currency mismatch** - Validate at payment creation
9. **Expired authorization** - Auth typically expires in 7 days
10. **Void vs Refund** - Void if not captured, refund if captured

## Extensions
- 3D Secure authentication
- Multi-currency support
- Subscription/recurring payments
- Payout to merchants (settlement cycle)
- Fraud detection (velocity checks, blacklists)
- PCI DSS tokenization (store tokens, not card numbers)
- Payment links and hosted checkout
- Dispute/chargeback management

---

## Interview Tips

1. **Lead with the state machine** - Draw the state diagram immediately; this is the core
2. **Emphasize idempotency** - Critical for financial systems; show the idempotency key mechanism
3. **Discuss two-phase capture** - Auth + Capture is standard (hotels, gas stations pre-auth more)
4. **Mention retry strategy** - Exponential backoff with max retries
5. **Audit trail** - Every state change must be logged; show the AuditLog class
6. **Security** - Never store raw card numbers, use tokenization
7. **Common follow-up**: "How to handle distributed transactions?" - Saga pattern, eventual consistency
8. **Common follow-up**: "How to ensure exactly-once processing?" - Idempotency keys + database transactions
