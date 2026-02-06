"""Cab Booking System - Full Demo with multiple ride scenarios."""

from enums import VehicleType
from location import Location
from vehicle import Vehicle
from driver import Driver
from rider import Rider
from ride_service import RideService
from rating import RatingService


def main():
    print("=" * 65)
    print("  CAB BOOKING SYSTEM - Modular LLD Demo")
    print("=" * 65)

    service = RideService()

    # Locations (using small lat/lng offsets for demo-friendly distances)
    airport = Location(12.9500, 77.6680, "Airport")
    mall = Location(12.9560, 77.6730, "City Mall")
    station = Location(12.9600, 77.6600, "Railway Station")
    office = Location(12.9530, 77.6750, "Tech Park")
    hotel = Location(12.9520, 77.6710, "Grand Hotel")

    # Register drivers
    drivers = [
        Driver("D1", "Ravi", "9000000001",
               Vehicle("V1", VehicleType.MINI, "Maruti", "Swift", "KA01-1234"),
               Location(12.9510, 77.6690, "Near Airport")),
        Driver("D2", "Priya", "9000000002",
               Vehicle("V2", VehicleType.SEDAN, "Honda", "City", "KA02-5678"),
               Location(12.9550, 77.6720, "Downtown")),
        Driver("D3", "Ahmed", "9000000003",
               Vehicle("V3", VehicleType.SUV, "Toyota", "Innova", "KA03-9999"),
               Location(12.9590, 77.6650, "East Side")),
        Driver("D4", "Kumar", "9000000004",
               Vehicle("V4", VehicleType.AUTO, "Bajaj", "RE", "KA04-1111"),
               Location(12.9515, 77.6700, "Station Rd")),
    ]
    for d in drivers:
        service.register_driver(d)

    # Register riders
    riders = [
        Rider("R1", "Alice", "8000000001", airport),
        Rider("R2", "Bob", "8000000002", mall),
        Rider("R3", "Charlie", "8000000003", station),
    ]
    for r in riders:
        service.register_rider(r)

    service.display_drivers()

    # Scenario 1: Normal rides
    print("\n[Scenario 1: Normal Rides]")
    ride1 = service.request_ride(riders[0], airport, mall, VehicleType.MINI)
    RatingService.rate_ride(ride1, 4.5, 5.0)

    ride2 = service.request_ride(riders[1], mall, office, VehicleType.SEDAN)
    RatingService.rate_ride(ride2, 5.0, 4.0)

    ride3 = service.request_ride(riders[2], station, hotel, VehicleType.SUV)
    RatingService.rate_ride(ride3, 4.0, 4.5)

    # Scenario 2: Auto ride
    print("\n[Scenario 2: Auto Ride]")
    ride4 = service.request_ride(riders[1], office, airport, VehicleType.AUTO)
    RatingService.rate_ride(ride4, 3.5, 4.0)

    # Scenario 3: Surge pricing
    print("\n[Scenario 3: Surge Pricing (1.8x)]")
    service.set_surge(1.8)
    ride5 = service.request_ride(riders[2], hotel, airport, VehicleType.SEDAN)
    RatingService.rate_ride(ride5, 4.0, 3.5)
    service.set_surge(1.0)

    # Scenario 4: No driver available
    print("\n[Scenario 4: No Driver Available]")
    service.request_ride(riders[0], airport, station, VehicleType.PREMIUM)

    # Final dashboard
    service.display_drivers()

    print("\n  Ride History for Alice:")
    for ride in riders[0].ride_history:
        print(f"    {ride}")

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
