"""AdminOnlyProxy - role-based access control (protection proxy)."""

from subject import Image
from real_subject import RealImage


class AdminOnlyProxy(Image):
    """Only allows admin users to display the image."""

    def __init__(self, filename: str, user_role: str):
        self._filename = filename
        self._user_role = user_role
        self._real_image = None

    def display(self) -> str:
        if self._user_role != "admin":
            return f"ACCESS DENIED: '{self._filename}' requires admin role"
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        return self._real_image.display()

    def get_filename(self) -> str:
        return self._filename
