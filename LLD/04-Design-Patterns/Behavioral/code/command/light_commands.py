"""Light commands - on and off."""

from command import Command


class Light:
    """Receiver: the actual light device."""

    def __init__(self, location: str):
        self.location = location
        self.is_on = False

    def turn_on(self) -> str:
        self.is_on = True
        return f"{self.location} light is ON"

    def turn_off(self) -> str:
        self.is_on = False
        return f"{self.location} light is OFF"


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> str:
        return self._light.turn_on()

    def undo(self) -> str:
        return self._light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> str:
        return self._light.turn_off()

    def undo(self) -> str:
        return self._light.turn_on()
