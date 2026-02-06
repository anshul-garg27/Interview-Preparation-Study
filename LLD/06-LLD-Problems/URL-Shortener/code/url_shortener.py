"""
URL Shortener (TinyURL) - Low Level Design
Run: python url_shortener.py

Patterns: Strategy (encoding), Factory (generator creation)
Key: Short code generation algorithms, collision handling, analytics
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
import random
import string


# ─── Models ──────────────────────────────────────────────────────────
class URLEntry:
    def __init__(self, short_code: str, long_url: str,
                 custom_alias: str = None, ttl_seconds: int = None):
        self.short_code = short_code
        self.long_url = long_url
        self.custom_alias = custom_alias
        self.created_at = datetime.now()
        self.expires_at = (datetime.now() + timedelta(seconds=ttl_seconds)
                          if ttl_seconds else None)
        self.click_count = 0
        self.last_accessed = None

    def is_expired(self) -> bool:
        return self.expires_at is not None and datetime.now() > self.expires_at

    def record_click(self):
        self.click_count += 1
        self.last_accessed = datetime.now()


class ClickStats:
    def __init__(self, total: int, last_accessed: datetime,
                 clicks_by_day: dict):
        self.total = total
        self.last_accessed = last_accessed
        self.clicks_by_day = clicks_by_day


# ─── Strategy Pattern: Code Generators ───────────────────────────────
class CodeGenerator(ABC):
    @abstractmethod
    def generate(self, url: str, length: int = 6) -> str:
        pass


class Base62CounterGenerator(CodeGenerator):
    """Auto-increment counter encoded as Base62. No collisions."""
    BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase

    def __init__(self, start: int = 100000):
        self._counter = start

    def generate(self, url: str, length: int = 6) -> str:
        self._counter += 1
        n = self._counter
        result = []
        while n > 0:
            result.append(self.BASE62[n % 62])
            n //= 62
        return "".join(reversed(result)).zfill(length)[-length:]


class HashBasedGenerator(CodeGenerator):
    """MD5 hash of URL, take first N characters."""
    def generate(self, url: str, length: int = 6) -> str:
        # Add timestamp salt for different codes on retry
        hash_input = url + str(random.random())
        digest = hashlib.md5(hash_input.encode()).hexdigest()
        # Convert hex to base62 for shorter codes
        num = int(digest[:12], 16)
        base62 = string.digits + string.ascii_lowercase + string.ascii_uppercase
        result = []
        while num > 0 and len(result) < length:
            result.append(base62[num % 62])
            num //= 62
        return "".join(reversed(result)).ljust(length, "0")[:length]


class RandomGenerator(CodeGenerator):
    """Random Base62 string."""
    def generate(self, url: str, length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=length))


# ─── Store ───────────────────────────────────────────────────────────
class URLStore:
    def __init__(self):
        self._code_to_entry: dict[str, URLEntry] = {}
        self._url_to_code: dict[str, str] = {}

    def save(self, entry: URLEntry) -> bool:
        if entry.short_code in self._code_to_entry:
            return False
        self._code_to_entry[entry.short_code] = entry
        self._url_to_code[entry.long_url] = entry.short_code
        return True

    def find_by_code(self, code: str) -> URLEntry | None:
        return self._code_to_entry.get(code)

    def find_by_url(self, url: str) -> URLEntry | None:
        code = self._url_to_code.get(url)
        if code:
            return self._code_to_entry.get(code)
        return None

    def code_exists(self, code: str) -> bool:
        return code in self._code_to_entry

    def delete(self, code: str):
        entry = self._code_to_entry.pop(code, None)
        if entry:
            self._url_to_code.pop(entry.long_url, None)


# ─── Analytics ───────────────────────────────────────────────────────
class Analytics:
    def __init__(self):
        self._clicks: dict[str, list[datetime]] = defaultdict(list)

    def record_click(self, code: str):
        self._clicks[code].append(datetime.now())

    def get_stats(self, code: str) -> ClickStats:
        clicks = self._clicks.get(code, [])
        by_day = defaultdict(int)
        for ts in clicks:
            by_day[ts.strftime("%Y-%m-%d")] += 1
        return ClickStats(
            total=len(clicks),
            last_accessed=clicks[-1] if clicks else None,
            clicks_by_day=dict(by_day)
        )


# ─── Service ─────────────────────────────────────────────────────────
class URLShortenerService:
    BASE_URL = "https://short.ly/"
    MAX_RETRIES = 5

    def __init__(self, generator: CodeGenerator, code_length: int = 6):
        self.store = URLStore()
        self.generator = generator
        self.analytics = Analytics()
        self.code_length = code_length

    def shorten(self, long_url: str, custom_alias: str = None,
                ttl_seconds: int = None) -> str:
        # Validate URL
        if not long_url or not long_url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL format")

        # Custom alias
        if custom_alias:
            if self.store.code_exists(custom_alias):
                raise ValueError(f"Alias '{custom_alias}' already taken")
            entry = URLEntry(custom_alias, long_url, custom_alias, ttl_seconds)
            self.store.save(entry)
            return self.BASE_URL + custom_alias

        # Check if URL already shortened (idempotent)
        existing = self.store.find_by_url(long_url)
        if existing and not existing.is_expired():
            return self.BASE_URL + existing.short_code

        # Generate short code with collision handling
        for attempt in range(self.MAX_RETRIES):
            code = self.generator.generate(long_url, self.code_length)
            if not self.store.code_exists(code):
                entry = URLEntry(code, long_url, ttl_seconds=ttl_seconds)
                self.store.save(entry)
                return self.BASE_URL + code

        raise RuntimeError("Failed to generate unique code after retries")

    def redirect(self, short_code: str) -> str:
        entry = self.store.find_by_code(short_code)
        if not entry:
            raise KeyError(f"Short code '{short_code}' not found (404)")
        if entry.is_expired():
            self.store.delete(short_code)
            raise KeyError(f"URL has expired (410 Gone)")
        entry.record_click()
        self.analytics.record_click(short_code)
        return entry.long_url

    def get_analytics(self, short_code: str) -> ClickStats:
        entry = self.store.find_by_code(short_code)
        if not entry:
            raise KeyError(f"Short code '{short_code}' not found")
        return self.analytics.get_stats(short_code)

    def get_info(self, short_code: str) -> dict:
        entry = self.store.find_by_code(short_code)
        if not entry:
            raise KeyError("Not found")
        return {
            "short_code": entry.short_code,
            "long_url": entry.long_url,
            "created_at": entry.created_at.isoformat(),
            "expires_at": entry.expires_at.isoformat() if entry.expires_at else "Never",
            "clicks": entry.click_count,
            "is_expired": entry.is_expired(),
        }


# ─── Demo ────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("URL SHORTENER DEMO")
    print("=" * 60)

    # --- Test each generator ---
    for name, gen in [("Base62 Counter", Base62CounterGenerator()),
                      ("Hash-Based", HashBasedGenerator()),
                      ("Random", RandomGenerator())]:
        print(f"\n{'=' * 60}")
        print(f"  Generator: {name}")
        print(f"{'=' * 60}")
        service = URLShortenerService(gen)

        # Basic shortening
        url1 = "https://www.example.com/very/long/path/to/resource?param=value"
        short1 = service.shorten(url1)
        print(f"  Shortened: {url1[:50]}...")
        print(f"       Code: {short1}")

        # Redirect
        original = service.redirect(short1.split("/")[-1])
        print(f"   Redirect: {original[:50]}...")

        # Idempotent (same URL returns same code)
        short1_again = service.shorten(url1)
        print(f"  Idempotent: {short1 == short1_again}")

    # --- Detailed demo with Base62 ---
    print(f"\n{'=' * 60}")
    print("  FULL FEATURE DEMO (Base62 Counter)")
    print(f"{'=' * 60}")
    service = URLShortenerService(Base62CounterGenerator())

    # Multiple URLs
    urls = [
        "https://docs.python.org/3/library/collections.html",
        "https://github.com/user/repo/pull/42",
        "https://stackoverflow.com/questions/12345/how-to-do-x",
    ]
    codes = []
    for url in urls:
        short = service.shorten(url)
        code = short.split("/")[-1]
        codes.append(code)
        print(f"  {url[:50]:50s} -> {short}")

    # Custom alias
    print(f"\n  Custom alias:")
    short_custom = service.shorten("https://my-portfolio.com", custom_alias="mysite")
    print(f"  https://my-portfolio.com -> {short_custom}")

    # Click analytics
    print(f"\n  Click analytics (simulating 5 clicks on first URL):")
    for _ in range(5):
        service.redirect(codes[0])
    info = service.get_info(codes[0])
    print(f"    Code: {info['short_code']}")
    print(f"    Clicks: {info['clicks']}")
    print(f"    Created: {info['created_at']}")

    # Expiration
    print(f"\n  Expiration (TTL = 0 seconds):")
    short_exp = service.shorten("https://temp-url.com/offer", ttl_seconds=0)
    code_exp = short_exp.split("/")[-1]
    try:
        service.redirect(code_exp)
    except KeyError as e:
        print(f"    {e}")

    # Duplicate custom alias
    print(f"\n  Duplicate alias:")
    try:
        service.shorten("https://other-site.com", custom_alias="mysite")
    except ValueError as e:
        print(f"    {e}")

    # Invalid URL
    print(f"\n  Invalid URL:")
    try:
        service.shorten("not-a-url")
    except ValueError as e:
        print(f"    {e}")

    # Capacity estimation
    print(f"\n{'=' * 60}")
    print("  CAPACITY ESTIMATION")
    print(f"{'=' * 60}")
    code_len = 6
    capacity = 62 ** code_len
    print(f"  Code length: {code_len} chars (Base62)")
    print(f"  Total possible codes: {capacity:,} ({capacity/1e9:.1f} billion)")
    print(f"  At 1M URLs/day: lasts {capacity / 1e6 / 365:.0f} years")


if __name__ == "__main__":
    main()
