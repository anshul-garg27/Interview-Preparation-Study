"""
Payment Gateway - Low Level Design
Run: python payment_gateway.py

Patterns: State (transaction lifecycle), Strategy (payment processors),
          Observer (webhooks), Command (transaction operations)
Key: Transaction state machine, idempotency, retry logic
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import time
import uuid
import random


# ─── Enums ───────────────────────────────────────────────────────────
class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    WALLET = "wallet"


# ─── Audit Log ───────────────────────────────────────────────────────
class AuditLog:
    def __init__(self, event: str, from_state: str, to_state: str,
                 details: str = ""):
        self.event = event
        self.from_state = from_state
        self.to_state = to_state
        self.timestamp = datetime.now()
        self.details = details

    def __repr__(self):
        return (f"  [{self.timestamp.strftime('%H:%M:%S')}] "
                f"{self.event}: {self.from_state} -> {self.to_state}"
                f"{' (' + self.details + ')' if self.details else ''}")


# ─── State Pattern: Transaction States ───────────────────────────────
class TransactionState(ABC):
    @abstractmethod
    def get_name(self) -> str: pass

    def authorize(self, txn: "Transaction"):
        raise ValueError(f"Cannot authorize from {self.get_name()}")

    def capture(self, txn: "Transaction"):
        raise ValueError(f"Cannot capture from {self.get_name()}")

    def settle(self, txn: "Transaction"):
        raise ValueError(f"Cannot settle from {self.get_name()}")

    def refund(self, txn: "Transaction", amount: float):
        raise ValueError(f"Cannot refund from {self.get_name()}")

    def fail(self, txn: "Transaction", reason: str):
        raise ValueError(f"Cannot fail from {self.get_name()}")


class InitiatedState(TransactionState):
    def get_name(self): return "INITIATED"

    def authorize(self, txn):
        txn._set_state(AuthorizedState(), "authorize")

    def fail(self, txn, reason):
        txn._set_state(FailedState(reason), "fail", reason)


class AuthorizedState(TransactionState):
    def get_name(self): return "AUTHORIZED"

    def capture(self, txn):
        txn._set_state(CapturedState(), "capture")

    def fail(self, txn, reason):
        txn._set_state(FailedState(reason), "fail", reason)


class CapturedState(TransactionState):
    def get_name(self): return "CAPTURED"

    def settle(self, txn):
        txn._set_state(SettledState(), "settle")

    def refund(self, txn, amount):
        txn._process_refund(amount)

    def fail(self, txn, reason):
        txn._set_state(FailedState(reason), "fail", reason)


class SettledState(TransactionState):
    def get_name(self): return "SETTLED"

    def refund(self, txn, amount):
        txn._process_refund(amount)


class RefundedState(TransactionState):
    def get_name(self): return "REFUNDED"

    def refund(self, txn, amount):
        # Allow additional partial refunds
        txn._process_refund(amount)


class FailedState(TransactionState):
    def __init__(self, reason: str = ""):
        self.reason = reason

    def get_name(self): return f"FAILED"

    def authorize(self, txn):
        """Allow retry of failed auth."""
        txn._set_state(AuthorizedState(), "retry_authorize")


# ─── Transaction ─────────────────────────────────────────────────────
class Transaction:
    def __init__(self, amount: float, method: PaymentMethod,
                 merchant_id: str, idempotency_key: str = None):
        self.id = "TXN-" + str(uuid.uuid4())[:8]
        self.idempotency_key = idempotency_key or str(uuid.uuid4())
        self.amount = amount
        self.currency = "USD"
        self.method = method
        self.merchant_id = merchant_id
        self.state: TransactionState = InitiatedState()
        self.refunded_amount = 0.0
        self.audit_trail: list[AuditLog] = []
        self.created_at = datetime.now()
        self.failure_reason = ""

        self.audit_trail.append(
            AuditLog("created", "-", "INITIATED",
                     f"${amount} via {method.value}"))

    def _set_state(self, new_state: TransactionState, event: str,
                   details: str = ""):
        old_name = self.state.get_name()
        self.state = new_state
        self.audit_trail.append(AuditLog(event, old_name, new_state.get_name(),
                                         details))

    def _process_refund(self, amount: float):
        remaining = self.amount - self.refunded_amount
        if amount > remaining:
            raise ValueError(
                f"Refund ${amount} exceeds remaining ${remaining:.2f}")
        self.refunded_amount += amount
        if self.refunded_amount >= self.amount:
            self._set_state(RefundedState(), "full_refund",
                           f"${amount:.2f}")
        else:
            self._set_state(RefundedState(), "partial_refund",
                           f"${amount:.2f} (total refunded: "
                           f"${self.refunded_amount:.2f})")

    @property
    def status(self) -> str:
        return self.state.get_name()


# ─── Strategy: Payment Processors ────────────────────────────────────
class PaymentProcessor(ABC):
    @abstractmethod
    def authorize(self, txn: Transaction) -> bool:
        pass

    @abstractmethod
    def capture(self, txn: Transaction) -> bool:
        pass

    @abstractmethod
    def refund(self, txn: Transaction, amount: float) -> bool:
        pass


class CreditCardProcessor(PaymentProcessor):
    def authorize(self, txn):
        print(f"    [CC] Authorizing ${txn.amount}...")
        return random.random() > 0.1  # 90% success

    def capture(self, txn):
        print(f"    [CC] Capturing ${txn.amount}...")
        return True

    def refund(self, txn, amount):
        print(f"    [CC] Refunding ${amount:.2f}...")
        return True


class UPIProcessor(PaymentProcessor):
    def authorize(self, txn):
        print(f"    [UPI] Authorizing ${txn.amount}...")
        return random.random() > 0.05

    def capture(self, txn):
        print(f"    [UPI] Instant capture ${txn.amount}...")
        return True

    def refund(self, txn, amount):
        print(f"    [UPI] Refunding ${amount:.2f}...")
        return True


class WalletProcessor(PaymentProcessor):
    def authorize(self, txn):
        print(f"    [Wallet] Checking balance for ${txn.amount}...")
        return True

    def capture(self, txn):
        print(f"    [Wallet] Deducting ${txn.amount}...")
        return True

    def refund(self, txn, amount):
        print(f"    [Wallet] Adding ${amount:.2f} back to wallet...")
        return True


# ─── Observer: Webhooks ──────────────────────────────────────────────
class WebhookNotifier(ABC):
    @abstractmethod
    def on_event(self, event: str, txn: Transaction):
        pass


class MerchantWebhook(WebhookNotifier):
    def __init__(self, merchant_id: str, url: str):
        self.merchant_id = merchant_id
        self.url = url

    def on_event(self, event: str, txn: Transaction):
        if txn.merchant_id == self.merchant_id:
            print(f"    [Webhook -> {self.url}] {event}: "
                  f"txn={txn.id}, status={txn.status}, "
                  f"amount=${txn.amount}")


# ─── Payment Gateway (Facade) ───────────────────────────────────────
class PaymentGateway:
    def __init__(self, max_retries: int = 3):
        self.transactions: dict[str, Transaction] = {}
        self.idempotency_cache: dict[str, str] = {}
        self.processors: dict[PaymentMethod, PaymentProcessor] = {
            PaymentMethod.CREDIT_CARD: CreditCardProcessor(),
            PaymentMethod.DEBIT_CARD: CreditCardProcessor(),  # same processor
            PaymentMethod.UPI: UPIProcessor(),
            PaymentMethod.WALLET: WalletProcessor(),
        }
        self.webhooks: list[WebhookNotifier] = []
        self.max_retries = max_retries

    def register_webhook(self, webhook: WebhookNotifier):
        self.webhooks.append(webhook)

    def create_payment(self, amount: float, method: PaymentMethod,
                       merchant_id: str,
                       idempotency_key: str = None) -> Transaction:
        # Idempotency check
        if idempotency_key and idempotency_key in self.idempotency_cache:
            existing_id = self.idempotency_cache[idempotency_key]
            print(f"    [Idempotency] Returning cached txn {existing_id}")
            return self.transactions[existing_id]

        txn = Transaction(amount, method, merchant_id, idempotency_key)
        self.transactions[txn.id] = txn
        if idempotency_key:
            self.idempotency_cache[idempotency_key] = txn.id
        self._notify("payment.created", txn)
        return txn

    def authorize(self, txn_id: str) -> bool:
        txn = self.transactions[txn_id]
        processor = self.processors[txn.method]

        # Retry logic with exponential backoff
        for attempt in range(self.max_retries):
            success = processor.authorize(txn)
            if success:
                txn.state.authorize(txn)
                self._notify("payment.authorized", txn)
                return True
            if attempt < self.max_retries - 1:
                wait = 0.1 * (2 ** attempt)  # exponential backoff
                print(f"    [Retry] Attempt {attempt + 2} in {wait:.1f}s...")
                time.sleep(wait)

        txn.state.fail(txn, "Authorization failed after retries")
        self._notify("payment.failed", txn)
        return False

    def capture(self, txn_id: str) -> bool:
        txn = self.transactions[txn_id]
        processor = self.processors[txn.method]
        if processor.capture(txn):
            txn.state.capture(txn)
            self._notify("payment.captured", txn)
            return True
        txn.state.fail(txn, "Capture failed")
        return False

    def settle(self, txn_id: str):
        txn = self.transactions[txn_id]
        txn.state.settle(txn)
        self._notify("payment.settled", txn)

    def refund(self, txn_id: str, amount: float = None):
        txn = self.transactions[txn_id]
        refund_amount = amount or txn.amount
        processor = self.processors[txn.method]
        if processor.refund(txn, refund_amount):
            txn.state.refund(txn, refund_amount)
            self._notify("payment.refunded", txn)
            return True
        return False

    def _notify(self, event: str, txn: Transaction):
        for wh in self.webhooks:
            wh.on_event(event, txn)

    def print_audit(self, txn_id: str):
        txn = self.transactions[txn_id]
        print(f"\n  Audit Trail for {txn.id}:")
        for log in txn.audit_trail:
            print(f"  {log}")


# ─── Demo ────────────────────────────────────────────────────────────
def main():
    random.seed(42)  # deterministic demo
    gw = PaymentGateway(max_retries=3)
    gw.register_webhook(MerchantWebhook("merchant_1", "https://shop.com/webhook"))

    # ── 1. Full Payment Lifecycle (Credit Card) ──
    print("=" * 60)
    print("1. FULL PAYMENT LIFECYCLE (Credit Card)")
    print("=" * 60)
    txn = gw.create_payment(99.99, PaymentMethod.CREDIT_CARD,
                             "merchant_1", idempotency_key="order-001")
    print(f"  Created: {txn.id} | ${txn.amount} | {txn.status}")

    gw.authorize(txn.id)
    print(f"  Status: {txn.status}")

    gw.capture(txn.id)
    print(f"  Status: {txn.status}")

    gw.settle(txn.id)
    print(f"  Status: {txn.status}")

    gw.print_audit(txn.id)

    # ── 2. Idempotency ──
    print(f"\n{'=' * 60}")
    print("2. IDEMPOTENCY (duplicate request)")
    print("=" * 60)
    txn_dup = gw.create_payment(99.99, PaymentMethod.CREDIT_CARD,
                                 "merchant_1", idempotency_key="order-001")
    print(f"  Same transaction? {txn.id == txn_dup.id}")

    # ── 3. UPI Payment ──
    print(f"\n{'=' * 60}")
    print("3. UPI PAYMENT")
    print("=" * 60)
    txn2 = gw.create_payment(49.99, PaymentMethod.UPI, "merchant_1")
    gw.authorize(txn2.id)
    gw.capture(txn2.id)
    gw.settle(txn2.id)
    print(f"  Final status: {txn2.status}")

    # ── 4. Partial Refund ──
    print(f"\n{'=' * 60}")
    print("4. PARTIAL REFUND")
    print("=" * 60)
    txn3 = gw.create_payment(200.00, PaymentMethod.WALLET, "merchant_1")
    gw.authorize(txn3.id)
    gw.capture(txn3.id)
    print(f"  Before refund: {txn3.status}")

    gw.refund(txn3.id, 50.00)
    print(f"  After $50 refund: {txn3.status} "
          f"(refunded: ${txn3.refunded_amount:.2f})")

    gw.refund(txn3.id, 150.00)
    print(f"  After $150 refund: {txn3.status} "
          f"(refunded: ${txn3.refunded_amount:.2f})")

    gw.print_audit(txn3.id)

    # ── 5. Over-refund Prevention ──
    print(f"\n{'=' * 60}")
    print("5. OVER-REFUND PREVENTION")
    print("=" * 60)
    try:
        gw.refund(txn3.id, 10.00)  # already fully refunded
    except ValueError as e:
        print(f"  Caught: {e}")

    # ── 6. Invalid State Transitions ──
    print(f"\n{'=' * 60}")
    print("6. INVALID STATE TRANSITIONS")
    print("=" * 60)
    txn4 = gw.create_payment(30.00, PaymentMethod.CREDIT_CARD, "merchant_1")
    # Try to capture before authorize
    try:
        gw.capture(txn4.id)
    except ValueError as e:
        print(f"  Capture before auth: {e}")

    # Try to settle before capture
    gw.authorize(txn4.id)
    try:
        gw.settle(txn4.id)
    except ValueError as e:
        print(f"  Settle before capture: {e}")

    # ── 7. Retry Logic (with seed showing retry) ──
    print(f"\n{'=' * 60}")
    print("7. RETRY WITH EXPONENTIAL BACKOFF")
    print("=" * 60)
    random.seed(99)  # seed that causes initial failure
    txn5 = gw.create_payment(75.00, PaymentMethod.CREDIT_CARD, "merchant_1")
    result = gw.authorize(txn5.id)
    print(f"  Auth result: {'Success' if result else 'Failed'}")
    print(f"  Status: {txn5.status}")

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print("PATTERN SUMMARY")
    print("=" * 60)
    patterns = [
        ("State", "Transaction: INITIATED -> AUTHORIZED -> CAPTURED -> SETTLED"),
        ("Strategy", "Processors: CreditCard, UPI, Wallet"),
        ("Observer", "Webhook notifications on every state change"),
        ("Command", "Retry authorize operation with exponential backoff"),
    ]
    for name, usage in patterns:
        print(f"  {name:20s} | {usage}")


if __name__ == "__main__":
    main()
