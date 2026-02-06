"""
Memento Pattern - Captures and externalizes an object's internal state
so it can be restored later, without violating encapsulation.

Examples:
1. Text Editor with undo/redo: type text, bold, italic
2. Game save system: save checkpoints, restore
"""
from dataclasses import dataclass, field
from copy import deepcopy


# --- Text Editor ---
@dataclass
class EditorMemento:
    """Stores editor state."""
    text: str
    cursor: int
    formatting: dict
    label: str = ""


class TextEditor:
    def __init__(self):
        self.text = ""
        self.cursor = 0
        self.formatting = {"bold": False, "italic": False, "underline": False}

    def type_text(self, text: str):
        self.text = self.text[:self.cursor] + text + self.text[self.cursor:]
        self.cursor += len(text)
        print(f"  Typed: '{text}' -> '{self.text}' (cursor: {self.cursor})")

    def toggle_bold(self):
        self.formatting["bold"] = not self.formatting["bold"]
        print(f"  Bold: {self.formatting['bold']}")

    def toggle_italic(self):
        self.formatting["italic"] = not self.formatting["italic"]
        print(f"  Italic: {self.formatting['italic']}")

    def save(self, label: str = "") -> EditorMemento:
        return EditorMemento(self.text, self.cursor,
                             deepcopy(self.formatting), label)

    def restore(self, memento: EditorMemento):
        self.text = memento.text
        self.cursor = memento.cursor
        self.formatting = deepcopy(memento.formatting)

    def display(self):
        fmt = [k for k, v in self.formatting.items() if v]
        fmt_str = ", ".join(fmt) if fmt else "none"
        print(f"  State: '{self.text}' | Cursor: {self.cursor} | Format: {fmt_str}")


class EditorHistory:
    def __init__(self, editor: TextEditor):
        self.editor = editor
        self._undo_stack: list[EditorMemento] = []
        self._redo_stack: list[EditorMemento] = []

    def save(self, label: str = ""):
        self._undo_stack.append(self.editor.save(label))
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            print("  Nothing to undo")
            return
        self._redo_stack.append(self.editor.save("before_undo"))
        memento = self._undo_stack.pop()
        self.editor.restore(memento)
        print(f"  << Undo (restored: '{memento.label}')")

    def redo(self):
        if not self._redo_stack:
            print("  Nothing to redo")
            return
        self._undo_stack.append(self.editor.save("before_redo"))
        memento = self._redo_stack.pop()
        self.editor.restore(memento)
        print(f"  >> Redo")


# --- Game Save System ---
@dataclass
class GameState:
    level: int
    hp: int
    score: int
    inventory: list = field(default_factory=list)
    position: tuple = (0, 0)


class GameSaveSystem:
    def __init__(self):
        self._checkpoints: dict[str, GameState] = {}

    def save(self, name: str, state: GameState):
        self._checkpoints[name] = deepcopy(state)
        print(f"  Saved checkpoint '{name}': Level {state.level}, "
              f"HP={state.hp}, Score={state.score}")

    def load(self, name: str) -> GameState:
        if name not in self._checkpoints:
            print(f"  Checkpoint '{name}' not found!")
            return None
        state = deepcopy(self._checkpoints[name])
        print(f"  Loaded '{name}': Level {state.level}, "
              f"HP={state.hp}, Score={state.score}")
        return state

    def list_saves(self):
        for name, state in self._checkpoints.items():
            print(f"    [{name}] Level {state.level}, HP={state.hp}, "
                  f"Score={state.score}, Items={state.inventory}")


if __name__ == "__main__":
    print("=" * 60)
    print("MEMENTO PATTERN DEMO")
    print("=" * 60)

    # Text Editor
    print("\n--- Text Editor with Undo/Redo ---")
    editor = TextEditor()
    history = EditorHistory(editor)

    history.save("initial")
    editor.type_text("Hello")
    history.save("after_hello")
    editor.type_text(" World")
    history.save("after_world")
    editor.toggle_bold()
    history.save("after_bold")
    editor.type_text("!")
    editor.display()

    print("\n  Undoing 3 times:")
    history.undo(); editor.display()
    history.undo(); editor.display()
    history.undo(); editor.display()

    print("\n  Redoing 1 time:")
    history.redo(); editor.display()

    # Game Save System
    print("\n--- Game Save System ---")
    saves = GameSaveSystem()
    state = GameState(level=1, hp=100, score=0, inventory=["sword"])

    saves.save("start", state)
    state.level = 3; state.hp = 75; state.score = 1500
    state.inventory.append("shield")
    saves.save("mid_game", state)
    state.level = 5; state.hp = 20; state.score = 4200
    state.inventory.append("potion")
    saves.save("boss_fight", state)

    print("\n  All checkpoints:")
    saves.list_saves()

    print("\n  Player dies! Loading mid_game...")
    state = saves.load("mid_game")
    print(f"  Restored inventory: {state.inventory}")
