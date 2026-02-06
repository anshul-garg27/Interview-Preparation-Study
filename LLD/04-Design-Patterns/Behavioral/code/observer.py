"""
Observer Pattern - Defines a one-to-many dependency so when one object
changes state, all dependents are notified automatically.

Examples:
1. Stock Market: Stock -> PriceAlert, MobileApp, EmailNotifier
2. Weather Station: WeatherData -> Displays
"""
from abc import ABC, abstractmethod


# --- Observer Infrastructure ---
class Observer(ABC):
    @abstractmethod
    def update(self, subject, **kwargs) -> None:
        pass


class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)
        return self

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, **kwargs):
        for obs in self._observers:
            obs.update(self, **kwargs)


# --- Stock Market ---
class Stock(Subject):
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self.symbol = symbol
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        old = self._price
        self._price = value
        if old != value:
            self.notify(old_price=old, new_price=value)


class PriceAlert(Observer):
    def __init__(self, name: str, threshold: float):
        self.name = name
        self.threshold = threshold

    def update(self, subject, **kwargs):
        if subject.price > self.threshold:
            print(f"    [{self.name}] ALERT: {subject.symbol} above "
                  f"${self.threshold} (now ${subject.price:.2f})")


class MobileApp(Observer):
    def __init__(self, user: str):
        self.user = user

    def update(self, subject, **kwargs):
        change = kwargs["new_price"] - kwargs["old_price"]
        arrow = "^" if change > 0 else "v"
        print(f"    [Mobile:{self.user}] {subject.symbol}: "
              f"${kwargs['new_price']:.2f} ({arrow}{abs(change):.2f})")


class EmailNotifier(Observer):
    def __init__(self, email: str):
        self.email = email

    def update(self, subject, **kwargs):
        pct = ((kwargs["new_price"] - kwargs["old_price"]) / kwargs["old_price"]) * 100
        if abs(pct) >= 5:
            print(f"    [Email:{self.email}] {subject.symbol} moved "
                  f"{pct:+.1f}% -> ${kwargs['new_price']:.2f}")


# --- Weather Station ---
class WeatherData(Subject):
    def __init__(self):
        super().__init__()
        self.temperature = 0.0
        self.humidity = 0.0
        self.pressure = 0.0

    def set_measurements(self, temp, humidity, pressure):
        self.temperature = temp
        self.humidity = humidity
        self.pressure = pressure
        self.notify()


class CurrentDisplay(Observer):
    def update(self, subject, **kwargs):
        print(f"    [Current] Temp: {subject.temperature:.1f}C, "
              f"Humidity: {subject.humidity:.1f}%")


class StatisticsDisplay(Observer):
    def __init__(self):
        self._temps = []

    def update(self, subject, **kwargs):
        self._temps.append(subject.temperature)
        avg = sum(self._temps) / len(self._temps)
        print(f"    [Stats] Avg: {avg:.1f}C, Min: {min(self._temps):.1f}C, "
              f"Max: {max(self._temps):.1f}C")


class ForecastDisplay(Observer):
    def __init__(self):
        self._last_pressure = 0

    def update(self, subject, **kwargs):
        if subject.pressure > self._last_pressure:
            forecast = "Improving weather ahead"
        elif subject.pressure < self._last_pressure:
            forecast = "Cooler, rainy weather ahead"
        else:
            forecast = "Same weather continuing"
        self._last_pressure = subject.pressure
        print(f"    [Forecast] {forecast} (pressure: {subject.pressure:.1f})")


if __name__ == "__main__":
    print("=" * 60)
    print("OBSERVER PATTERN DEMO")
    print("=" * 60)

    # Stock Market
    print("\n--- Stock Market ---")
    aapl = Stock("AAPL", 150.00)
    aapl.attach(PriceAlert("Alert-200", 200))
    aapl.attach(MobileApp("Alice"))
    aapl.attach(EmailNotifier("bob@mail.com"))

    for price in [155.00, 180.00, 210.00, 195.00]:
        print(f"\n  AAPL price -> ${price:.2f}")
        aapl.price = price

    # Weather Station
    print("\n--- Weather Station ---")
    weather = WeatherData()
    weather.attach(CurrentDisplay())
    weather.attach(StatisticsDisplay())
    weather.attach(ForecastDisplay())

    for temp, hum, press in [(25, 65, 1013), (28, 70, 1010), (22, 90, 1005)]:
        print(f"\n  New reading: {temp}C, {hum}%, {press}hPa")
        weather.set_measurements(temp, hum, press)
