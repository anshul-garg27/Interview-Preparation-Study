"""LoggingHandler - logs request details."""

from handler import Handler, Request


class LoggingHandler(Handler):
    """Logs the request path and accumulated middleware data."""

    def handle(self, request: Request) -> str:
        request.logs.append(f"Logging: {request.path}")
        print(f"    [LOG] {request.ip} -> {request.path} | chain: {request.logs}")
        return self.pass_to_next(request)
