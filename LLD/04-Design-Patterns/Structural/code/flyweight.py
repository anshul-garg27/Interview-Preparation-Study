"""
Flyweight Pattern - Minimizes memory usage by sharing common state
(intrinsic) among many objects while keeping unique state (extrinsic)
separate.

Examples:
1. Text Editor: Character flyweight (font, size shared; position unique)
2. Game: Tree flyweight (type shared; position unique)
3. Memory comparison with and without flyweight
"""
import sys


# --- Text Editor Flyweight ---
class CharacterStyle:
    """Flyweight: shared intrinsic state (font, size, color)."""
    def __init__(self, font: str, size: int, color: str):
        self.font = font
        self.size = size
        self.color = color

    def render(self, char: str, row: int, col: int) -> str:
        return f"'{char}' at ({row},{col}) [{self.font} {self.size}pt {self.color}]"


class CharacterStyleFactory:
    _cache: dict[tuple, CharacterStyle] = {}

    @classmethod
    def get_style(cls, font: str, size: int, color: str) -> CharacterStyle:
        key = (font, size, color)
        if key not in cls._cache:
            cls._cache[key] = CharacterStyle(font, size, color)
        return cls._cache[key]

    @classmethod
    def cache_size(cls) -> int:
        return len(cls._cache)


class Character:
    """Each character holds extrinsic state + reference to flyweight."""
    def __init__(self, char: str, row: int, col: int, style: CharacterStyle):
        self.char = char
        self.row = row
        self.col = col
        self.style = style  # Shared flyweight

    def render(self) -> str:
        return self.style.render(self.char, self.row, self.col)


# --- Game Tree Flyweight ---
class TreeType:
    """Flyweight for shared tree data (texture, mesh, color)."""
    def __init__(self, name: str, color: str, texture: str):
        self.name = name
        self.color = color
        self.texture = texture
        self._data = "X" * 1000  # Simulate heavy data (1KB)


class TreeFactory:
    _cache: dict[str, TreeType] = {}

    @classmethod
    def get_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = f"{name}_{color}"
        if key not in cls._cache:
            cls._cache[key] = TreeType(name, color, texture)
        return cls._cache[key]


class Tree:
    """Individual tree with unique position."""
    def __init__(self, x: float, y: float, tree_type: TreeType):
        self.x = x
        self.y = y
        self.type = tree_type

    def draw(self) -> str:
        return f"  {self.type.name}({self.type.color}) at ({self.x},{self.y})"


# --- Without Flyweight (for comparison) ---
class HeavyCharacter:
    def __init__(self, char, row, col, font, size, color):
        self.char = char
        self.row = row
        self.col = col
        self.font = font
        self.size = size
        self.color = color


if __name__ == "__main__":
    print("=" * 60)
    print("FLYWEIGHT PATTERN DEMO")
    print("=" * 60)

    # Text Editor
    print("\n--- Text Editor Flyweight ---")
    chars = []
    text = "Hello, Flyweight Pattern!"
    for i, ch in enumerate(text):
        style = CharacterStyleFactory.get_style("Arial", 12, "black")
        chars.append(Character(ch, 0, i, style))

    for c in chars[:5]:
        print(f"  {c.render()}")
    print(f"  ... ({len(chars)} total characters)")
    print(f"  Unique styles cached: {CharacterStyleFactory.cache_size()}")
    print(f"  All share same style object? {len(set(id(c.style) for c in chars)) == 1}")

    # Memory comparison
    print("\n--- Memory Comparison (10,000 characters) ---")
    flyweight_chars = []
    heavy_chars = []
    for i in range(10000):
        style = CharacterStyleFactory.get_style("Arial", 12, "black")
        flyweight_chars.append(Character("A", i // 80, i % 80, style))
        heavy_chars.append(HeavyCharacter("A", i // 80, i % 80, "Arial", 12, "black"))

    fw_size = sum(sys.getsizeof(c) for c in flyweight_chars)
    heavy_size = sum(sys.getsizeof(c) for c in heavy_chars)
    print(f"  With flyweight:    ~{fw_size:,} bytes (objects only)")
    print(f"  Without flyweight: ~{heavy_size:,} bytes (objects only)")
    print(f"  Savings: ~{(1 - fw_size / heavy_size) * 100:.0f}% fewer bytes per object")

    # Game Trees
    print("\n--- Game Forest (1000 trees, 3 types) ---")
    import random
    random.seed(42)
    forest = []
    types = [("Oak", "green", "oak.png"), ("Pine", "dark_green", "pine.png"),
             ("Birch", "light_green", "birch.png")]
    for _ in range(1000):
        name, color, tex = random.choice(types)
        tree = Tree(random.uniform(0, 500), random.uniform(0, 500),
                    TreeFactory.get_type(name, color, tex))
        forest.append(tree)

    print(f"  Total trees: {len(forest)}")
    print(f"  Unique tree types: {len(TreeFactory._cache)}")
    print(f"  Sample: {forest[0].draw()}")
    print(f"  Memory saved: ~{997 * 1000 // 1024} KB (997 duplicate textures avoided)")
