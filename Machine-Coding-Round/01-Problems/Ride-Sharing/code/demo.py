"""Full simulation demonstrating the Ride-Sharing system.

Run: cd code/ && python demo.py
"""

from enums import VehicleType
from location import Location
from vehicle import Vehicle
from ride_service import RideService


def print_separator(title: str = "") -> None:
    """Print a formatted section separator."""
    print()
    if title:
        print(f"{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print("-" * 60)


def print_ride_history(name: str, rides: list) -> None:
    """Print ride history for a user."""
    print(f"\n  {name}'s Ride History:")
    if not rides:
        print("    (No rides yet)")
        return
    for ride in rides:
        vehicle_type = ride.driver.vehicle.vehicle_type.value if ride.driver else "N/A"
        print(
            f"    Ride {ride.ride_id} | {vehicle_type} | "
            f"Rs {ride.fare:.2f} | {ride.status.value}"
        )


def main() -> None:
    """Run the ride-sharing system simulation."""
    # Reset singleton for clean run
    RideService.reset()
    service = RideService()

    print_separator("RIDE-SHARING SYSTEM SIMULATION")

    # ---- Register Drivers ----
    print("\n--- Registering Drivers ---")

    v1 = Vehicle(VehicleType.AUTO, "Bajaj", "RE", "KA01AB1234")
    d1 = service.register_driver("Amit", "9000000001", v1, Location(12.9716, 77.5946))
    print(f"  [+] Driver registered: {d1.name} ({v1})")

    v2 = Vehicle(VehicleType.MINI, "Maruti", "Swift", "KA01CD5678")
    d2 = service.register_driver("Priya", "9000000002", v2, Location(12.9750, 77.5900))
    print(f"  [+] Driver registered: {d2.name} ({v2})")

    v3 = Vehicle(VehicleType.SEDAN, "Honda", "City", "KA01EF9012")
    d3 = service.register_driver("Ravi", "9000000003", v3, Location(12.9800, 77.6000))
    print(f"  [+] Driver registered: {d3.name} ({v3})")

    # ---- Register Riders ----
    print("\n--- Registering Riders ---")

    r1 = service.register_rider("John", "9876543210", Location(12.9720, 77.5950))
    print(f"  [+] Rider registered: {r1.name} (Phone: {r1.phone})")

    r2 = service.register_rider("Jane", "9876543211", Location(12.9700, 77.5930))
    print(f"  [+] Rider registered: {r2.name} (Phone: {r2.phone})")

    # ---- Ride 1: John requests a Mini ride ----
    print_separator()
    print("--- John Requests a MINI Ride ---")

    source1 = Location(12.9720, 77.5950)
    dest1 = Location(12.9350, 77.6200)

    ride1 = service.request_ride(r1, source1, dest1, VehicleType.MINI)
    print(f"  [*] Nearest driver matched: {ride1.driver.name}")
    dist1 = source1.distance_to(ride1.driver.location)
    print(f"  [*] Driver is {dist1:.2f} km away")
    print(f"  [*] Ride {ride1.ride_id} created: {ride1.status.value}")
    print(f"  [*] Distance: {ride1.distance:.2f} km")
    print(f"  [*] Fare estimate: Rs {ride1.fare:.2f}")

    # Driver accepts
    print(f"\n--- Driver {ride1.driver.name} Accepts the Ride ---")
    service.accept_ride(ride1)
    print(f"  [*] Ride {ride1.ride_id}: REQUESTED -> {ride1.status.value}")

    # Ride starts
    print("\n--- Ride Starts ---")
    service.start_ride(ride1)
    print(f"  [*] Ride {ride1.ride_id}: ACCEPTED -> {ride1.status.value}")

    # Ride completes
    print("\n--- Ride Completed ---")
    service.complete_ride(ride1)
    print(f"  [*] Ride {ride1.ride_id}: IN_PROGRESS -> {ride1.status.value}")
    print(f"  [*] Final fare: Rs {ride1.fare:.2f}")

    # Ratings
    print("\n--- Rating ---")
    service.rate_driver(ride1, 5)
    print(f"  [*] {r1.name} rates {ride1.driver.name}: 5 stars")
    service.rate_rider(ride1, 4)
    print(f"  [*] {ride1.driver.name} rates {r1.name}: 4 stars")
    print(f"  [*] {ride1.driver.name}'s average rating: {ride1.driver.average_rating}")
    print(f"  [*] {r1.name}'s average rating: {r1.average_rating}")

    # ---- Ride 2: Jane requests an Auto ride ----
    print_separator()
    print("--- Jane Requests an AUTO Ride ---")

    source2 = Location(12.9700, 77.5930)
    dest2 = Location(12.9500, 77.5800)

    ride2 = service.request_ride(r2, source2, dest2, VehicleType.AUTO)
    print(f"  [*] Nearest driver matched: {ride2.driver.name}")
    dist2 = source2.distance_to(ride2.driver.location)
    print(f"  [*] Driver is {dist2:.2f} km away")
    print(f"  [*] Ride {ride2.ride_id} created: {ride2.status.value}")
    print(f"  [*] Distance: {ride2.distance:.2f} km")
    print(f"  [*] Fare estimate: Rs {ride2.fare:.2f}")

    # Full lifecycle
    service.accept_ride(ride2)
    print(f"\n  [*] Ride accepted by {ride2.driver.name}")
    service.start_ride(ride2)
    print(f"  [*] Ride started")
    service.complete_ride(ride2)
    print(f"  [*] Ride completed! Fare: Rs {ride2.fare:.2f}")

    service.rate_driver(ride2, 4)
    service.rate_rider(ride2, 5)
    print(f"  [*] Jane rated driver 4 stars, driver rated Jane 5 stars")

    # ---- Ride 3: John requests a Sedan ride ----
    print_separator()
    print("--- John Requests a SEDAN Ride ---")

    source3 = Location(12.9350, 77.6200)
    dest3 = Location(12.9100, 77.6400)

    ride3 = service.request_ride(r1, source3, dest3, VehicleType.SEDAN)
    print(f"  [*] Nearest driver matched: {ride3.driver.name}")
    print(f"  [*] Ride {ride3.ride_id}: {ride3.status.value}")
    print(f"  [*] Distance: {ride3.distance:.2f} km")
    print(f"  [*] Fare: Rs {ride3.fare:.2f}")

    service.accept_ride(ride3)
    service.start_ride(ride3)
    service.complete_ride(ride3)
    print(f"  [*] Ride completed! Final fare: Rs {ride3.fare:.2f}")

    service.rate_driver(ride3, 5)
    service.rate_rider(ride3, 4)

    # ---- Ride History ----
    print_separator()
    print("--- Ride History ---")
    print_ride_history("John", service.get_ride_history(r1))
    print_ride_history("Jane", service.get_ride_history(r2))

    # ---- Driver Stats ----
    print("\n--- Driver Ratings ---")
    for driver in [d1, d2, d3]:
        rides_done = len([r for r in driver.ride_history])
        print(
            f"  {driver.name} ({driver.vehicle.vehicle_type.value}): "
            f"Rating {driver.average_rating}/5.0 | Rides: {rides_done}"
        )

    # ---- Error Handling Demo ----
    print_separator()
    print("--- Error Handling Demos ---")

    # Try to complete an already completed ride
    try:
        service.complete_ride(ride1)
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Try to rate outside range
    try:
        service.rate_driver(ride3, 7)
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Try cancel a completed ride
    try:
        service.cancel_ride(ride1)
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # ---- Cancel Demo ----
    print("\n--- Cancellation Demo ---")
    r1.ride_history.clear()  # Clear history to allow new ride request
    source4 = Location(12.9100, 77.6400)
    dest4 = Location(12.8900, 77.6600)
    # Re-enable Priya for this demo
    d2.is_available = True
    ride4 = service.request_ride(r1, source4, dest4, VehicleType.MINI)
    print(f"  [*] Ride {ride4.ride_id} requested")
    service.accept_ride(ride4)
    print(f"  [*] Ride accepted")
    service.cancel_ride(ride4)
    print(f"  [*] Ride cancelled! Status: {ride4.status.value}")
    print(f"  [*] Driver {ride4.driver.name} is now available: {ride4.driver.is_available}")

    print_separator("SIMULATION COMPLETE")
    print()


if __name__ == "__main__":
    main()
