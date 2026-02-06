"""Cinema entity with screens and shows."""

from datetime import datetime
from cinema_hall import CinemaHall
from show import Show


class Cinema:
    """A cinema multiplex with multiple screens."""

    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city
        self.halls: list[CinemaHall] = []
        self.shows: list[Show] = []

    def add_hall(self, hall: CinemaHall) -> None:
        self.halls.append(hall)

    def add_show(self, show: Show) -> None:
        self.shows.append(show)

    def search_shows(self, movie_title: str = None,
                     date: datetime = None) -> list[Show]:
        """Search shows by title or date."""
        results = self.shows
        if movie_title:
            results = [s for s in results
                       if movie_title.lower() in s.movie.title.lower()]
        if date:
            results = [s for s in results
                       if s.start_time.date() == date.date()]
        return results

    def display_shows(self) -> None:
        """Print all shows with availability."""
        print(f"\n  {self.name} ({self.city}) - Now Showing:")
        print(f"  {'─' * 50}")
        for show in self.shows:
            avail = show.available_count()
            total = len(show.screen.seats)
            print(f"    {show.show_id}: {show.movie.title:20s} | "
                  f"{show.screen.name:10s} | "
                  f"{show.start_time.strftime('%I:%M %p'):>8s} | "
                  f"Seats: {avail}/{total}")
