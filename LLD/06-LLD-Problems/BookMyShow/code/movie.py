"""Movie entity for BookMyShow."""


class Movie:
    """Represents a movie with metadata."""

    def __init__(self, movie_id: str, title: str, duration_min: int,
                 genre: str, language: str = "English", rating: float = 0.0):
        self.movie_id = movie_id
        self.title = title
        self.duration_min = duration_min
        self.genre = genre
        self.language = language
        self.rating = rating

    def __repr__(self) -> str:
        return f"{self.title} ({self.genre}, {self.duration_min}min)"
