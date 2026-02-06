"""Search service - find available rooms with filtering."""


class SearchService:
    """Handles searching and filtering for available conference rooms."""

    def __init__(self, booking_service):
        self._booking_service = booking_service

    def find_available(self, start_time, end_time, min_capacity=None,
                       building_name=None, required_amenities=None):
        """
        Find available rooms matching the given criteria.

        Args:
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            min_capacity: Minimum number of seats required
            building_name: Filter by specific building
            required_amenities: List of Amenity enums that the room must have
        """
        if start_time >= end_time:
            print(f"[ERROR] Start time ({start_time}) must be before end time ({end_time})")
            return []

        calendar = self._booking_service.get_calendar()
        all_rooms = self._booking_service.get_all_rooms()
        results = []

        for room in all_rooms:
            # Filter: availability
            if not calendar.is_available(room.id, start_time, end_time):
                continue

            # Filter: minimum capacity
            if min_capacity and room.capacity < min_capacity:
                continue

            # Filter: building
            if building_name and room.building_name != building_name:
                continue

            # Filter: amenities
            if required_amenities and not room.has_all_amenities(required_amenities):
                continue

            results.append(room)

        return results

    def display_search_results(self, rooms, title="Search Results"):
        """Display search results in a formatted table."""
        print(f"\n  {title}")
        print(f"  {'-' * 55}")
        if not rooms:
            print("  No rooms found matching your criteria.")
        else:
            for i, room in enumerate(rooms, 1):
                print(f"  {i}. {room.short_str()}")
                if room.amenities:
                    amenities_str = ", ".join(a.value for a in room.amenities)
                    print(f"     Amenities: {amenities_str}")
        print(f"  {'-' * 55}")
        print(f"  Total: {len(rooms)} room(s) found")
