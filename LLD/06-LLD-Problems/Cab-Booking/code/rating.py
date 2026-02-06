"""Rating system for drivers and riders."""


class Rating:
    """Tracks ratings with running average."""

    def __init__(self):
        self._scores = []

    def add_rating(self, score: float) -> None:
        """Add a rating clamped between 1.0 and 5.0."""
        self._scores.append(max(1.0, min(5.0, score)))

    @property
    def average(self) -> float:
        return sum(self._scores) / len(self._scores) if self._scores else 0.0

    @property
    def count(self) -> int:
        return len(self._scores)


class RatingService:
    """Service to handle mutual ride ratings."""

    @staticmethod
    def rate_ride(ride, rider_rates_driver: float, driver_rates_rider: float) -> None:
        """Both parties rate each other after a completed ride."""
        if ride.driver:
            ride.driver.rating.add_rating(rider_rates_driver)
            print(f"    [Rating] {ride.rider.name} rated {ride.driver.name}: "
                  f"{rider_rates_driver:.1f} stars")
        ride.rider.rating.add_rating(driver_rates_rider)
        print(f"    [Rating] {ride.driver.name} rated {ride.rider.name}: "
              f"{driver_rates_rider:.1f} stars")
