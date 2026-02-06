"""Home theater subsystem components."""


class DVDPlayer:
    def on(self) -> str:
        return "DVD Player is ON"

    def play(self, movie: str) -> str:
        return f"Playing '{movie}'"

    def off(self) -> str:
        return "DVD Player is OFF"


class Amplifier:
    def on(self) -> str:
        return "Amplifier is ON"

    def set_volume(self, level: int) -> str:
        return f"Volume set to {level}"

    def off(self) -> str:
        return "Amplifier is OFF"


class Projector:
    def on(self) -> str:
        return "Projector is ON"

    def wide_screen(self) -> str:
        return "Projector in widescreen mode"

    def off(self) -> str:
        return "Projector is OFF"


class Screen:
    def down(self) -> str:
        return "Screen going down"

    def up(self) -> str:
        return "Screen going up"


class Lights:
    def dim(self, level: int) -> str:
        return f"Lights dimmed to {level}%"

    def on(self) -> str:
        return "Lights are ON"
