"""RealImage - expensive to load from disk."""

from subject import Image


class RealImage(Image):
    """Simulates an image that is expensive to load."""

    def __init__(self, filename: str):
        self._filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"    [RealImage] Loading '{self._filename}' from disk... (slow)")

    def display(self) -> str:
        return f"Displaying '{self._filename}'"

    def get_filename(self) -> str:
        return self._filename
