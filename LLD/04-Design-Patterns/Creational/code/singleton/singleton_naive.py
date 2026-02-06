"""Naive Singleton using a class variable."""


class NaiveSingleton:
    """Basic singleton - NOT thread-safe."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.value = None

    def __repr__(self):
        return f"NaiveSingleton(value={self.value}, id={id(self)})"


if __name__ == "__main__":
    s1 = NaiveSingleton()
    s2 = NaiveSingleton()
    s1.value = 42
    print(f"s1: {s1}")
    print(f"s2: {s2}")
    print(f"Same instance: {s1 is s2}")
