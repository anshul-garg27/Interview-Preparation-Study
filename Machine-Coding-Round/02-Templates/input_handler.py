"""
Reusable Input Handler for Machine Coding Problems
====================================================
Parses command-line style input like:
  ADD_USER Alice alice@email.com
  CREATE_BOOKING R1 Alice 10:00 11:00
  SHOW_BALANCES
  EXIT

Usage:
  1. Create an InputHandler instance
  2. Register command handlers
  3. Call run() for interactive mode or process_commands() for batch mode
"""


class InputHandler:
    """
    Generic command parser for machine coding problems.
    Supports registering handlers for named commands and processing them.
    """

    def __init__(self):
        self._handlers = {}
        self._descriptions = {}

    def register(self, command_name, handler, description=""):
        """
        Register a handler for a command.

        Args:
            command_name: The command string (e.g., "ADD_USER")
            handler: A callable that accepts the parsed arguments
            description: Human-readable description for HELP command
        """
        self._handlers[command_name.upper()] = handler
        if description:
            self._descriptions[command_name.upper()] = description

    def process_line(self, line):
        """Parse and execute a single command line."""
        line = line.strip()
        if not line or line.startswith("#"):
            return

        parts = line.split()
        command = parts[0].upper()
        args = parts[1:]

        if command == "HELP":
            self._show_help()
            return
        if command == "EXIT":
            return "EXIT"

        handler = self._handlers.get(command)
        if not handler:
            print(f"[ERROR] Unknown command: {command}. Type HELP for available commands.")
            return

        try:
            handler(*args)
        except TypeError as e:
            print(f"[ERROR] Wrong number of arguments for {command}: {e}")
        except Exception as e:
            print(f"[ERROR] Failed to execute {command}: {e}")

    def process_commands(self, commands):
        """Process a list of command strings (batch mode)."""
        for cmd in commands:
            print(f"\n> {cmd}")
            result = self.process_line(cmd)
            if result == "EXIT":
                break

    def run_interactive(self, prompt="> "):
        """Run in interactive mode, reading from stdin."""
        print("Type HELP for available commands, EXIT to quit.\n")
        while True:
            try:
                line = input(prompt)
                result = self.process_line(line)
                if result == "EXIT":
                    print("Goodbye!")
                    break
            except EOFError:
                print("\nGoodbye!")
                break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

    def _show_help(self):
        """Display all registered commands and their descriptions."""
        print("\nAvailable Commands:")
        print("-" * 50)
        for cmd in sorted(self._descriptions.keys()):
            print(f"  {cmd.ljust(25)} {self._descriptions[cmd]}")
        print(f"  {'HELP'.ljust(25)} Show this help message")
        print(f"  {'EXIT'.ljust(25)} Exit the program")
        print("-" * 50)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def _example_demo():
    """Demonstrates how to use InputHandler in a machine coding problem."""

    # Simulate a simple user management system
    users = {}

    def add_user(name, email):
        users[name] = {"name": name, "email": email}
        print(f"[SUCCESS] User added: {name} ({email})")

    def remove_user(name):
        if name in users:
            del users[name]
            print(f"[SUCCESS] User removed: {name}")
        else:
            print(f"[ERROR] User not found: {name}")

    def show_users():
        if not users:
            print("  No users found.")
            return
        print(f"  {'Name'.ljust(15)} {'Email'.ljust(25)}")
        print(f"  {'-' * 40}")
        for user in users.values():
            print(f"  {user['name'].ljust(15)} {user['email'].ljust(25)}")

    # Setup handler
    handler = InputHandler()
    handler.register("ADD_USER", add_user, "ADD_USER <name> <email>")
    handler.register("REMOVE_USER", remove_user, "REMOVE_USER <name>")
    handler.register("SHOW_USERS", show_users, "SHOW_USERS")

    # Batch mode demo
    print("=" * 50)
    print("  INPUT HANDLER DEMO")
    print("=" * 50)

    commands = [
        "ADD_USER Alice alice@example.com",
        "ADD_USER Bob bob@example.com",
        "ADD_USER Charlie charlie@example.com",
        "SHOW_USERS",
        "REMOVE_USER Bob",
        "SHOW_USERS",
        "REMOVE_USER NonExistent",
        "INVALID_COMMAND test",
        "ADD_USER",  # Wrong number of args
    ]

    handler.process_commands(commands)


if __name__ == "__main__":
    _example_demo()
