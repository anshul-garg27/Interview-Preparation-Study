"""Mac platform UI components and factory."""

from button import Button
from checkbox import Checkbox
from factory import GUIFactory


class MacButton(Button):
    def render(self) -> str:
        return "[Mac Button] rendered with Cocoa framework"

    def on_click(self, callback: str) -> str:
        return f"[Mac Button] NSEvent -> {callback}"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "[Mac Checkbox] rendered with Cocoa framework"

    def toggle(self) -> str:
        return "[Mac Checkbox] state toggled via NSButton"


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
