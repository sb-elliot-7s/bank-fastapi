from abc import ABC, abstractmethod

from currency_service.network_service import CurrencyExchangeService
from fastapi import HTTPException, status
from account.account_types import AccountType


class CommissionInterface(ABC):
    @abstractmethod
    async def calculate(self, amount: float, account_type: AccountType, from_currency: str = None,
                        to_currency: str = None): pass

    @property
    def percent(self): return 0.0


class CalculateCommissionInterface(CommissionInterface, ABC):

    def __init__(self, currency_exchange_service: CurrencyExchangeService):
        self.currency_exchange_service = currency_exchange_service

    async def pre_calculate(self, amount: float, from_currency: str, to_currency: str):
        if not (currency_data := await self.currency_exchange_service.exchange_rate(
                from_currency=from_currency, to_currency=to_currency
        )) or (currency_data.from_currency.lower() != from_currency
               and currency_data.to_currency.lower() != to_currency):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='something wrong')
        return round(float(currency_data.exchange_rate) * amount, 2)

    # @abstractmethod
    # async def calculate(self, amount: float, account_type: AccountType,
    #                     from_currency: str = None, to_currency: str = None): pass
