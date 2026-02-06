"""User entity for BookMyShow."""


class User:
    """Represents a registered user."""

    def __init__(self, name: str, email: str, phone: str = ""):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self) -> str:
        return f"User({self.name}, {self.email})"
