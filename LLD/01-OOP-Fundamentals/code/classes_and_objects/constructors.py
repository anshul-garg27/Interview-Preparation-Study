"""Constructors - __init__, default params, multiple constructor patterns."""


class User:
    """Basic constructor with default parameters."""

    def __init__(self, name: str, email: str, role: str = "viewer"):
        self.name = name
        self.email = email
        self.role = role

    def __repr__(self):
        return f"User({self.name!r}, {self.email!r}, role={self.role!r})"


class Connection:
    """Multiple constructor patterns using @classmethod."""

    def __init__(self, host: str, port: int, protocol: str):
        self.host = host
        self.port = port
        self.protocol = protocol

    @classmethod
    def from_url(cls, url: str) -> "Connection":
        """Alternative constructor: parse a URL string."""
        # Simple parse: "https://example.com:443"
        protocol, rest = url.split("://")
        host, port = rest.split(":")
        return cls(host, int(port), protocol)

    @classmethod
    def default(cls) -> "Connection":
        """Alternative constructor: default localhost connection."""
        return cls("localhost", 8080, "http")

    def __repr__(self):
        return f"{self.protocol}://{self.host}:{self.port}"


class Temperature:
    """Multiple constructors for unit conversion."""

    def __init__(self, celsius: float):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        return cls((f - 32) * 5 / 9)

    @classmethod
    def from_kelvin(cls, k: float) -> "Temperature":
        return cls(k - 273.15)

    def __repr__(self):
        return f"{self.celsius:.1f}°C"


if __name__ == "__main__":
    print("=== Constructors ===\n")

    # Default parameters
    u1 = User("Alice", "alice@mail.com")
    u2 = User("Bob", "bob@mail.com", role="admin")
    print(f"Default role: {u1}")
    print(f"Custom role:  {u2}")

    # Multiple constructors via classmethod
    print("\n--- Multiple Constructors ---")
    c1 = Connection("api.example.com", 443, "https")
    c2 = Connection.from_url("https://api.example.com:443")
    c3 = Connection.default()
    print(f"Direct:      {c1}")
    print(f"From URL:    {c2}")
    print(f"Default:     {c3}")

    # Temperature conversions
    print("\n--- Temperature Constructors ---")
    t1 = Temperature(100)
    t2 = Temperature.from_fahrenheit(212)
    t3 = Temperature.from_kelvin(373.15)
    print(f"Direct:          {t1}")
    print(f"From Fahrenheit: {t2}")
    print(f"From Kelvin:     {t3}")
