from currency_service.network_service import CurrencyExchangeService
from .interfaces.commission_interfaces import CalculateCommissionInterface


class WithoutCommission(CalculateCommissionInterface):
    def __init__(self, currency_exchange_service: CurrencyExchangeService):
        self.currency_exchange_service = currency_exchange_service

    async def calculate(self, from_currency: str, to_currency: str, amount: float):
        currency_data = await self.currency_exchange_service.exchange_rate(
            from_currency=from_currency, to_currency=to_currency)
        if not currency_data.from_currency.lower() == from_currency \
                and currency_data.to_currency.lower() == to_currency:
            print("Tickers don't match")
            return
        return round(float(currency_data.exchange_rate) * amount, 2)


class Commission(WithoutCommission):
    def __init__(self, commision: float, currency_exchange_service: CurrencyExchangeService):
        super().__init__(currency_exchange_service=currency_exchange_service)
        self._commission = commision

    async def calculate(self, from_currency: str, to_currency: str, amount: float):
        result = await super().calculate(from_currency=from_currency, to_currency=to_currency, amount=amount)
        fix = result * self._commission / 100
        # transfer fix money to bank account
        return result - fix
