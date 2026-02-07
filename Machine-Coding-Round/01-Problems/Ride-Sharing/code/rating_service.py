"""Rating service for managing rider and driver ratings."""

from typing import Dict

from enums import RideStatus
from ride import Ride


class RatingService:
    """Manages ratings for riders and drivers after ride completion.

    Ensures ratings are only given for completed rides and within
    the valid range of 1-5 stars.
    """

    def __init__(self) -> None:
        """Initialize the RatingService."""
        self._ride_driver_rated: Dict[str, bool] = {}
        self._ride_rider_rated: Dict[str, bool] = {}

    def rate_driver(self, ride: Ride, rating: int) -> None:
        """Rate a driver for a completed ride.

        Args:
            ride: The completed ride.
            rating: Rating value between 1 and 5.

        Raises:
            ValueError: If ride is not completed, already rated, or rating invalid.
        """
        if ride.status != RideStatus.COMPLETED:
            raise ValueError("Can only rate driver after ride is completed.")
        if not ride.driver:
            raise ValueError("No driver assigned to this ride.")
        if self._ride_driver_rated.get(ride.ride_id, False):
            raise ValueError("Driver already rated for this ride.")
        if not 1 <= rating <= 5:
            raise ValueError(f"Rating must be between 1 and 5, got {rating}.")

        ride.driver.add_rating(rating)
        self._ride_driver_rated[ride.ride_id] = True

    def rate_rider(self, ride: Ride, rating: int) -> None:
        """Rate a rider for a completed ride.

        Args:
            ride: The completed ride.
            rating: Rating value between 1 and 5.

        Raises:
            ValueError: If ride is not completed, already rated, or rating invalid.
        """
        if ride.status != RideStatus.COMPLETED:
            raise ValueError("Can only rate rider after ride is completed.")
        if self._ride_rider_rated.get(ride.ride_id, False):
            raise ValueError("Rider already rated for this ride.")
        if not 1 <= rating <= 5:
            raise ValueError(f"Rating must be between 1 and 5, got {rating}.")

        ride.rider.add_rating(rating)
        self._ride_rider_rated[ride.ride_id] = True
