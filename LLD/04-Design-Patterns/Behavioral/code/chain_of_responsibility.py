"""
Chain of Responsibility Pattern - Passes a request along a chain of
handlers. Each handler decides to process or pass to the next handler.

Examples:
1. Middleware chain: Auth -> Authorization -> RateLimiting -> Logging -> Handler
2. Support ticket escalation: L1 -> L2 -> L3 -> Manager
"""
from abc import ABC, abstractmethod
from datetime import datetime


# --- Middleware Chain ---
class Request:
    def __init__(self, path: str, method: str, token: str = None,
                 role: str = "user", ip: str = "127.0.0.1"):
        self.path = path
        self.method = method
        self.token = token
        self.role = role
        self.ip = ip


class Response:
    def __init__(self, status: int, body: str):
        self.status = status
        self.body = body

    def __str__(self):
        return f"[{self.status}] {self.body}"


class Middleware(ABC):
    def __init__(self):
        self._next: 'Middleware' = None

    def set_next(self, handler: 'Middleware') -> 'Middleware':
        self._next = handler
        return handler

    def handle(self, request: Request) -> Response:
        if self._next:
            return self._next.handle(request)
        return Response(200, "OK - Request processed")


class AuthMiddleware(Middleware):
    def handle(self, request: Request) -> Response:
        print(f"    [Auth] Checking token...")
        if not request.token:
            return Response(401, "Unauthorized - No token")
        if request.token == "invalid":
            return Response(401, "Unauthorized - Invalid token")
        print(f"    [Auth] Token valid")
        return super().handle(request)


class AuthorizationMiddleware(Middleware):
    def __init__(self, required_role: str = "admin"):
        super().__init__()
        self.required_role = required_role

    def handle(self, request: Request) -> Response:
        print(f"    [Authz] Checking role '{request.role}'...")
        if request.role != self.required_role and request.path.startswith("/admin"):
            return Response(403, f"Forbidden - '{self.required_role}' role required")
        print(f"    [Authz] Access granted")
        return super().handle(request)


class RateLimitMiddleware(Middleware):
    _requests: dict = {}
    LIMIT = 5

    def handle(self, request: Request) -> Response:
        count = self._requests.get(request.ip, 0) + 1
        self._requests[request.ip] = count
        print(f"    [RateLimit] {request.ip}: {count}/{self.LIMIT}")
        if count > self.LIMIT:
            return Response(429, "Too Many Requests")
        return super().handle(request)


class LoggingMiddleware(Middleware):
    def handle(self, request: Request) -> Response:
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"    [Log] {ts} {request.method} {request.path}")
        response = super().handle(request)
        print(f"    [Log] Response: {response}")
        return response


# --- Support Ticket Escalation ---
class SupportTicket:
    def __init__(self, issue: str, severity: int):
        self.issue = issue
        self.severity = severity  # 1=low, 2=medium, 3=high, 4=critical


class SupportHandler(ABC):
    def __init__(self, name: str, max_severity: int):
        self.name = name
        self.max_severity = max_severity
        self._next: 'SupportHandler' = None

    def set_next(self, handler: 'SupportHandler') -> 'SupportHandler':
        self._next = handler
        return handler

    def handle(self, ticket: SupportTicket) -> str:
        if ticket.severity <= self.max_severity:
            return f"  [{self.name}] Resolved: '{ticket.issue}' (severity {ticket.severity})"
        if self._next:
            print(f"  [{self.name}] Escalating '{ticket.issue}' (severity {ticket.severity} > my max {self.max_severity})")
            return self._next.handle(ticket)
        return f"  [UNRESOLVED] No handler for: '{ticket.issue}'"


class L1Support(SupportHandler):
    def __init__(self):
        super().__init__("L1 Support", 1)


class L2Support(SupportHandler):
    def __init__(self):
        super().__init__("L2 Engineer", 2)


class L3Support(SupportHandler):
    def __init__(self):
        super().__init__("L3 Specialist", 3)


class ManagerSupport(SupportHandler):
    def __init__(self):
        super().__init__("Manager", 4)


if __name__ == "__main__":
    print("=" * 60)
    print("CHAIN OF RESPONSIBILITY PATTERN DEMO")
    print("=" * 60)

    # Middleware chain
    print("\n--- Middleware Chain ---")
    auth = AuthMiddleware()
    authz = AuthorizationMiddleware("admin")
    rate = RateLimitMiddleware()
    log = LoggingMiddleware()
    auth.set_next(authz).set_next(rate).set_next(log)

    requests = [
        ("No token", Request("/api/data", "GET")),
        ("Valid user", Request("/api/data", "GET", token="abc123", role="user")),
        ("Admin access", Request("/admin/users", "GET", token="abc123", role="admin")),
        ("Forbidden", Request("/admin/users", "GET", token="abc123", role="user")),
    ]
    for name, req in requests:
        print(f"\n  Request: {name} ({req.method} {req.path})")
        result = auth.handle(req)
        print(f"  Result: {result}")

    # Support Ticket Escalation
    print("\n--- Support Ticket Escalation ---")
    l1 = L1Support()
    l1.set_next(L2Support()).set_next(L3Support()).set_next(ManagerSupport())

    tickets = [
        SupportTicket("Password reset", 1),
        SupportTicket("App crash on login", 2),
        SupportTicket("Data corruption", 3),
        SupportTicket("Security breach", 4),
    ]
    for ticket in tickets:
        print(f"\n  Ticket: '{ticket.issue}' (severity {ticket.severity})")
        print(l1.handle(ticket))
