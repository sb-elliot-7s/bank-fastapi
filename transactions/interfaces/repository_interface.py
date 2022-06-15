from abc import ABC, abstractmethod
from typing import Optional

from common_enums import Currency
from .commission_interfaces import CalculateCommissionInterface
from ..constants import TransactionType
from ..schemas import ExchangeTransactionSchema, MoneyTransactionSchema, DepositWithdrawTransactionSchema


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    async def transfer_direct_money(self, sender_id: str, amount: float,
                                    currency: Currency, receiver_account_id: str,
                                    description: Optional[str]) -> MoneyTransactionSchema:
        pass

    @abstractmethod
    async def deposit_or_withdraw_money(self, transaction_type: TransactionType, user_id: str, amount: float,
                                        currency: Currency) -> DepositWithdrawTransactionSchema:
        pass

    @abstractmethod
    async def transfer_money_by_phone(self, user_collection, phone: int, sender_id: str,
                                      amount: float, currency: Currency,
                                      description: Optional[str]) -> MoneyTransactionSchema:
        pass

    @abstractmethod
    async def exchange_money(self, user_id: str,
                             amount: float,
                             from_currency: Currency,
                             to_currency: Currency,
                             commission_service: CalculateCommissionInterface) -> ExchangeTransactionSchema:
        pass
