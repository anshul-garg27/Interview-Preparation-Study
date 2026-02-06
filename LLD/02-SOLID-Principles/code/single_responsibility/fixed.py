"""SRP Fixed - Each class has ONE reason to change."""


class User:
    """Only manages user data. Nothing else."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def get_info(self) -> str:
        return f"{self.name} ({self.email})"


class EmailService:
    """Only handles sending emails."""

    def send(self, to: str, subject: str, body: str) -> str:
        return f"Email sent to {to}: {subject} - {body}"

    def send_welcome(self, user: User) -> str:
        return self.send(user.email, "Welcome!", f"Hi {user.name}, welcome!")

    def send_password_reset(self, user: User) -> str:
        return self.send(user.email, "Password Reset", "Click link to reset")


class Logger:
    """Only handles logging."""

    def __init__(self):
        self.entries: list[str] = []

    def log(self, message: str) -> None:
        import datetime
        entry = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}"
        self.entries.append(entry)
        print(f"  LOG: {entry}")


class UserService:
    """Orchestrates user operations using focused services."""

    def __init__(self):
        self.email_service = EmailService()
        self.logger = Logger()

    def register(self, name: str, email: str) -> User:
        user = User(name, email)
        self.logger.log(f"User created: {user.get_info()}")
        result = self.email_service.send_welcome(user)
        self.logger.log(result)
        return user


if __name__ == "__main__":
    print("GOOD DESIGN: Single Responsibility Principle\n")

    service = UserService()
    user = service.register("Alice", "alice@example.com")
    print(f"\nUser: {user.get_info()}")

    print("\nBENEFITS:")
    print("  1. Change email provider? Only modify EmailService")
    print("  2. Change logging? Only modify Logger")
    print("  3. Test user logic? No email/logging dependencies")
    print("  4. Each class is small, focused, and testable")
