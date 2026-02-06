"""Observer Pattern: Ride notifications."""

from abc import ABC, abstractmethod


class RideObserver(ABC):
    """Observer interface for ride events."""

    @abstractmethod
    def on_ride_update(self, ride, message: str) -> None:
        pass


class RideNotification(RideObserver):
    """Sends notifications to rider and driver on ride events."""

    def on_ride_update(self, ride, message: str) -> None:
        print(f"    [Notify -> {ride.rider.name}] {message}")
        if ride.driver:
            print(f"    [Notify -> {ride.driver.name}] {message}")


class RideNotificationService:
    """Manages observer subscriptions for ride updates."""

    def __init__(self):
        self._observers = []

    def subscribe(self, observer: RideObserver) -> None:
        self._observers.append(observer)

    def notify_all(self, ride, message: str) -> None:
        for obs in self._observers:
            obs.on_ride_update(ride, message)
