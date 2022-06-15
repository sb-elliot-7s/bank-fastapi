from abc import ABC, abstractmethod
from typing import Optional

from common_enums import Currency
from .commission_interfaces import CommissionInterface
from ..constants import TransactionType
from ..schemas import ExchangeTransactionSchema, MoneyTransactionSchema, DepositWithdrawTransactionSchema


class TransferMoneyRepositoryInterface(ABC):
    @abstractmethod
    async def transfer_money_by_phone(self, amount: float, currency: Currency, sender_id: str, phone: int,
                                      user_collection, commission_service: CommissionInterface,
                                      description: Optional[str]) -> MoneyTransactionSchema:
        pass

    @abstractmethod
    async def transfer_direct_money(self, sender_id: str, amount: float,
                                    commission_service: CommissionInterface,
                                    currency: Currency, receiver_account_id: str,
                                    description: Optional[str]) -> MoneyTransactionSchema:
        pass


class DepositOrWithdrawRepositoryInterface(ABC):
    @abstractmethod
    async def deposit_or_withdraw_money(self, transaction_type: TransactionType, currency: Currency,
                                        user_id: str, amount: float, ) -> DepositWithdrawTransactionSchema:
        pass


class ExchangeMoneyRepositoryInterface(ABC):
    @abstractmethod
    async def exchange_money(self, user_id: str, amount: float,
                             from_currency: Currency, to_currency: Currency,
                             commission_service: CommissionInterface) -> ExchangeTransactionSchema:
        pass


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    async def save_transaction(self, amount: float, sender_account_id: str, receiver_account_id: str,
                               currency: Currency, transaction_type: TransactionType, commission: float,
                               description: Optional[str], amount_to_receiver_account: float = None,
                               **others: dict):
        pass
