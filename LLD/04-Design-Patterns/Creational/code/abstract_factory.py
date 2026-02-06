"""
Abstract Factory Pattern - Produces families of related objects
without specifying their concrete classes.

Example: Cross-platform UI factory creating Button, Checkbox, TextField
for Windows and Mac platforms.
"""
from abc import ABC, abstractmethod


# --- Abstract Products ---
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def toggle(self) -> str:
        pass


class TextField(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def set_text(self, text: str) -> str:
        pass


# --- Windows Products ---
class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button - flat, rectangular, blue]"

    def on_click(self) -> str:
        return "Windows button clicked with ripple effect"


class WindowsCheckbox(Checkbox):
    def __init__(self):
        self.checked = False

    def render(self) -> str:
        mark = "X" if self.checked else " "
        return f"[Windows Checkbox [{mark}] - square corners]"

    def toggle(self) -> str:
        self.checked = not self.checked
        return f"Windows checkbox toggled to {self.checked}"


class WindowsTextField(TextField):
    def render(self) -> str:
        return "[Windows TextField |___________| - underlined]"

    def set_text(self, text: str) -> str:
        return f"Windows TextField: |{text}|"


# --- Mac Products ---
class MacButton(Button):
    def render(self) -> str:
        return "[Mac Button - rounded, gradient, shadow]"

    def on_click(self) -> str:
        return "Mac button clicked with bounce animation"


class MacCheckbox(Checkbox):
    def __init__(self):
        self.checked = False

    def render(self) -> str:
        mark = "v" if self.checked else " "
        return f"[Mac Checkbox ({mark}) - rounded toggle]"

    def toggle(self) -> str:
        self.checked = not self.checked
        return f"Mac checkbox toggled to {self.checked}"


class MacTextField(TextField):
    def render(self) -> str:
        return "[Mac TextField (___________) - rounded border]"

    def set_text(self, text: str) -> str:
        return f"Mac TextField: ({text})"


# --- Abstract Factory ---
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

    @abstractmethod
    def create_textfield(self) -> TextField:
        pass


class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

    def create_textfield(self) -> TextField:
        return WindowsTextField()


class MacFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

    def create_textfield(self) -> TextField:
        return MacTextField()


# --- Client code ---
def render_ui(factory: UIFactory, platform: str):
    print(f"\n  --- {platform} UI ---")
    btn = factory.create_button()
    chk = factory.create_checkbox()
    txt = factory.create_textfield()

    print(f"  {btn.render()}")
    print(f"  {chk.render()}")
    print(f"  {txt.render()}")
    print(f"  {btn.on_click()}")
    print(f"  {chk.toggle()}")
    print(f"  {chk.render()}")
    print(f"  {txt.set_text('Hello World')}")


if __name__ == "__main__":
    print("=" * 60)
    print("ABSTRACT FACTORY PATTERN DEMO")
    print("=" * 60)

    render_ui(WindowsFactory(), "Windows")
    render_ui(MacFactory(), "Mac")

    # Factory selection based on config
    print("\n  --- Dynamic Factory Selection ---")
    platform = "mac"
    factory = MacFactory() if platform == "mac" else WindowsFactory()
    btn = factory.create_button()
    print(f"  Platform '{platform}' -> {btn.render()}")
