from abc import ABC, abstractmethod
from typing import Optional

from common_enums import Currency
from ..constants import TransactionType
from account.schemas import AccountSchema


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    async def transfer_direct_money(self, sender_id: str, amount: float, currency: Currency,
                                    receiver_account_id: str, transaction_type: TransactionType,
                                    description: Optional[str]):
        pass

    @abstractmethod
    async def update_balance(self, user_id: str, amount: float, currency: Currency,
                             transaction_type: TransactionType) -> AccountSchema:
        pass

    @abstractmethod
    async def transfer_money_by_phone(self, user_collection, phone: int, sender_id: str, amount: float,
                                      currency: Currency, description: Optional[str],
                                      transaction_type: TransactionType):
        pass
