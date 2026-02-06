"""RateLimitHandler - limits requests per IP."""

from handler import Handler, Request


class RateLimitHandler(Handler):
    """Tracks request counts per IP and blocks excessive requests."""

    def __init__(self, max_requests: int = 3):
        super().__init__()
        self._counts: dict[str, int] = {}
        self._max = max_requests

    def handle(self, request: Request) -> str:
        count = self._counts.get(request.ip, 0)
        if count >= self._max:
            return f"429 Too Many Requests: {request.ip} exceeded limit"
        self._counts[request.ip] = count + 1
        request.logs.append(f"RateLimit: {count + 1}/{self._max}")
        return self.pass_to_next(request)
