"""
Conference Room Booking System - Demo
======================================
Run: python demo.py
"""

from enums import RoomSize, Amenity
from conference_room import ConferenceRoom
from building import Building
from booking_service import BookingService
from search_service import SearchService


def setup_buildings():
    """Create buildings with floors and rooms."""

    # Building 1: HQ
    hq = Building("HQ")

    floor1 = hq.add_floor(1)
    floor1.add_room(ConferenceRoom(
        "R-A", "Room-A", capacity=4, size=RoomSize.SMALL,
        amenities=[Amenity.WHITEBOARD]
    ))
    floor1.add_room(ConferenceRoom(
        "R-B", "Room-B", capacity=8, size=RoomSize.MEDIUM,
        amenities=[Amenity.WHITEBOARD, Amenity.PROJECTOR]
    ))

    floor2 = hq.add_floor(2)
    floor2.add_room(ConferenceRoom(
        "R-C", "Room-C", capacity=15, size=RoomSize.LARGE,
        amenities=[Amenity.WHITEBOARD, Amenity.PROJECTOR, Amenity.VIDEO_CONFERENCING]
    ))
    floor2.add_room(ConferenceRoom(
        "R-D", "Room-D", capacity=10, size=RoomSize.MEDIUM,
        amenities=[Amenity.PROJECTOR, Amenity.PHONE]
    ))

    # Building 2: Annex
    annex = Building("Annex")

    annex_floor1 = annex.add_floor(1)
    annex_floor1.add_room(ConferenceRoom(
        "R-E", "Room-E", capacity=3, size=RoomSize.SMALL,
        amenities=[Amenity.WHITEBOARD]
    ))
    annex_floor1.add_room(ConferenceRoom(
        "R-F", "Room-F", capacity=6, size=RoomSize.MEDIUM,
        amenities=[Amenity.WHITEBOARD, Amenity.PROJECTOR, Amenity.PHONE]
    ))

    return [hq, annex]


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    # =========================================================================
    # SETUP
    # =========================================================================
    print_header("CONFERENCE ROOM BOOKING SYSTEM")

    buildings = setup_buildings()
    booking_service = BookingService(buildings)
    search_service = SearchService(booking_service)

    # Display building setup
    print_header("Building Setup")
    for building in buildings:
        print(f"\n{building}")

    # =========================================================================
    # FEATURE 1: Book Rooms
    # =========================================================================
    print_header("Feature 1: Book Rooms")

    bk1 = booking_service.book_room("R-A", "Alice", "09:00", "10:00")
    bk2 = booking_service.book_room("R-B", "Bob", "09:00", "11:00")
    bk3 = booking_service.book_room("R-C", "Charlie", "14:00", "15:30")
    bk4 = booking_service.book_room("R-D", "Diana", "10:00", "12:00")
    bk5 = booking_service.book_room("R-F", "Eve", "13:00", "14:00")

    # =========================================================================
    # FEATURE 2: Prevent Double Booking
    # =========================================================================
    print_header("Feature 2: Double Booking Prevention")

    # Try to book Room-A during an overlapping slot
    booking_service.book_room("R-A", "Frank", "09:30", "10:30")
    # Try exact same slot
    booking_service.book_room("R-B", "Grace", "09:00", "11:00")
    # Try a slot that starts within existing booking
    booking_service.book_room("R-C", "Hank", "14:30", "16:00")

    # =========================================================================
    # FEATURE 3: Search Available Rooms
    # =========================================================================
    print_header("Feature 3: Search Available Rooms")

    # Search 1: Available rooms 09:00-10:00, min capacity 5
    print("\n  Query: Available 09:00-10:00, min capacity 5")
    results = search_service.find_available("09:00", "10:00", min_capacity=5)
    search_service.display_search_results(results,
        "Available rooms 09:00-10:00, capacity >= 5")

    # Search 2: Available rooms 09:00-10:00, any capacity
    print("\n  Query: Available 09:00-10:00, any capacity")
    results = search_service.find_available("09:00", "10:00")
    search_service.display_search_results(results,
        "Available rooms 09:00-10:00, any capacity")

    # Search 3: Available rooms in HQ building only
    print("\n  Query: Available 12:00-13:00, HQ building only")
    results = search_service.find_available("12:00", "13:00", building_name="HQ")
    search_service.display_search_results(results,
        "Available rooms 12:00-13:00 in HQ")

    # Search 4: Rooms with video conferencing
    print("\n  Query: Available 10:00-11:00, needs VIDEO_CONFERENCING")
    results = search_service.find_available("10:00", "11:00",
        required_amenities=[Amenity.VIDEO_CONFERENCING])
    search_service.display_search_results(results,
        "Available rooms 10:00-11:00 with Video Conferencing")

    # =========================================================================
    # FEATURE 4: Room Calendar
    # =========================================================================
    print_header("Feature 4: Room Calendars")

    booking_service.show_room_calendar("R-A")
    booking_service.show_room_calendar("R-B")
    booking_service.show_room_calendar("R-C")

    # =========================================================================
    # FEATURE 5: Cancel Booking
    # =========================================================================
    print_header("Feature 5: Cancel Booking")

    # Cancel Alice's booking
    booking_service.cancel_booking(bk1.id)

    # Try to cancel again (already cancelled)
    booking_service.cancel_booking(bk1.id)

    # Try to cancel non-existent booking
    booking_service.cancel_booking("BK-999")

    # =========================================================================
    # FEATURE 6: Room-A is Now Available After Cancellation
    # =========================================================================
    print_header("Feature 6: Room Available After Cancellation")

    print("\n  Room-A should now be available for 09:00-10:00:")
    results = search_service.find_available("09:00", "10:00")
    search_service.display_search_results(results,
        "Available rooms 09:00-10:00 (after cancellation)")

    # Book Room-A again with a different person
    booking_service.book_room("R-A", "Ivy", "09:00", "10:00")

    # =========================================================================
    # FEATURE 7: Edge Cases
    # =========================================================================
    print_header("Feature 7: Edge Case Handling")

    # Invalid room
    booking_service.book_room("R-Z", "Test", "09:00", "10:00")

    # Invalid time (end before start)
    booking_service.book_room("R-A", "Test", "11:00", "10:00")

    # =========================================================================
    # FINAL STATE
    # =========================================================================
    print_header("Final State: All Active Bookings")

    active_bookings = booking_service.get_all_bookings()
    if not active_bookings:
        print("  No active bookings.")
    else:
        print(f"  {'ID':<10} {'Room':<12} {'Time':<14} {'Organizer':<12} {'Status'}")
        print(f"  {'-' * 60}")
        for b in active_bookings:
            print(f"  {b.id:<10} {b.room.name:<12} "
                  f"{b.start_time}-{b.end_time:<7} {b.organizer:<12} {b.status.value}")

    print_header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
