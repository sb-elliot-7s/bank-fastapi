from abc import ABC, abstractmethod
from typing import Optional

from ..schemas import AccountSchema

from common_enums import Currency


class AccountRepositoryInterface(ABC):

    @abstractmethod
    async def open_account(self, *, balance: Optional[float] = None,
                           currency: Currency,
                           user_id: str) -> Optional[AccountSchema]:
        pass

    @abstractmethod
    async def close_account(self, account_id: str, user_id: str) -> None:
        pass

    @abstractmethod
    async def get_account(self, account_id: str, user_id: str) -> AccountSchema:
        pass

    @abstractmethod
    async def get_all_accounts(self, user_id: str,
                               limit: int = 10) -> list[AccountSchema]:
        pass
