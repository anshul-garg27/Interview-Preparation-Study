"""Singleton using a Metaclass."""


class SingletonMeta(type):
    """Metaclass that creates Singleton instances."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MetaSingleton(metaclass=SingletonMeta):
    """Any class using SingletonMeta becomes a singleton."""

    def __init__(self):
        self.value = None

    def __repr__(self):
        return f"MetaSingleton(value={self.value}, id={id(self)})"


if __name__ == "__main__":
    s1 = MetaSingleton()
    s2 = MetaSingleton()
    s1.value = "hello"
    print(f"s1: {s1}")
    print(f"s2: {s2}")
    print(f"Same instance: {s1 is s2}")
