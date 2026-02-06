"""
Proxy Pattern - Provides a surrogate or placeholder for another object
to control access to it.

Examples:
1. Virtual Proxy: LazyImage (loads only when displayed)
2. Protection Proxy: Role-based access control
3. Caching Proxy: CachedWeatherService
"""
from abc import ABC, abstractmethod
import time


# --- Virtual Proxy (Lazy Loading) ---
class Image(ABC):
    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass


class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._load()

    def _load(self):
        self._data = f"[pixel data for {self.filename}]"
        self._size = 1024

    def display(self) -> str:
        return f"  Displaying {self.filename} ({self._size}KB)"

    def get_info(self) -> str:
        return f"  Info: {self.filename}, {self._size}KB"


class LazyImage(Image):
    """Virtual proxy - only loads the real image when display() is called."""
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None
        print(f"  [Proxy] Created lazy proxy for {filename} (NOT loaded)")

    def _ensure_loaded(self):
        if self._real_image is None:
            print(f"  [Proxy] NOW loading {self.filename}...")
            self._real_image = RealImage(self.filename)

    def display(self) -> str:
        self._ensure_loaded()
        return self._real_image.display()

    def get_info(self) -> str:
        if self._real_image:
            return self._real_image.get_info()
        return f"  Info: {self.filename} (not yet loaded)"


# --- Protection Proxy ---
class Document:
    def __init__(self, title: str, content: str, classification: str = "public"):
        self.title = title
        self.content = content
        self.classification = classification


class DocumentAccess(ABC):
    @abstractmethod
    def read(self, doc: Document) -> str:
        pass

    @abstractmethod
    def edit(self, doc: Document, new_content: str) -> str:
        pass


class RealDocumentAccess(DocumentAccess):
    def read(self, doc: Document) -> str:
        return f'  Content of "{doc.title}": {doc.content}'

    def edit(self, doc: Document, new_content: str) -> str:
        doc.content = new_content
        return f'  "{doc.title}" updated successfully'


class ProtectedDocumentAccess(DocumentAccess):
    def __init__(self, user_role: str):
        self.user_role = user_role
        self._real = RealDocumentAccess()
        self._permissions = {
            "admin": {"read": True, "edit": True, "classified": True},
            "editor": {"read": True, "edit": True, "classified": False},
            "viewer": {"read": True, "edit": False, "classified": False},
        }

    def _check_access(self, doc: Document, action: str) -> bool:
        perms = self._permissions.get(self.user_role, {})
        if doc.classification == "classified" and not perms.get("classified"):
            return False
        return perms.get(action, False)

    def read(self, doc: Document) -> str:
        if self._check_access(doc, "read"):
            return self._real.read(doc)
        return f'  ACCESS DENIED: {self.user_role} cannot read "{doc.title}"'

    def edit(self, doc: Document, new_content: str) -> str:
        if self._check_access(doc, "edit"):
            return self._real.edit(doc, new_content)
        return f'  ACCESS DENIED: {self.user_role} cannot edit "{doc.title}"'


# --- Caching Proxy ---
class WeatherService(ABC):
    @abstractmethod
    def get_forecast(self, city: str) -> str:
        pass


class RealWeatherService(WeatherService):
    def get_forecast(self, city: str) -> str:
        time.sleep(0.01)  # Simulate API call
        return f"Sunny, 25C in {city}"


class CachedWeatherService(WeatherService):
    def __init__(self, service: RealWeatherService, ttl: float = 5.0):
        self._service = service
        self._cache: dict[str, tuple[str, float]] = {}
        self._ttl = ttl

    def get_forecast(self, city: str) -> str:
        now = time.time()
        if city in self._cache:
            result, cached_at = self._cache[city]
            if now - cached_at < self._ttl:
                return f"{result} [CACHED]"
        result = self._service.get_forecast(city)
        self._cache[city] = (result, now)
        return f"{result} [FRESH]"


if __name__ == "__main__":
    print("=" * 60)
    print("PROXY PATTERN DEMO")
    print("=" * 60)

    # Virtual Proxy
    print("\n--- Virtual Proxy (Lazy Loading) ---")
    images = [LazyImage(f"photo{i}.jpg") for i in range(1, 4)]
    print(images[0].get_info())  # Not loaded yet
    print(images[0].display())   # Triggers load
    print(images[0].display())   # Already loaded

    # Protection Proxy
    print("\n--- Protection Proxy ---")
    public_doc = Document("Guide", "How to use the app", "public")
    secret_doc = Document("Secrets", "Top secret data", "classified")

    for role in ["admin", "editor", "viewer"]:
        proxy = ProtectedDocumentAccess(role)
        print(f"\n  User role: {role}")
        print(proxy.read(public_doc))
        print(proxy.edit(public_doc, "Updated"))
        print(proxy.read(secret_doc))

    # Caching Proxy
    print("\n--- Caching Proxy ---")
    weather = CachedWeatherService(RealWeatherService())
    for city in ["NYC", "London", "NYC", "Tokyo", "NYC"]:
        print(f"  {city}: {weather.get_forecast(city)}")
