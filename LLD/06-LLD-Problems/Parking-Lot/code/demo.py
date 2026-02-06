"""
Parking Lot System - Demo
==========================
Demonstrates: Singleton, Strategy (Payment), Observer (DisplayBoard),
vehicle entry/exit, fee calculation, and concurrent access.

Run: cd code/ && python demo.py
"""

import threading

from enums import SpotType
from car import Car
from bike import Bike
from truck import Truck
from parking_floor import ParkingFloor
from parking_lot import ParkingLot
from payment import CreditCardPayment, CashPayment, UPIPayment


def demo_concurrent_entry(lot: ParkingLot, vehicles: list) -> None:
    """Simulate concurrent vehicle entry using threads."""
    threads = [threading.Thread(target=lot.enter, args=(v,)) for v in vehicles]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    print("=" * 60)
    print("  PARKING LOT SYSTEM - Modular LLD Demo")
    print("=" * 60)

    # Reset singleton for clean demo
    ParkingLot._instance = None

    # 1. Create parking lot (Singleton)
    lot = ParkingLot("City Center Parking")
    lot.add_floor(ParkingFloor(1, {SpotType.COMPACT: 3, SpotType.REGULAR: 3, SpotType.LARGE: 2}))
    lot.add_floor(ParkingFloor(2, {SpotType.COMPACT: 2, SpotType.REGULAR: 4, SpotType.LARGE: 1}))
    lot.add_floor(ParkingFloor(3, {SpotType.COMPACT: 2, SpotType.REGULAR: 2, SpotType.LARGE: 2}))

    # Verify Singleton
    lot2 = ParkingLot()
    print(f"\nSingleton check: lot is lot2 -> {lot is lot2}")

    # 2. Show initial availability
    lot.display_availability()

    # 3. Vehicles enter (using concrete subclasses)
    print("\n--- Vehicles Entering ---")
    vehicles = [
        Bike("KA-01-1234"),
        Car("KA-02-5678"),
        Truck("KA-03-9999"),
        Car("KA-04-1111"),
        Bike("KA-05-2222"),
        Car("KA-06-3333"),
        Truck("KA-07-4444"),
    ]
    demo_concurrent_entry(lot, vehicles)

    # 4. Try duplicate entry
    print("\n--- Duplicate Entry Attempt ---")
    lot.enter(Bike("KA-01-1234"))

    # 5. Show availability after parking
    lot.display_availability()

    # 6. Pay and exit with different strategies
    print("\n--- Payments & Exits ---")
    lot.pay_and_exit("KA-01-1234", CashPayment(), simulated_hours=2)
    lot.pay_and_exit("KA-02-5678", CreditCardPayment("4111222233334444"), simulated_hours=5)
    lot.pay_and_exit("KA-03-9999", UPIPayment("user@upi"), simulated_hours=3)

    # 7. Show availability after some exits
    lot.display_availability()

    # 8. New vehicle enters freed spot
    print("\n--- New Vehicle Enters Freed Spot ---")
    lot.enter(Car("KA-08-7777"))

    # 9. Exit remaining vehicles
    print("\n--- Remaining Exits ---")
    lot.pay_and_exit("KA-04-1111", CreditCardPayment("5555666677778888"), simulated_hours=1)
    lot.pay_and_exit("KA-05-2222", CashPayment(), simulated_hours=4)
    lot.pay_and_exit("KA-06-3333", UPIPayment("driver@upi"), simulated_hours=2)
    lot.pay_and_exit("KA-07-4444", CashPayment(), simulated_hours=6)
    lot.pay_and_exit("KA-08-7777", CreditCardPayment("9999000011112222"), simulated_hours=1)

    # 10. Final availability
    lot.display_availability()
    print("\nDemo complete!")
