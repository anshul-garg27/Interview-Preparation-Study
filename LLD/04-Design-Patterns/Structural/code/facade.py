"""
Facade Pattern - Provides a simplified interface to a complex
subsystem. Hides complexity behind a single, easy-to-use API.

Examples:
1. Home Theater: DVD, Projector, Amplifier, Screen, Lights
2. Computer boot: CPU, Memory, HardDrive
"""


# --- Home Theater Subsystem ---
class DVDPlayer:
    def on(self):  return "  DVD Player ON"
    def play(self, movie): return f"  DVD: Playing '{movie}'"
    def stop(self): return "  DVD: Stopped"
    def off(self): return "  DVD Player OFF"


class Projector:
    def on(self):  return "  Projector ON"
    def wide_screen(self): return "  Projector: Widescreen mode"
    def off(self): return "  Projector OFF"


class Amplifier:
    def on(self):  return "  Amplifier ON"
    def set_volume(self, level): return f"  Amplifier: Volume set to {level}"
    def set_surround(self): return "  Amplifier: Surround sound enabled"
    def off(self): return "  Amplifier OFF"


class Screen:
    def down(self): return "  Screen: Lowering"
    def up(self):   return "  Screen: Raising"


class Lights:
    def dim(self, level): return f"  Lights: Dimmed to {level}%"
    def on(self):  return "  Lights ON (100%)"


class HomeTheaterFacade:
    def __init__(self):
        self.dvd = DVDPlayer()
        self.projector = Projector()
        self.amp = Amplifier()
        self.screen = Screen()
        self.lights = Lights()

    def watch_movie(self, movie: str):
        print("  === Starting Movie Night ===")
        for msg in [
            self.lights.dim(15), self.screen.down(),
            self.projector.on(), self.projector.wide_screen(),
            self.amp.on(), self.amp.set_surround(), self.amp.set_volume(7),
            self.dvd.on(), self.dvd.play(movie),
        ]:
            print(msg)

    def end_movie(self):
        print("\n  === Shutting Down ===")
        for msg in [
            self.dvd.stop(), self.dvd.off(),
            self.amp.off(), self.projector.off(),
            self.screen.up(), self.lights.on(),
        ]:
            print(msg)


# --- Computer Boot Subsystem ---
class CPU:
    def freeze(self): return "  CPU: Freezing processes"
    def jump(self, addr): return f"  CPU: Jumping to {addr}"
    def execute(self): return "  CPU: Executing boot sequence"


class Memory:
    def load(self, addr, data): return f"  RAM: Loading '{data}' at {addr}"


class HardDrive:
    def read(self, sector, size): return f"  HDD: Reading {size}B from sector {sector}"


class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hdd = HardDrive()

    def start(self):
        print("  === Booting Computer ===")
        for msg in [
            self.cpu.freeze(),
            self.hdd.read(0, 1024),
            self.memory.load("0x00", "boot_loader"),
            self.cpu.jump("0x00"),
            self.cpu.execute(),
        ]:
            print(msg)
        print("  === Computer Ready ===")


if __name__ == "__main__":
    print("=" * 60)
    print("FACADE PATTERN DEMO")
    print("=" * 60)

    # Home Theater
    print("\n--- Home Theater Facade ---")
    theater = HomeTheaterFacade()
    theater.watch_movie("The Matrix")
    theater.end_movie()

    # Computer Boot
    print("\n--- Computer Boot Facade ---")
    computer = ComputerFacade()
    computer.start()
