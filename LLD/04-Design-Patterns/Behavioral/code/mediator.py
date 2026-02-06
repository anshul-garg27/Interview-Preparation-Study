"""
Mediator Pattern - Defines an object that encapsulates how a set of
objects interact, promoting loose coupling by keeping objects from
referring to each other explicitly.

Examples:
1. Chat Room: Users communicate through the room (mediator)
2. Air Traffic Control: Planes communicate through the tower
"""
from abc import ABC, abstractmethod
from datetime import datetime


# --- Chat Room Mediator ---
class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: 'ChatUser', target: str = None):
        pass

    @abstractmethod
    def add_user(self, user: 'ChatUser'):
        pass


class ChatUser:
    def __init__(self, name: str):
        self.name = name
        self.room: ChatMediator = None
        self.messages: list[str] = []

    def send(self, message: str, target: str = None):
        dest = f" to {target}" if target else " to all"
        print(f"  [{self.name}] sends{dest}: {message}")
        self.room.send_message(message, self, target)

    def receive(self, message: str, sender_name: str):
        msg = f"  [{self.name}] received from {sender_name}: {message}"
        self.messages.append(msg)
        print(msg)


class ChatRoom(ChatMediator):
    def __init__(self, name: str):
        self.name = name
        self._users: dict[str, ChatUser] = {}

    def add_user(self, user: ChatUser):
        self._users[user.name] = user
        user.room = self
        print(f"  {user.name} joined '{self.name}'")

    def send_message(self, message: str, sender: ChatUser, target: str = None):
        if target:
            if target in self._users:
                self._users[target].receive(message, sender.name)
            else:
                print(f"  [Room] User '{target}' not found")
        else:
            for name, user in self._users.items():
                if name != sender.name:
                    user.receive(message, sender.name)


# --- Air Traffic Control ---
class ATC:
    """Air Traffic Control mediator."""
    def __init__(self):
        self._aircraft: dict[str, 'Aircraft'] = {}
        self._runway_free = True

    def register(self, aircraft: 'Aircraft'):
        self._aircraft[aircraft.call_sign] = aircraft
        aircraft.atc = self
        print(f"  [ATC] {aircraft.call_sign} registered")

    def request_landing(self, aircraft: 'Aircraft') -> bool:
        if self._runway_free:
            self._runway_free = False
            print(f"  [ATC] {aircraft.call_sign}: Cleared to land on runway 27L")
            self._notify_all(f"{aircraft.call_sign} is landing", exclude=aircraft.call_sign)
            return True
        else:
            print(f"  [ATC] {aircraft.call_sign}: Hold position, runway occupied")
            return False

    def request_takeoff(self, aircraft: 'Aircraft') -> bool:
        if self._runway_free:
            self._runway_free = False
            print(f"  [ATC] {aircraft.call_sign}: Cleared for takeoff runway 27L")
            self._notify_all(f"{aircraft.call_sign} is taking off", exclude=aircraft.call_sign)
            return True
        print(f"  [ATC] {aircraft.call_sign}: Hold, runway occupied")
        return False

    def runway_cleared(self, aircraft: 'Aircraft'):
        self._runway_free = True
        print(f"  [ATC] Runway cleared by {aircraft.call_sign}")
        self._notify_all("Runway is now free", exclude=aircraft.call_sign)

    def _notify_all(self, message: str, exclude: str = None):
        for sign, ac in self._aircraft.items():
            if sign != exclude:
                ac.receive(f"[ATC Broadcast] {message}")


class Aircraft:
    def __init__(self, call_sign: str):
        self.call_sign = call_sign
        self.atc: ATC = None

    def request_landing(self):
        print(f"  {self.call_sign}: Requesting landing")
        return self.atc.request_landing(self)

    def request_takeoff(self):
        print(f"  {self.call_sign}: Requesting takeoff")
        return self.atc.request_takeoff(self)

    def landed(self):
        print(f"  {self.call_sign}: Landed and clearing runway")
        self.atc.runway_cleared(self)

    def receive(self, message: str):
        print(f"    {self.call_sign} hears: {message}")


if __name__ == "__main__":
    print("=" * 60)
    print("MEDIATOR PATTERN DEMO")
    print("=" * 60)

    # Chat Room
    print("\n--- Chat Room ---")
    room = ChatRoom("General")
    alice = ChatUser("Alice")
    bob = ChatUser("Bob")
    charlie = ChatUser("Charlie")

    room.add_user(alice)
    room.add_user(bob)
    room.add_user(charlie)

    print()
    alice.send("Hello everyone!")
    print()
    bob.send("Hey Alice, how are you?", target="Alice")
    print()
    charlie.send("Group meeting at 3pm")

    # Air Traffic Control
    print("\n--- Air Traffic Control ---")
    tower = ATC()
    flight1 = Aircraft("AA-101")
    flight2 = Aircraft("BA-202")
    flight3 = Aircraft("UA-303")

    tower.register(flight1)
    tower.register(flight2)
    tower.register(flight3)

    print()
    flight1.request_landing()   # Granted
    print()
    flight2.request_landing()   # Denied (runway busy)
    print()
    flight1.landed()            # Clears runway
    print()
    flight2.request_landing()   # Now granted
