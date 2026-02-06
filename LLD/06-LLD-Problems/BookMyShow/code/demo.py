"""BookMyShow demo - booking flow, concurrent booking, cancellation."""

import threading
from datetime import datetime, timedelta
from enums import SeatType
from movie import Movie
from cinema_hall import CinemaHall
from cinema import Cinema
from show import Show
from user import User
from payment import CreditCardPayment, UPIPayment, WalletPayment
from booking_service import BookingService


def concurrent_booking_test(service, show, users_and_seats):
    """Simulate multiple users trying to book the same seats."""
    results = {}
    lock = threading.Lock()

    def attempt(user, seat_ids, payment):
        booking = service.book_seats(user, show, seat_ids, payment)
        with lock:
            results[user.name] = booking

    threads = []
    for user, seat_ids, payment in users_and_seats:
        t = threading.Thread(target=attempt, args=(user, seat_ids, payment))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


def main():
    print("=" * 60)
    print("  BOOKMYSHOW - Movie Booking System - LLD Demo")
    print("=" * 60)

    # Setup cinema
    screen1 = CinemaHall("S1", "Audi 1", {
        SeatType.VIP: [("A", 5)],
        SeatType.PREMIUM: [("B", 8), ("C", 8)],
        SeatType.REGULAR: [("D", 10), ("E", 10)],
    })
    screen2 = CinemaHall("S2", "Audi 2", {
        SeatType.PREMIUM: [("A", 6)],
        SeatType.REGULAR: [("B", 8), ("C", 8)],
    })

    cinema = Cinema("PVR Cinemas", "Mumbai")
    cinema.add_hall(screen1)
    cinema.add_hall(screen2)

    # Create movies and shows
    movie1 = Movie("M1", "Inception", 148, "Sci-Fi")
    movie2 = Movie("M2", "The Dark Knight", 152, "Action")

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    show1 = Show("SH1", movie1, screen1, today + timedelta(hours=10))
    show2 = Show("SH2", movie1, screen1, today + timedelta(hours=14))
    show3 = Show("SH3", movie2, screen2, today + timedelta(hours=11))
    cinema.add_show(show1)
    cinema.add_show(show2)
    cinema.add_show(show3)

    cinema.display_shows()

    # Search
    print("\n  Searching for 'Inception':")
    for s in cinema.search_shows(movie_title="Inception"):
        print(f"    Found: {s}")

    # Display seat layout
    screen1.display_layout()

    # Booking flow
    print("\n" + "=" * 60)
    print("  BOOKING FLOW")
    print("=" * 60)

    service = BookingService()
    alice = User("Alice", "alice@email.com")
    bob = User("Bob", "bob@email.com")
    charlie = User("Charlie", "charlie@email.com")

    service.book_seats(alice, show1, ["A1", "A2"], CreditCardPayment())
    service.book_seats(bob, show1, ["B3", "B4", "B5"], UPIPayment())
    service.book_seats(charlie, show1, ["D1", "D2", "D3", "D4"],
                       WalletPayment())

    # Concurrent booking - same seats
    print("\n" + "=" * 60)
    print("  CONCURRENT BOOKING TEST (Same Seats)")
    print("=" * 60)

    dave = User("Dave", "dave@email.com")
    eve = User("Eve", "eve@email.com")
    frank = User("Frank", "frank@email.com")

    concurrent_users = [
        (dave, ["A3", "A4"], CreditCardPayment()),
        (eve, ["A3", "A4"], UPIPayment()),
        (frank, ["A3", "A4"], WalletPayment()),
    ]
    results = concurrent_booking_test(service, show1, concurrent_users)

    print("\n  Results:")
    winners = sum(1 for b in results.values() if b is not None)
    print(f"    {winners} out of 3 users got the seats")
    for user_name, booking in results.items():
        status = "GOT SEATS" if booking else "MISSED OUT"
        print(f"    {user_name}: {status}")

    # Seat layout after bookings
    print("\n  Seat layout after bookings:")
    screen1.display_layout(show1)

    # Already-booked seats
    print("\n" + "=" * 60)
    print("  EDGE CASE: Already Booked Seats")
    print("=" * 60)
    grace = User("Grace", "grace@email.com")
    service.book_seats(grace, show1, ["A1", "B3"], CreditCardPayment())

    # Cancellation
    print("\n" + "=" * 60)
    print("  CANCELLATION")
    print("=" * 60)
    if service.bookings:
        last = service.bookings[-1]
        print(f"\n    Cancelling: {last}")
        service.cancel_booking(last)

    # Different show, same screen
    print("\n" + "=" * 60)
    print("  DIFFERENT SHOW - Same Screen")
    print("=" * 60)
    hank = User("Hank", "hank@email.com")
    service.book_seats(hank, show2, ["A1", "A2", "A3"], CreditCardPayment())

    cinema.display_shows()
    print("\nDemo complete!")


if __name__ == "__main__":
    main()
