"""Fan commands - on and off."""

from command import Command


class Fan:
    """Receiver: the actual fan device."""

    def __init__(self, location: str):
        self.location = location
        self.speed = 0

    def turn_on(self) -> str:
        self.speed = 3
        return f"{self.location} fan is ON (speed {self.speed})"

    def turn_off(self) -> str:
        self.speed = 0
        return f"{self.location} fan is OFF"


class FanOnCommand(Command):
    def __init__(self, fan: Fan):
        self._fan = fan

    def execute(self) -> str:
        return self._fan.turn_on()

    def undo(self) -> str:
        return self._fan.turn_off()


class FanOffCommand(Command):
    def __init__(self, fan: Fan):
        self._fan = fan

    def execute(self) -> str:
        return self._fan.turn_off()

    def undo(self) -> str:
        return self._fan.turn_on()
