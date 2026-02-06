"""Abstract Handler for the middleware chain."""

from abc import ABC, abstractmethod


class Request:
    """HTTP-like request object passed through the chain."""

    def __init__(self, path: str, token: str = None, ip: str = "127.0.0.1"):
        self.path = path
        self.token = token
        self.ip = ip
        self.logs: list[str] = []


class Handler(ABC):
    """Base handler with next-handler linking."""

    def __init__(self):
        self._next: Handler = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: Request) -> str:
        pass

    def pass_to_next(self, request: Request) -> str:
        if self._next:
            return self._next.handle(request)
        return "Request processed successfully"
