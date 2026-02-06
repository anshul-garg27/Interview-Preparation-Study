"""
Command Pattern - Encapsulates a request as an object, letting you
parameterize, queue, log, and undo operations.

Example: Smart Home Remote with undo/redo and macro commands.
Devices: Light, Fan, AC. Supports undo history and macro (party mode).
"""
from abc import ABC, abstractmethod


# --- Command Interface ---
class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass

    @abstractmethod
    def undo(self) -> str:
        pass


# --- Receivers ---
class Light:
    def __init__(self, room: str):
        self.room = room
        self.on = False
        self.brightness = 100

    def turn_on(self):
        self.on = True
        return f"  {self.room} Light ON (brightness: {self.brightness}%)"

    def turn_off(self):
        self.on = False
        return f"  {self.room} Light OFF"


class Fan:
    def __init__(self, room: str):
        self.room = room
        self.speed = 0

    def turn_on(self, speed=3):
        self.speed = speed
        return f"  {self.room} Fan ON (speed: {self.speed})"

    def turn_off(self):
        self.speed = 0
        return f"  {self.room} Fan OFF"


class AC:
    def __init__(self, room: str):
        self.room = room
        self.on = False
        self.temp = 24

    def turn_on(self, temp=24):
        self.on = True
        self.temp = temp
        return f"  {self.room} AC ON at {self.temp}C"

    def turn_off(self):
        self.on = False
        return f"  {self.room} AC OFF"


# --- Concrete Commands ---
class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self): return self.light.turn_on()
    def undo(self):    return self.light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self): return self.light.turn_off()
    def undo(self):    return self.light.turn_on()


class FanOnCommand(Command):
    def __init__(self, fan: Fan, speed=3):
        self.fan = fan
        self.speed = speed
        self._prev_speed = 0

    def execute(self):
        self._prev_speed = self.fan.speed
        return self.fan.turn_on(self.speed)

    def undo(self):
        if self._prev_speed == 0:
            return self.fan.turn_off()
        return self.fan.turn_on(self._prev_speed)


class ACOnCommand(Command):
    def __init__(self, ac: AC, temp=24):
        self.ac = ac
        self.temp = temp

    def execute(self): return self.ac.turn_on(self.temp)
    def undo(self):    return self.ac.turn_off()


# --- Macro Command ---
class MacroCommand(Command):
    def __init__(self, name: str, commands: list[Command]):
        self.name = name
        self.commands = commands

    def execute(self):
        results = [f"  === Executing Macro: {self.name} ==="]
        for cmd in self.commands:
            results.append(cmd.execute())
        return "\n".join(results)

    def undo(self):
        results = [f"  === Undoing Macro: {self.name} ==="]
        for cmd in reversed(self.commands):
            results.append(cmd.undo())
        return "\n".join(results)


# --- Invoker with history ---
class RemoteControl:
    def __init__(self):
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command):
        result = command.execute()
        self._history.append(command)
        self._redo_stack.clear()
        print(result)

    def undo(self):
        if not self._history:
            print("  Nothing to undo")
            return
        cmd = self._history.pop()
        print(cmd.undo())
        self._redo_stack.append(cmd)

    def redo(self):
        if not self._redo_stack:
            print("  Nothing to redo")
            return
        cmd = self._redo_stack.pop()
        print(cmd.execute())
        self._history.append(cmd)


if __name__ == "__main__":
    print("=" * 60)
    print("COMMAND PATTERN DEMO")
    print("=" * 60)

    light = Light("Living Room")
    fan = Fan("Living Room")
    ac = AC("Living Room")
    remote = RemoteControl()

    # Execute commands
    print("\n--- Execute Commands ---")
    remote.execute(LightOnCommand(light))
    remote.execute(FanOnCommand(fan, speed=5))
    remote.execute(ACOnCommand(ac, temp=22))

    # Undo
    print("\n--- Undo (x2) ---")
    remote.undo()
    remote.undo()

    # Redo
    print("\n--- Redo ---")
    remote.redo()

    # Macro: Party Mode
    print("\n--- Macro Command: Party Mode ---")
    party = MacroCommand("Party Mode", [
        LightOnCommand(Light("Dance Floor")),
        FanOnCommand(Fan("Dance Floor"), speed=5),
        ACOnCommand(AC("Dance Floor"), temp=20),
    ])
    remote.execute(party)

    print("\n--- Undo Party Mode ---")
    remote.undo()
