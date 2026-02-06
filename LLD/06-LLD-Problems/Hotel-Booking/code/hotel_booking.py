"""
Hotel Booking System - Low Level Design Implementation

Design Patterns Used:
- State Pattern: Booking lifecycle (Reserved, CheckedIn, CheckedOut, Cancelled)
- Strategy Pattern: Pricing (Regular, Seasonal, Dynamic)
- Observer Pattern: Booking event notifications
- Factory Pattern: Room creation
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
import uuid


# ============================================================
# Enums
# ============================================================

class RoomType(Enum):
    STANDARD = "Standard"
    DELUXE = "Deluxe"
    SUITE = "Suite"

class RoomStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    CLEANING = "cleaning"

class BookingEvent(Enum):
    CREATED = "created"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"


# ============================================================
# Observer Pattern
# ============================================================

class BookingObserver(ABC):
    @abstractmethod
    def on_booking_event(self, booking: "Booking", event: BookingEvent):
        pass

class EmailNotifier(BookingObserver):
    def on_booking_event(self, booking, event):
        print(f"  [EMAIL] {booking.guest.name}: Your booking {booking.booking_id} "
              f"has been {event.value}.")

class AvailabilityTracker(BookingObserver):
    def on_booking_event(self, booking, event):
        if event == BookingEvent.CREATED:
            print(f"  [TRACKER] Room {booking.room.room_number} reserved "
                  f"{booking.check_in} to {booking.check_out}")
        elif event in (BookingEvent.CHECKED_OUT, BookingEvent.CANCELLED):
            print(f"  [TRACKER] Room {booking.room.room_number} released")


# ============================================================
# Pricing Strategies
# ============================================================

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_price: float, check_in: date,
                        check_out: date) -> float:
        pass

class RegularPricing(PricingStrategy):
    def calculate_price(self, base_price, check_in, check_out):
        nights = (check_out - check_in).days
        return base_price * nights

class SeasonalPricing(PricingStrategy):
    def __init__(self, peak_months: List[int] = None, peak_multiplier: float = 1.5):
        self.peak_months = peak_months or [6, 7, 8, 12]
        self.peak_multiplier = peak_multiplier

    def calculate_price(self, base_price, check_in, check_out):
        total = 0.0
        current = check_in
        while current < check_out:
            if current.month in self.peak_months:
                total += base_price * self.peak_multiplier
            else:
                total += base_price
            current += timedelta(days=1)
        return total

class DynamicPricing(PricingStrategy):
    def __init__(self, occupancy_rate: float = 0.5, threshold: float = 0.8,
                 surge_multiplier: float = 1.3):
        self.occupancy_rate = occupancy_rate
        self.threshold = threshold
        self.surge_multiplier = surge_multiplier

    def calculate_price(self, base_price, check_in, check_out):
        nights = (check_out - check_in).days
        if self.occupancy_rate > self.threshold:
            return base_price * self.surge_multiplier * nights
        return base_price * nights


# ============================================================
# Cancellation Policy
# ============================================================

class CancellationPolicy:
    @staticmethod
    def calculate_refund(total_price: float, check_in: date,
                         cancel_date: date) -> Tuple[float, str]:
        days_before = (check_in - cancel_date).days
        if days_before >= 7:
            return total_price, "100% refund (7+ days notice)"
        elif days_before >= 3:
            return total_price * 0.5, "50% refund (3-7 days notice)"
        elif days_before >= 1:
            return total_price * 0.25, "25% refund (1-3 days notice)"
        else:
            return 0.0, "No refund (less than 24 hours)"


# ============================================================
# Room & Factory
# ============================================================

ROOM_CONFIG = {
    RoomType.STANDARD: {"base_price": 100.0, "amenities": ["WiFi", "TV", "AC"]},
    RoomType.DELUXE: {"base_price": 200.0, "amenities": ["WiFi", "TV", "AC", "Mini Bar", "Balcony"]},
    RoomType.SUITE: {"base_price": 400.0, "amenities": ["WiFi", "TV", "AC", "Mini Bar", "Balcony", "Jacuzzi", "Living Room"]},
}

class Room:
    def __init__(self, room_number: str, room_type: RoomType, base_price: float,
                 amenities: List[str]):
        self.room_number = room_number
        self.room_type = room_type
        self.base_price = base_price
        self.amenities = amenities
        self.status = RoomStatus.AVAILABLE

    def is_available_for_dates(self, check_in: date, check_out: date,
                                bookings: List["Booking"]) -> bool:
        for b in bookings:
            if b.room.room_number == self.room_number and not b.is_cancelled():
                if check_in < b.check_out and check_out > b.check_in:
                    return False
        return self.status in (RoomStatus.AVAILABLE, RoomStatus.OCCUPIED)

    def __str__(self):
        return (f"Room {self.room_number} ({self.room_type.value}) - "
                f"${self.base_price}/night | {', '.join(self.amenities)}")


class RoomFactory:
    @staticmethod
    def create_room(room_number: str, room_type: RoomType) -> Room:
        config = ROOM_CONFIG[room_type]
        return Room(room_number, room_type, config["base_price"],
                    list(config["amenities"]))


# ============================================================
# Guest
# ============================================================

class Guest:
    def __init__(self, name: str, email: str, phone: str):
        self.guest_id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.phone = phone


# ============================================================
# State Pattern: Booking States
# ============================================================

class BookingState(ABC):
    @abstractmethod
    def check_in(self, booking: "Booking") -> str:
        pass
    @abstractmethod
    def check_out(self, booking: "Booking") -> str:
        pass
    @abstractmethod
    def cancel(self, booking: "Booking", cancel_date: date) -> str:
        pass

class ReservedState(BookingState):
    def check_in(self, booking):
        booking.room.status = RoomStatus.OCCUPIED
        booking.state = CheckedInState()
        return f"Checked in to Room {booking.room.room_number}. Welcome!"

    def check_out(self, booking):
        return "Cannot check out - guest hasn't checked in yet."

    def cancel(self, booking, cancel_date):
        refund, reason = CancellationPolicy.calculate_refund(
            booking.total_price, booking.check_in, cancel_date)
        booking.state = CancelledState()
        booking.room.status = RoomStatus.AVAILABLE
        booking.refund_amount = refund
        return f"Booking cancelled. {reason}. Refund: ${refund:.2f}"

class CheckedInState(BookingState):
    def check_in(self, booking):
        return "Already checked in."

    def check_out(self, booking):
        booking.room.status = RoomStatus.CLEANING
        booking.state = CheckedOutState()
        total = booking.total_price + booking.room_service_charges
        return (f"Checked out of Room {booking.room.room_number}. "
                f"Room charges: ${booking.total_price:.2f} | "
                f"Room service: ${booking.room_service_charges:.2f} | "
                f"Total: ${total:.2f}")

    def cancel(self, booking, cancel_date):
        return "Cannot cancel after check-in. Please check out instead."

class CheckedOutState(BookingState):
    def check_in(self, booking):
        return "Booking already completed."
    def check_out(self, booking):
        return "Already checked out."
    def cancel(self, booking, cancel_date):
        return "Cannot cancel a completed booking."

class CancelledState(BookingState):
    def check_in(self, booking):
        return "Booking was cancelled."
    def check_out(self, booking):
        return "Booking was cancelled."
    def cancel(self, booking, cancel_date):
        return "Booking is already cancelled."


# ============================================================
# Booking
# ============================================================

class RoomServiceItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Booking:
    def __init__(self, guest: Guest, room: Room, check_in: date,
                 check_out: date, total_price: float):
        self.booking_id = "BK-" + str(uuid.uuid4())[:6].upper()
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.total_price = total_price
        self.state: BookingState = ReservedState()
        self.room_service_charges = 0.0
        self.room_service_items: List[RoomServiceItem] = []
        self.refund_amount = 0.0

    def is_cancelled(self) -> bool:
        return isinstance(self.state, CancelledState)

    def do_check_in(self) -> str:
        return self.state.check_in(self)

    def do_check_out(self) -> str:
        return self.state.check_out(self)

    def cancel(self, cancel_date: date) -> str:
        return self.state.cancel(self, cancel_date)

    def add_room_service(self, item_name: str, price: float) -> str:
        if not isinstance(self.state, CheckedInState):
            return "Room service only available during stay."
        item = RoomServiceItem(item_name, price)
        self.room_service_items.append(item)
        self.room_service_charges += price
        return f"Added {item_name} (${price:.2f}). Total room service: ${self.room_service_charges:.2f}"

    def __str__(self):
        nights = (self.check_out - self.check_in).days
        return (f"[{self.booking_id}] {self.guest.name} | Room {self.room.room_number} "
                f"({self.room.room_type.value}) | {self.check_in} to {self.check_out} "
                f"({nights} nights) | ${self.total_price:.2f} | "
                f"State: {self.state.__class__.__name__}")


# ============================================================
# Hotel
# ============================================================

class Hotel:
    def __init__(self, name: str):
        self.name = name
        self.rooms: Dict[str, Room] = {}
        self.bookings: List[Booking] = []
        self.pricing_strategy: PricingStrategy = RegularPricing()
        self._observers: List[BookingObserver] = []

    def add_observer(self, observer: BookingObserver):
        self._observers.append(observer)

    def _notify(self, booking: Booking, event: BookingEvent):
        for obs in self._observers:
            obs.on_booking_event(booking, event)

    def add_room(self, room: Room):
        self.rooms[room.room_number] = room

    def set_pricing_strategy(self, strategy: PricingStrategy):
        self.pricing_strategy = strategy

    def search_rooms(self, check_in: date, check_out: date,
                     room_type: Optional[RoomType] = None,
                     max_price: Optional[float] = None) -> List[Tuple[Room, float]]:
        results = []
        for room in self.rooms.values():
            if room_type and room.room_type != room_type:
                continue
            if not room.is_available_for_dates(check_in, check_out, self.bookings):
                continue
            price = self.pricing_strategy.calculate_price(
                room.base_price, check_in, check_out)
            if max_price and price > max_price:
                continue
            results.append((room, price))
        results.sort(key=lambda x: x[1])
        return results

    def create_booking(self, guest: Guest, room: Room, check_in: date,
                       check_out: date) -> Optional[Booking]:
        if not room.is_available_for_dates(check_in, check_out, self.bookings):
            print(f"  Room {room.room_number} not available for selected dates.")
            return None
        price = self.pricing_strategy.calculate_price(
            room.base_price, check_in, check_out)
        booking = Booking(guest, room, check_in, check_out, price)
        self.bookings.append(booking)
        self._notify(booking, BookingEvent.CREATED)
        return booking

    def check_in(self, booking: Booking) -> str:
        result = booking.do_check_in()
        if "Welcome" in result:
            self._notify(booking, BookingEvent.CHECKED_IN)
        return result

    def check_out(self, booking: Booking) -> str:
        result = booking.do_check_out()
        if "Checked out" in result:
            self._notify(booking, BookingEvent.CHECKED_OUT)
        return result

    def cancel_booking(self, booking: Booking, cancel_date: date) -> str:
        result = booking.cancel(cancel_date)
        if "cancelled" in result.lower():
            self._notify(booking, BookingEvent.CANCELLED)
        return result


# ============================================================
# Demo
# ============================================================

def main():
    print("=" * 65)
    print("         HOTEL BOOKING SYSTEM - LOW LEVEL DESIGN DEMO")
    print("=" * 65)

    # Setup hotel
    hotel = Hotel("Grand Palace Hotel")
    hotel.add_observer(EmailNotifier())
    hotel.add_observer(AvailabilityTracker())

    # Create rooms using factory
    for i in range(1, 4):
        hotel.add_room(RoomFactory.create_room(f"10{i}", RoomType.STANDARD))
    for i in range(1, 3):
        hotel.add_room(RoomFactory.create_room(f"20{i}", RoomType.DELUXE))
    hotel.add_room(RoomFactory.create_room("301", RoomType.SUITE))

    print(f"\n{hotel.name} - Available Rooms:")
    for room in hotel.rooms.values():
        print(f"  {room}")

    # Create guests
    alice = Guest("Alice Johnson", "alice@email.com", "555-0101")
    bob = Guest("Bob Smith", "bob@email.com", "555-0202")

    # ---- Scenario 1: Search and Book ----
    print("\n" + "=" * 65)
    print("SCENARIO 1: Search and Book with Regular Pricing")
    print("=" * 65)

    check_in = date(2025, 3, 15)
    check_out = date(2025, 3, 18)

    results = hotel.search_rooms(check_in, check_out, RoomType.DELUXE)
    print(f"\nDeluxe rooms for {check_in} to {check_out}:")
    for room, price in results:
        print(f"  {room} => Total: ${price:.2f}")

    if results:
        booking1 = hotel.create_booking(alice, results[0][0], check_in, check_out)
        print(f"\nBooking created: {booking1}")

    # ---- Scenario 2: Seasonal Pricing ----
    print("\n" + "=" * 65)
    print("SCENARIO 2: Search with Seasonal Pricing (Summer)")
    print("=" * 65)

    hotel.set_pricing_strategy(SeasonalPricing(peak_months=[6, 7, 8], peak_multiplier=1.5))
    summer_in = date(2025, 7, 1)
    summer_out = date(2025, 7, 4)

    results = hotel.search_rooms(summer_in, summer_out)
    print(f"\nAll rooms for {summer_in} to {summer_out} (peak season):")
    for room, price in results:
        print(f"  Room {room.room_number} ({room.room_type.value}): "
              f"${room.base_price}/night => Total: ${price:.2f} (1.5x peak)")

    hotel.set_pricing_strategy(RegularPricing())  # Reset

    # ---- Scenario 3: Check-in, Room Service, Check-out ----
    print("\n" + "=" * 65)
    print("SCENARIO 3: Check-In, Room Service, Check-Out")
    print("=" * 65)

    print(f"\n>> {hotel.check_in(booking1)}")
    print(f">> {booking1.add_room_service('Club Sandwich', 18.50)}")
    print(f">> {booking1.add_room_service('Bottle of Wine', 45.00)}")
    print(f">> {booking1.add_room_service('Spa Treatment', 120.00)}")
    print(f"\n>> {hotel.check_out(booking1)}")

    # ---- Scenario 4: Cancellation with Refund ----
    print("\n" + "=" * 65)
    print("SCENARIO 4: Booking Cancellation with Refund Policy")
    print("=" * 65)

    future_in = date(2025, 5, 1)
    future_out = date(2025, 5, 3)
    suite = hotel.rooms["301"]
    booking2 = hotel.create_booking(bob, suite, future_in, future_out)
    print(f"\nBooking created: {booking2}")

    # Cancel 10 days before (100% refund)
    cancel_date = date(2025, 4, 21)
    print(f"\nCancel on {cancel_date} (10 days before):")
    print(f">> {hotel.cancel_booking(booking2, cancel_date)}")

    # Book again and cancel 2 days before (25% refund)
    booking3 = hotel.create_booking(bob, suite, future_in, future_out)
    cancel_date2 = date(2025, 4, 29)
    print(f"\nCancel on {cancel_date2} (2 days before):")
    print(f">> {hotel.cancel_booking(booking3, cancel_date2)}")

    # ---- Scenario 5: Double booking prevention ----
    print("\n" + "=" * 65)
    print("SCENARIO 5: Double Booking Prevention")
    print("=" * 65)

    # Book room 202 first
    room_202 = hotel.rooms["202"]
    booking_in = date(2025, 4, 10)
    booking_out = date(2025, 4, 14)
    booking4 = hotel.create_booking(alice, room_202, booking_in, booking_out)
    print(f"\nFirst booking on 202: {booking4}")

    # Try overlapping dates on the same room
    overlap_in = date(2025, 4, 12)
    overlap_out = date(2025, 4, 16)
    print(f"\nAttempt overlapping booking on Room 202 ({overlap_in} to {overlap_out}):")
    booking5 = hotel.create_booking(bob, room_202, overlap_in, overlap_out)
    if booking5 is None:
        print("  Booking rejected - room not available for those dates.")

    # ---- Summary ----
    print("\n" + "=" * 65)
    print("ALL BOOKINGS SUMMARY")
    print("=" * 65)
    for b in hotel.bookings:
        print(f"  {b}")


if __name__ == "__main__":
    main()
