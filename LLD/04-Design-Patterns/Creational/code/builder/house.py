"""House product class."""


class House:
    """The complex product being built step by step."""

    def __init__(self):
        self.foundation = None
        self.walls = None
        self.roof = None
        self.rooms = 0
        self.garage = False
        self.pool = False
        self.garden = False

    def __repr__(self):
        features = []
        if self.garage:
            features.append("garage")
        if self.pool:
            features.append("pool")
        if self.garden:
            features.append("garden")
        extras = f", extras=[{', '.join(features)}]" if features else ""
        return (
            f"House(foundation={self.foundation}, walls={self.walls}, "
            f"roof={self.roof}, rooms={self.rooms}{extras})"
        )
