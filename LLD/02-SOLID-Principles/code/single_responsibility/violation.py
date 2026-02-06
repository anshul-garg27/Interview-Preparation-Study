"""SRP Violation - User class does EVERYTHING (data + email + logging)."""


class User:
    """BAD: This class has THREE responsibilities:
    1. Manage user data
    2. Send emails
    3. Log activities
    Any change to email logic or logging requires modifying this class."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.log_entries: list[str] = []

    # Responsibility 1: User data
    def get_info(self) -> str:
        return f"{self.name} ({self.email})"

    # Responsibility 2: Email (why is User sending emails??)
    def send_welcome_email(self) -> str:
        subject = "Welcome!"
        body = f"Hi {self.name}, welcome to our platform!"
        self._log(f"Sent email to {self.email}")
        return f"Email sent to {self.email}: {subject} - {body}"

    def send_password_reset(self) -> str:
        self._log(f"Password reset for {self.email}")
        return f"Password reset email sent to {self.email}"

    # Responsibility 3: Logging (why is User logging??)
    def _log(self, message: str) -> None:
        import datetime
        entry = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}"
        self.log_entries.append(entry)

    def print_logs(self) -> None:
        for entry in self.log_entries:
            print(f"  {entry}")


if __name__ == "__main__":
    print("BAD DESIGN: Single Responsibility Violation\n")

    user = User("Alice", "alice@example.com")
    print(f"User: {user.get_info()}")
    print(user.send_welcome_email())
    print(user.send_password_reset())

    print("\nLogs stored INSIDE user object:")
    user.print_logs()

    print("\nPROBLEMS:")
    print("  1. Change email provider? Must modify User class")
    print("  2. Change logging format? Must modify User class")
    print("  3. Want to test user data logic? Must deal with email/logging")
    print("  4. User class grows endlessly as features are added")
