"""Online Shopping System - Full Demo: browse, cart, checkout, pay, track."""

from enums import ProductCategory, PaymentMethod, OrderStatus
from product import Product
from customer import Customer
from seller import Seller
from catalog import ProductCatalog
from order_service import OrderService


def main():
    print("=" * 70)
    print("  ONLINE SHOPPING SYSTEM - Modular LLD Demo")
    print("=" * 70)

    catalog = ProductCatalog()
    order_svc = OrderService()

    # 1. Add products
    products = [
        Product("P1", "MacBook Pro 14", 1999.99, ProductCategory.ELECTRONICS, "Apple", 5),
        Product("P2", "iPhone 15 Pro", 999.99, ProductCategory.ELECTRONICS, "Apple", 10),
        Product("P3", "Galaxy S24 Ultra", 1199.99, ProductCategory.ELECTRONICS, "Samsung", 8),
        Product("P4", "Running Shoes", 129.99, ProductCategory.SPORTS, "Nike", 20),
        Product("P5", "Yoga Mat", 49.99, ProductCategory.SPORTS, "Adidas", 30),
        Product("P6", "Clean Code", 39.99, ProductCategory.BOOKS, "Pearson", 15),
        Product("P7", "Design Patterns", 44.99, ProductCategory.BOOKS, "O'Reilly", 12),
        Product("P8", "Cotton T-Shirt", 24.99, ProductCategory.CLOTHING, "Uniqlo", 50),
        Product("P9", "Instant Pot", 89.99, ProductCategory.HOME, "Instant", 7),
        Product("P10", "Air Purifier", 249.99, ProductCategory.HOME, "Dyson", 3),
    ]
    for p in products:
        p.add_review(4.0 + (hash(p.name) % 10) / 10.0)
        catalog.add_product(p)

    catalog.display()

    # 2. Register users
    alice = Customer("U1", "Alice", "alice@email.com", "123 Main St")
    bob = Customer("U2", "Bob", "bob@email.com", "456 Oak Ave")
    seller = Seller("S1", "TechStore", "tech@store.com", "TechStore Inc")

    # 3. Search & Browse
    print("\n  [Search: 'Electronics' category, price $500-$1500]")
    for p in catalog.search(category=ProductCategory.ELECTRONICS, min_price=500, max_price=1500):
        print(f"    {p}")

    print("\n  [Search: keyword 'book']")
    for p in catalog.search(keyword="book"):
        print(f"    {p}")

    print("\n  [Search: brand 'Apple']")
    for p in catalog.search(brand="Apple"):
        print(f"    {p}")

    # 4. Alice's shopping flow
    print(f"\n{'='*70}")
    print("  ALICE'S SHOPPING FLOW")
    print(f"{'='*70}")

    print("\n  Alice browses and adds to cart:")
    alice.cart.add_item(products[1], 1)  # iPhone
    alice.cart.add_item(products[5], 2)  # 2x Clean Code
    alice.cart.add_item(products[3], 1)  # Running Shoes
    alice.cart.display()

    print("\n  Alice removes Running Shoes:")
    alice.cart.remove_item("P4")
    alice.cart.display()

    order1 = order_svc.checkout(alice, PaymentMethod.CREDIT_CARD)
    if order1:
        order_svc.process_order(order1)
        order1.display_tracking()

    # 5. Bob's shopping flow
    print(f"\n{'='*70}")
    print("  BOB'S SHOPPING FLOW")
    print(f"{'='*70}")

    bob.cart.add_item(products[0], 1)  # MacBook
    bob.cart.add_item(products[8], 1)  # Instant Pot
    bob.cart.add_item(products[4], 2)  # 2x Yoga Mats

    order2 = order_svc.checkout(bob, PaymentMethod.UPI)
    if order2:
        order_svc.process_order(order2)
        order2.display_tracking()

    # 6. Alice second order with COD, then cancels
    print(f"\n{'='*70}")
    print("  ALICE'S SECOND ORDER (COD) -> CANCELLED")
    print(f"{'='*70}")

    alice.cart.add_item(products[7], 3)  # 3x T-Shirts
    alice.cart.add_item(products[6], 1)  # Design Patterns
    order3 = order_svc.checkout(alice, PaymentMethod.COD)
    if order3:
        order3.update_status(OrderStatus.CONFIRMED)
        order3.update_status(OrderStatus.CANCELLED)
        order3.display_tracking()

    # 7. Edge cases
    print(f"\n{'='*70}")
    print("  EDGE CASES")
    print(f"{'='*70}")
    if order1:
        order1.update_status(OrderStatus.SHIPPED)  # Invalid transition
    order_svc.checkout(alice, PaymentMethod.WALLET)  # Empty cart

    # 8. Summary
    print(f"\n{'='*70}")
    print("  ORDER SUMMARY")
    print(f"{'='*70}")
    for order in order_svc.all_orders:
        print(f"    {order}")

    print(f"\n  Alice's Orders ({len(alice.order_history)}):")
    for o in alice.order_history:
        print(f"    {o}")

    print(f"\n  Bob's Orders ({len(bob.order_history)}):")
    for o in bob.order_history:
        print(f"    {o}")

    print("\n  Updated Stock:")
    for pid in ["P2", "P6", "P1", "P9"]:
        p = catalog.products[pid]
        print(f"    {p.name}: {p.stock} remaining")

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
