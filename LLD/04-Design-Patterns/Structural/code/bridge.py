"""
Bridge Pattern - Separates abstraction from implementation so
both can vary independently. Uses composition over inheritance.

Examples:
1. Shape x Renderer: (Circle, Square) x (Vector, Raster)
2. Notification x Priority: (Email, SMS, Push) x (Urgent, Normal)
"""
from abc import ABC, abstractmethod


# --- Shape x Renderer ---
class Renderer(ABC):
    """Implementation interface."""
    @abstractmethod
    def render_circle(self, radius: float) -> str:
        pass

    @abstractmethod
    def render_square(self, side: float) -> str:
        pass


class VectorRenderer(Renderer):
    def render_circle(self, radius: float) -> str:
        return f"Drawing circle as SVG path (r={radius})"

    def render_square(self, side: float) -> str:
        return f"Drawing square as SVG rect (side={side})"


class RasterRenderer(Renderer):
    def render_circle(self, radius: float) -> str:
        return f"Drawing circle as {int(radius*2)}x{int(radius*2)} pixel bitmap"

    def render_square(self, side: float) -> str:
        return f"Drawing square as {int(side)}x{int(side)} pixel bitmap"


class Shape(ABC):
    """Abstraction that holds a reference to a Renderer."""
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        pass


class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float):
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        return self.renderer.render_circle(self.radius)


class Square(Shape):
    def __init__(self, renderer: Renderer, side: float):
        super().__init__(renderer)
        self.side = side

    def draw(self) -> str:
        return self.renderer.render_square(self.side)


# --- Notification x Priority ---
class Priority(ABC):
    @abstractmethod
    def format_message(self, message: str) -> str:
        pass


class UrgentPriority(Priority):
    def format_message(self, message: str) -> str:
        return f"[URGENT] {message.upper()}"


class NormalPriority(Priority):
    def format_message(self, message: str) -> str:
        return f"[Normal] {message}"


class Notification(ABC):
    def __init__(self, priority: Priority):
        self.priority = priority

    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        pass


class EmailNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        msg = self.priority.format_message(message)
        return f"Email to {recipient}: {msg}"


class SMSNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        msg = self.priority.format_message(message)
        return f"SMS to {recipient}: {msg}"


class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        msg = self.priority.format_message(message)
        return f"Push to {recipient}: {msg}"


if __name__ == "__main__":
    print("=" * 60)
    print("BRIDGE PATTERN DEMO")
    print("=" * 60)

    # Shape x Renderer
    print("\n--- Shape x Renderer ---")
    vector = VectorRenderer()
    raster = RasterRenderer()

    shapes = [
        Circle(vector, 5), Circle(raster, 5),
        Square(vector, 10), Square(raster, 10),
    ]
    for s in shapes:
        print(f"  {s.draw()}")

    # Notification x Priority
    print("\n--- Notification x Priority ---")
    urgent = UrgentPriority()
    normal = NormalPriority()

    notifications = [
        EmailNotification(urgent), EmailNotification(normal),
        SMSNotification(urgent), PushNotification(normal),
    ]
    for n in notifications:
        print(f"  {n.send('alice@mail.com', 'Server is down')}")
