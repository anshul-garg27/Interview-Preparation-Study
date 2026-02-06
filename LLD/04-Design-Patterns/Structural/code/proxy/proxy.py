"""LazyImageProxy - defers loading until display() is called."""

from subject import Image
from real_subject import RealImage


class LazyImageProxy(Image):
    """Loads the real image only when first displayed (virtual proxy)."""

    def __init__(self, filename: str):
        self._filename = filename
        self._real_image = None

    def display(self) -> str:
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        return self._real_image.display()

    def get_filename(self) -> str:
        return self._filename
