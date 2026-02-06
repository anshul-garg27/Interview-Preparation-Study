"""Target interface - the JSON-based system our app expects."""

from abc import ABC, abstractmethod


class JSONDataProvider(ABC):
    """Our application works with JSON data."""

    @abstractmethod
    def get_json_data(self) -> dict:
        pass

    @abstractmethod
    def get_record_count(self) -> int:
        pass
