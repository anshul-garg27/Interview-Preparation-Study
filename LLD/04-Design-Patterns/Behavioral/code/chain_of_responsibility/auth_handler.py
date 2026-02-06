"""AuthenticationHandler - validates request tokens."""

from handler import Handler, Request

VALID_TOKENS = {"token-abc", "token-xyz", "admin-token"}


class AuthenticationHandler(Handler):
    """Checks if the request has a valid auth token."""

    def handle(self, request: Request) -> str:
        if not request.token:
            return "401 Unauthorized: No token provided"
        if request.token not in VALID_TOKENS:
            return "403 Forbidden: Invalid token"
        request.logs.append("Auth: passed")
        return self.pass_to_next(request)
