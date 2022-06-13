from abc import ABC, abstractmethod
from typing import Optional
from ..constants import Gender


class AuthRepositoriesInterface(ABC):
    @abstractmethod
    async def save_user(self, first_name: str, last_name: str, password: str, email: str,
                        username: Optional[str], gender: Gender) -> None:
        pass

    @abstractmethod
    async def get_user(self, field: str, value: str): pass
