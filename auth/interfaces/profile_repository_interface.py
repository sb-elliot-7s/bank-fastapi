from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from ..schemas import User


class ProfileRepositoryInterface(ABC):
    @abstractmethod
    async def update_profile(self, user_id: str, updated_data: dict) -> User:
        pass
