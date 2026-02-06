"""Demo: Chain of Responsibility - HTTP middleware pipeline."""

from handler import Request
from auth_handler import AuthenticationHandler
from rate_limit_handler import RateLimitHandler
from logging_handler import LoggingHandler


def main():
    print("=" * 50)
    print("CHAIN OF RESPONSIBILITY PATTERN")
    print("=" * 50)

    # Build chain: Auth -> RateLimit -> Logging
    auth = AuthenticationHandler()
    rate_limit = RateLimitHandler(max_requests=3)
    logging = LoggingHandler()
    auth.set_next(rate_limit).set_next(logging)

    # Valid request
    print("\n--- Valid Request ---")
    req = Request("/api/data", token="token-abc")
    print(f"  Result: {auth.handle(req)}")

    # No token
    print("\n--- No Token ---")
    req = Request("/api/data")
    print(f"  Result: {auth.handle(req)}")

    # Invalid token
    print("\n--- Invalid Token ---")
    req = Request("/api/data", token="bad-token")
    print(f"  Result: {auth.handle(req)}")

    # Rate limiting (send 4 requests)
    print("\n--- Rate Limiting ---")
    for i in range(4):
        req = Request(f"/api/item/{i}", token="token-xyz", ip="10.0.0.1")
        print(f"  Request {i + 1}: {auth.handle(req)}")


if __name__ == "__main__":
    main()
