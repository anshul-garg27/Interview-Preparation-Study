"""Demo: Command pattern - remote control with undo."""

from light_commands import Light, LightOnCommand, LightOffCommand
from fan_commands import Fan, FanOnCommand, FanOffCommand
from remote_control import RemoteControl


def main():
    print("=" * 50)
    print("COMMAND PATTERN")
    print("=" * 50)

    remote = RemoteControl()
    living_light = Light("Living Room")
    bedroom_fan = Fan("Bedroom")

    # Execute commands
    print("\n--- Execute ---")
    print(f"  {remote.press_button(LightOnCommand(living_light))}")
    print(f"  {remote.press_button(FanOnCommand(bedroom_fan))}")

    # Undo
    print("\n--- Undo ---")
    print(f"  {remote.press_undo()}")
    print(f"  {remote.press_undo()}")
    print(f"  {remote.press_undo()}")  # Nothing to undo

    # Macro command
    print("\n--- Macro: All On ---")
    macro = [LightOnCommand(living_light), FanOnCommand(bedroom_fan)]
    for result in remote.execute_macro(macro):
        print(f"  {result}")

    print("\n--- Undo macro step by step ---")
    print(f"  {remote.press_undo()}")
    print(f"  {remote.press_undo()}")


if __name__ == "__main__":
    main()
