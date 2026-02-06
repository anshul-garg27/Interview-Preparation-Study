"""Abstract Account base class for library users."""

from abc import ABC, abstractmethod
from enums import AccountStatus


class Account(ABC):
    """Base class for all library account holders."""

    def __init__(self, account_id: str, name: str, email: str):
        self.account_id = account_id
        self.name = name
        self.email = email
        self.status = AccountStatus.ACTIVE

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{self.get_role()}({self.account_id}, {self.name})"
