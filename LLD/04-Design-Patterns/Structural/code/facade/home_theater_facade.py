"""Facade that simplifies home theater operations."""

from subsystems import DVDPlayer, Amplifier, Projector, Screen, Lights


class HomeTheaterFacade:
    """Simple interface hiding complex subsystem interactions."""

    def __init__(self):
        self._dvd = DVDPlayer()
        self._amp = Amplifier()
        self._projector = Projector()
        self._screen = Screen()
        self._lights = Lights()

    def watch_movie(self, movie: str) -> list[str]:
        steps = [
            "Preparing to watch movie...",
            self._lights.dim(10),
            self._screen.down(),
            self._projector.on(),
            self._projector.wide_screen(),
            self._amp.on(),
            self._amp.set_volume(7),
            self._dvd.on(),
            self._dvd.play(movie),
        ]
        return steps

    def end_movie(self) -> list[str]:
        steps = [
            "Shutting down movie...",
            self._dvd.off(),
            self._amp.off(),
            self._projector.off(),
            self._screen.up(),
            self._lights.on(),
        ]
        return steps
