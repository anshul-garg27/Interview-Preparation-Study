"""RemoteControl invoker with undo support."""

from command import Command


class RemoteControl:
    """Invoker: stores and executes commands with undo history."""

    def __init__(self):
        self._history: list[Command] = []

    def press_button(self, command: Command) -> str:
        result = command.execute()
        self._history.append(command)
        return result

    def press_undo(self) -> str:
        if not self._history:
            return "Nothing to undo"
        command = self._history.pop()
        return command.undo()

    def execute_macro(self, commands: list[Command]) -> list[str]:
        """Execute a batch of commands."""
        results = []
        for cmd in commands:
            results.append(self.press_button(cmd))
        return results
