# Conference Room Booking System

## Problem Statement

Design and implement a **Conference Room Booking System** for a company with multiple
buildings. The system should allow employees to search for available rooms, book them
for meetings, and manage their bookings.

**Time Limit**: 90 minutes

---

## Requirements

### Functional Requirements

1. **Building & Room Management**
   - The company has multiple buildings, each with multiple floors
   - Each floor has multiple conference rooms
   - Rooms have different capacities (SMALL: 1-4, MEDIUM: 5-10, LARGE: 11-20)
   - Rooms may have amenities (whiteboard, projector, video conferencing, phone)

2. **Booking Operations**
   - Book a conference room for a given time slot (start time, end time)
   - Cancel an existing booking
   - A room cannot be double-booked (overlapping time slots not allowed)
   - Bookings have an organizer (employee name)

3. **Search & Availability**
   - Search for available rooms in a given time slot
   - Filter by minimum capacity
   - Filter by building
   - Filter by required amenities
   - Show calendar for a specific room (all bookings for the day)

4. **Edge Cases**
   - Cannot book a room in the past (but for this exercise, treat all times as same-day)
   - Cannot book for zero or negative duration
   - Start time must be before end time
   - Booking times are in HH:MM format (24-hour)

### Non-Functional Requirements
- In-memory storage (no database)
- Clean, modular code with separate files per class
- Use enums for room sizes and amenity types
- Handle invalid inputs gracefully

---

## Sample Input/Output

```
=== Setting Up Buildings and Rooms ===
Building HQ added with 2 floors
  Floor 1: Room-A (Small, 4), Room-B (Medium, 8)
  Floor 2: Room-C (Large, 15), Room-D (Medium, 10)

Building Annex added with 1 floor
  Floor 1: Room-E (Small, 3), Room-F (Medium, 6)

=== Booking Rooms ===
[SUCCESS] Booking BK-001 created: Room-A, 09:00-10:00, Organizer: Alice
[SUCCESS] Booking BK-002 created: Room-B, 09:00-11:00, Organizer: Bob
[SUCCESS] Booking BK-003 created: Room-C, 14:00-15:30, Organizer: Charlie
[ERROR]   Room-A is not available from 09:30 to 10:30 (conflicts with BK-001)

=== Search: Available rooms 09:00-10:00, min capacity 5 ===
  Room-C (Large, 15 seats) - Floor 2, Building HQ
  Room-D (Medium, 10 seats) - Floor 2, Building HQ
  Room-F (Medium, 6 seats) - Floor 1, Building Annex

=== Room Calendar: Room-B ===
  09:00-11:00  Bob (BK-002)
  13:00-14:00  (available)
  ...

=== Cancel Booking ===
[SUCCESS] Booking BK-001 cancelled

=== Search: Available rooms 09:00-10:00, min capacity 1 ===
  Room-A (Small, 4 seats) - Floor 1, Building HQ  <-- Now available!
  Room-C (Large, 15 seats) - Floor 2, Building HQ
  Room-D (Medium, 10 seats) - Floor 2, Building HQ
  Room-E (Small, 3 seats) - Floor 1, Building Annex
  Room-F (Medium, 6 seats) - Floor 1, Building Annex
```

---

## Class Diagram

```
┌─────────────┐     ┌──────────┐     ┌─────────────────┐
│  Building    │────>│  Floor   │────>│ ConferenceRoom   │
│             │ 1..* │          │ 1..*│                  │
│ - name      │     │ - number │     │ - id             │
│ - floors[]  │     │ - rooms[]│     │ - name           │
└─────────────┘     └──────────┘     │ - capacity       │
                                      │ - size (enum)    │
                                      │ - amenities[]    │
                                      │ - bookings[]     │
                                      └────────┬─────────┘
                                               │ 0..*
                                      ┌────────┴─────────┐
                                      │    Booking        │
                                      │                   │
                                      │ - id              │
                                      │ - room_id         │
                                      │ - organizer       │
                                      │ - start_time      │
                                      │ - end_time        │
                                      │ - status (enum)   │
                                      └───────────────────┘

┌──────────────────┐     ┌──────────────────┐
│ BookingService    │     │ SearchService     │
│                   │     │                   │
│ + book()          │     │ + find_available()│
│ + cancel()        │     │ + filter_by_*()   │
│ + get_booking()   │     │ + room_calendar() │
└──────────────────┘     └──────────────────┘

Enums: RoomSize (SMALL, MEDIUM, LARGE)
       Amenity (WHITEBOARD, PROJECTOR, VIDEO_CONF, PHONE)
       BookingStatus (CONFIRMED, CANCELLED)
```

---

## File Structure

```
code/
├── enums.py              # RoomSize, Amenity, BookingStatus
├── conference_room.py    # ConferenceRoom class
├── floor.py              # Floor class
├── building.py           # Building class
├── booking.py            # Booking class
├── calendar_view.py      # Room calendar / availability checker
├── booking_service.py    # Book, cancel, get bookings
├── search_service.py     # Search available rooms with filters
└── demo.py               # Full working demo
```

---

## Evaluation Criteria

| Criteria | Points | What They Look For |
|----------|--------|--------------------|
| Executable | 30 | demo.py runs, all features work |
| Modularity | 25 | Separate files, clean OOP, SRP |
| Extensibility | 15 | Easy to add new amenity types, room sizes |
| Edge Cases | 15 | Overlap detection, invalid time, not-found |
| Patterns | 10 | Enums, clean search with filtering |
| Bonus | 5 | Calendar view, formatted output |

---

## Hints

1. **Time overlap detection**: Two slots overlap if `start1 < end2 AND start2 < end1`
2. **Store times as strings** in HH:MM format for simplicity; compare them lexicographically
3. **Use a list of bookings per room** for quick availability checking
4. **Search filtering**: Build filters as a chain (capacity -> building -> amenities -> availability)
5. **ID generation**: Use a simple counter with prefix (BK-001, BK-002, ...)

---

## Extension Ideas (If You Finish Early)

- Recurring bookings (daily, weekly)
- Buffer time between bookings (e.g., 5 min gap)
- Room usage analytics (most booked room, peak hours)
- Notification to organizer when booking is about to start
- Waitlist when a room is fully booked
