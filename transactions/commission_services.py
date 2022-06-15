from currency_service.network_service import CurrencyExchangeService
from .interfaces.commission_interfaces import CalculateCommissionInterface


class WithoutCommission(CalculateCommissionInterface):

    async def calculate(self, from_currency: str, to_currency: str, amount: float):
        return await self.pre_calculate(from_currency=from_currency, to_currency=to_currency, amount=amount)

    @property
    def percent(self): return f'{0.0}%'


class Commission(CalculateCommissionInterface):

    def __init__(self, commission: float, currency_exchange_service: CurrencyExchangeService):
        self._commission = commission
        super().__init__(currency_exchange_service=currency_exchange_service)

    async def calculate(self, from_currency: str, to_currency: str, amount: float):
        result = await self.pre_calculate(from_currency=from_currency, to_currency=to_currency, amount=amount)
        fix = result * self._commission / 100
        # transfer fix money to bank account
        return round(result - fix, 2)

    @property
    def percent(self): return str(self._commission) + '%'
