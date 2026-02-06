"""Enums for the Online Shopping System."""

from enum import Enum


class OrderStatus(Enum):
    """State machine for order lifecycle."""
    PLACED = "Placed"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"


class PaymentMethod(Enum):
    """Supported payment methods."""
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    UPI = "UPI"
    WALLET = "Wallet"
    COD = "Cash on Delivery"


class ProductCategory(Enum):
    """Product categories in the catalog."""
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    BOOKS = "Books"
    HOME = "Home & Kitchen"
    SPORTS = "Sports"
