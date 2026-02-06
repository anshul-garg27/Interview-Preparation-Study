"""Singleton using a decorator."""


def singleton(cls):
    """Decorator that makes a class a Singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class AppConfig:
    """Application configuration - only one instance needed."""

    def __init__(self):
        self.settings = {}

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def __repr__(self):
        return f"AppConfig(settings={self.settings})"


if __name__ == "__main__":
    c1 = AppConfig()
    c2 = AppConfig()
    c1.set("theme", "dark")
    print(f"c1: {c1}")
    print(f"c2: {c2}")
    print(f"Same instance: {c1 is c2}")
