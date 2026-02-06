"""
Builder Pattern - Constructs complex objects step by step.
Allows producing different types using the same construction process.

Examples:
1. HouseBuilder with Director for pre-configured houses
2. QueryBuilder for SQL queries (fluent interface)
"""


# --- House Builder ---
class House:
    def __init__(self):
        self.floors = 1
        self.rooms = 1
        self.garage = False
        self.swimming_pool = False
        self.garden = False
        self.style = "Basic"

    def __str__(self):
        features = []
        if self.garage: features.append("Garage")
        if self.swimming_pool: features.append("Pool")
        if self.garden: features.append("Garden")
        extras = ", ".join(features) if features else "None"
        return (f"  House({self.style}): {self.floors} floor(s), "
                f"{self.rooms} room(s), Extras: [{extras}]")


class HouseBuilder:
    def __init__(self):
        self._house = House()

    def set_floors(self, floors):
        self._house.floors = floors
        return self  # Fluent interface

    def set_rooms(self, rooms):
        self._house.rooms = rooms
        return self

    def add_garage(self):
        self._house.garage = True
        return self

    def add_swimming_pool(self):
        self._house.swimming_pool = True
        return self

    def add_garden(self):
        self._house.garden = True
        return self

    def set_style(self, style):
        self._house.style = style
        return self

    def build(self):
        house = self._house
        self._house = House()  # Reset for next build
        return house


class Director:
    """Pre-configured build sequences."""

    @staticmethod
    def build_simple_house(builder: HouseBuilder) -> House:
        return (builder.set_style("Simple").set_floors(1)
                .set_rooms(2).add_garden().build())

    @staticmethod
    def build_luxury_house(builder: HouseBuilder) -> House:
        return (builder.set_style("Luxury").set_floors(3)
                .set_rooms(8).add_garage().add_swimming_pool()
                .add_garden().build())


# --- SQL Query Builder ---
class QueryBuilder:
    def __init__(self):
        self._select = "*"
        self._table = ""
        self._where = []
        self._order_by = ""
        self._limit = None
        self._joins = []

    def select(self, *columns):
        self._select = ", ".join(columns)
        return self

    def from_table(self, table):
        self._table = table
        return self

    def where(self, condition):
        self._where.append(condition)
        return self

    def join(self, table, on):
        self._joins.append(f"JOIN {table} ON {on}")
        return self

    def order_by(self, column, desc=False):
        self._order_by = f"{column} {'DESC' if desc else 'ASC'}"
        return self

    def limit(self, n):
        self._limit = n
        return self

    def build(self) -> str:
        query = f"SELECT {self._select} FROM {self._table}"
        for j in self._joins:
            query += f" {j}"
        if self._where:
            query += " WHERE " + " AND ".join(self._where)
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        if self._limit is not None:
            query += f" LIMIT {self._limit}"
        return query


if __name__ == "__main__":
    print("=" * 60)
    print("BUILDER PATTERN DEMO")
    print("=" * 60)

    # House Builder
    print("\n--- House Builder ---")
    builder = HouseBuilder()

    print("Director builds simple house:")
    print(Director.build_simple_house(builder))

    print("Director builds luxury house:")
    print(Director.build_luxury_house(builder))

    print("Custom house (fluent interface):")
    custom = (builder.set_style("Modern").set_floors(2)
              .set_rooms(5).add_garage().add_garden().build())
    print(custom)

    # SQL Query Builder
    print("\n--- SQL Query Builder ---")
    q1 = (QueryBuilder().select("name", "email")
           .from_table("users")
           .where("age > 18").where("active = true")
           .order_by("name").limit(10).build())
    print(f"  Query 1: {q1}")

    q2 = (QueryBuilder().select("o.id", "u.name", "o.total")
           .from_table("orders o")
           .join("users u", "u.id = o.user_id")
           .where("o.total > 100")
           .order_by("o.total", desc=True).build())
    print(f"  Query 2: {q2}")
