"""
Template Method Pattern - Defines the skeleton of an algorithm in a base
class, letting subclasses override specific steps without changing the
algorithm's structure.

Examples:
1. Data Mining: CSVMiner, JSONMiner, XMLMiner
2. Game AI: abstract play() with init, start_turn, make_move, end_turn
"""
from abc import ABC, abstractmethod
import json


# --- Data Mining ---
class DataMiner(ABC):
    """Template method defines the algorithm skeleton."""

    def mine(self, data: str):
        """Template method - the algorithm skeleton."""
        print(f"  --- {self.__class__.__name__} ---")
        raw = self.extract(data)
        parsed = self.parse(raw)
        analysis = self.analyze(parsed)
        self.report(analysis)

    @abstractmethod
    def extract(self, data: str) -> list[str]:
        pass

    @abstractmethod
    def parse(self, raw_data: list[str]) -> list[dict]:
        pass

    def analyze(self, records: list[dict]) -> dict:
        """Common analysis (can be overridden)."""
        return {
            "count": len(records),
            "fields": list(records[0].keys()) if records else [],
            "sample": records[0] if records else {},
        }

    def report(self, analysis: dict):
        """Common reporting step."""
        print(f"    Records: {analysis['count']}")
        print(f"    Fields: {analysis['fields']}")
        print(f"    Sample: {analysis['sample']}")


class CSVMiner(DataMiner):
    def extract(self, data: str) -> list[str]:
        print("    [CSV] Extracting rows...")
        return data.strip().split("\n")

    def parse(self, raw_data: list[str]) -> list[dict]:
        print("    [CSV] Parsing CSV format...")
        headers = raw_data[0].split(",")
        return [dict(zip(headers, row.split(","))) for row in raw_data[1:]]


class JSONMiner(DataMiner):
    def extract(self, data: str) -> list[str]:
        print("    [JSON] Extracting entries...")
        return [data]

    def parse(self, raw_data: list[str]) -> list[dict]:
        print("    [JSON] Parsing JSON format...")
        return json.loads(raw_data[0])


class XMLMiner(DataMiner):
    def extract(self, data: str) -> list[str]:
        print("    [XML] Extracting tags...")
        import re
        return re.findall(r"<record>(.*?)</record>", data)

    def parse(self, raw_data: list[str]) -> list[dict]:
        print("    [XML] Parsing XML format...")
        import re
        records = []
        for entry in raw_data:
            record = {}
            for match in re.finditer(r"<(\w+)>(.*?)</\1>", entry):
                record[match.group(1)] = match.group(2)
            records.append(record)
        return records


# --- Game AI ---
class GameAI(ABC):
    def play(self):
        """Template method for game turn."""
        self.init()
        for turn in range(1, 4):
            print(f"    Turn {turn}:")
            self.start_turn(turn)
            self.make_move(turn)
            self.end_turn(turn)
        self.game_over()

    @abstractmethod
    def init(self): pass
    @abstractmethod
    def start_turn(self, turn): pass
    @abstractmethod
    def make_move(self, turn): pass

    def end_turn(self, turn):
        print(f"      End of turn {turn}")

    def game_over(self):
        print("    Game Over!")


class AggressiveAI(GameAI):
    def init(self):
        print("    [Aggressive AI] Ready to attack!")

    def start_turn(self, turn):
        print(f"      Scouting enemy positions...")

    def make_move(self, turn):
        print(f"      ATTACKING with full force! (power: {turn * 30})")


class DefensiveAI(GameAI):
    def init(self):
        print("    [Defensive AI] Building fortifications!")

    def start_turn(self, turn):
        print(f"      Checking defenses...")

    def make_move(self, turn):
        print(f"      Building wall (defense: {turn * 20})")


if __name__ == "__main__":
    print("=" * 60)
    print("TEMPLATE METHOD PATTERN DEMO")
    print("=" * 60)

    # Data Mining
    print("\n--- Data Mining ---")
    csv_data = "name,age,city\nAlice,30,NYC\nBob,25,London"
    CSVMiner().mine(csv_data)

    json_data = json.dumps([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
    JSONMiner().mine(json_data)

    xml_data = ("<data><record><name>Alice</name><age>30</age></record>"
                "<record><name>Bob</name><age>25</age></record></data>")
    XMLMiner().mine(xml_data)

    # Game AI
    print("\n--- Game AI ---")
    print("\n  Aggressive Strategy:")
    AggressiveAI().play()
    print("\n  Defensive Strategy:")
    DefensiveAI().play()
