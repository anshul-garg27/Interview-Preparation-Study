"""Windows platform UI components and factory."""

from button import Button
from checkbox import Checkbox
from factory import GUIFactory


class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button] rendered with Win32 API"

    def on_click(self, callback: str) -> str:
        return f"[Windows Button] WM_CLICK -> {callback}"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[Windows Checkbox] rendered with Win32 API"

    def toggle(self) -> str:
        return "[Windows Checkbox] state toggled via WM_COMMAND"


class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()
