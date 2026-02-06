"""Composition - Car HAS-A Engine, Wheels (strong ownership)."""


class Engine:
    """Engine is OWNED by Car - created and destroyed with it."""

    def __init__(self, horsepower: int, fuel_type: str):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self.running = False

    def start(self) -> str:
        self.running = True
        return f"Engine ({self.horsepower}hp, {self.fuel_type}) started"

    def stop(self) -> str:
        self.running = False
        return "Engine stopped"


class Wheel:
    def __init__(self, size: int):
        self.size = size
        self.pressure = 32  # PSI

    def __repr__(self) -> str:
        return f"Wheel({self.size}in, {self.pressure}psi)"


class GPS:
    def navigate(self, destination: str) -> str:
        return f"Navigating to {destination}"


class Car:
    """Car OWNS its parts - they are created inside the Car."""

    def __init__(self, model: str, hp: int):
        self.model = model
        # Composition: parts are created BY the car
        self._engine = Engine(hp, "gasoline")
        self._wheels = [Wheel(17) for _ in range(4)]
        self._gps = GPS()

    def start(self) -> str:
        return f"{self.model}: {self._engine.start()}"

    def stop(self) -> str:
        return f"{self.model}: {self._engine.stop()}"

    def drive_to(self, dest: str) -> str:
        if not self._engine.running:
            return "Start the car first!"
        return f"{self.model}: {self._gps.navigate(dest)}"

    def status(self) -> str:
        return (f"{self.model} | Engine: {'ON' if self._engine.running else 'OFF'}"
                f" | Wheels: {self._wheels}")


if __name__ == "__main__":
    print("=== Composition (Strong Ownership) ===\n")
    print("Car HAS-A Engine, Wheels, GPS\n")

    car = Car("Tesla Model 3", 283)
    print(car.status())
    print(car.start())
    print(car.drive_to("San Francisco"))
    print(car.stop())

    # If car is destroyed, its engine/wheels/gps are also destroyed
    print("\nKey: Engine, Wheels, GPS don't exist independently of Car.")
    print("Delete car = delete all its parts (strong ownership).")
