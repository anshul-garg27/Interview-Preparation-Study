"""Offer service - cashback and referral bonuses."""

from enums import TransactionCategory


class OfferService:
    """Manages offers: first top-up cashback, referral bonuses."""

    FIRST_TOPUP_CASHBACK_PERCENT = 10
    FIRST_TOPUP_MAX_CASHBACK = 100.0
    REFERRAL_BONUS_AMOUNT = 50.0

    def __init__(self, transaction_service):
        self._txn_service = transaction_service
        self._offers_applied = {}  # user_id -> [offer descriptions]

    def apply_first_topup_cashback(self, user_id, topup_amount):
        """
        Apply first top-up cashback (10% up to max 100).
        Returns the cashback amount, or 0 if not applicable.
        """
        user = self._txn_service.get_user(user_id)
        if not user:
            return 0

        cashback = min(
            topup_amount * self.FIRST_TOPUP_CASHBACK_PERCENT / 100,
            self.FIRST_TOPUP_MAX_CASHBACK
        )

        self._txn_service.credit_to_wallet(
            user.wallet, cashback, TransactionCategory.CASHBACK,
            f"First top-up cashback ({self.FIRST_TOPUP_CASHBACK_PERCENT}%)"
        )

        self._record_offer(user_id, f"First top-up cashback: {cashback:.2f}")

        print(f"[CASHBACK] First top-up bonus: {cashback:.2f} credited to "
              f"{user.name}'s wallet")
        return cashback

    def apply_referral_bonus(self, referrer_id, referee_id):
        """
        Apply referral bonus to both referrer and referee.
        Both get REFERRAL_BONUS_AMOUNT.
        """
        referrer = self._txn_service.get_user(referrer_id)
        referee = self._txn_service.get_user(referee_id)

        if not referrer:
            print(f"[ERROR] Referrer '{referrer_id}' not found")
            return False
        if not referee:
            print(f"[ERROR] Referee '{referee_id}' not found")
            return False
        if referrer_id == referee_id:
            print("[ERROR] Cannot refer yourself")
            return False

        bonus = self.REFERRAL_BONUS_AMOUNT

        # Credit referrer
        self._txn_service.credit_to_wallet(
            referrer.wallet, bonus, TransactionCategory.REFERRAL_BONUS,
            f"Referral bonus for inviting {referee.name}"
        )

        # Credit referee
        self._txn_service.credit_to_wallet(
            referee.wallet, bonus, TransactionCategory.REFERRAL_BONUS,
            f"Referral bonus from {referrer.name}"
        )

        self._record_offer(referrer_id, f"Referral bonus (referred {referee.name}): {bonus:.2f}")
        self._record_offer(referee_id, f"Referral bonus (from {referrer.name}): {bonus:.2f}")

        print(f"[REFERRAL] Both {referrer.name} and {referee.name} received "
              f"{bonus:.2f} referral bonus")
        return True

    def get_offers_for_user(self, user_id):
        """Get all offers applied to a user."""
        return self._offers_applied.get(user_id, [])

    def display_offers(self, user_id):
        """Display all offers for a user."""
        user = self._txn_service.get_user(user_id)
        if not user:
            print(f"[ERROR] User '{user_id}' not found")
            return

        offers = self.get_offers_for_user(user_id)
        print(f"\n  Offers Applied: {user.name}")
        print(f"  {'-' * 45}")
        if not offers:
            print("  (no offers applied)")
        else:
            for i, offer in enumerate(offers, 1):
                print(f"  {i}. {offer}")
        print(f"  {'-' * 45}")

    def _record_offer(self, user_id, description):
        if user_id not in self._offers_applied:
            self._offers_applied[user_id] = []
        self._offers_applied[user_id].append(description)
