"""Base User class for the Online Shopping System."""


class User:
    """Base class for all users (customers and sellers)."""

    def __init__(self, user_id: str, name: str, email: str, address: str = ""):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.address = address

    def __repr__(self) -> str:
        return f"User({self.name}, {self.email})"
