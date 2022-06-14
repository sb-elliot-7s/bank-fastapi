from abc import ABC, abstractmethod

from currency_service.network_service import CurrencyExchangeService


class CalculateCommissionInterface(ABC):

    def __init__(self, currency_exchange_service: CurrencyExchangeService):
        self.currency_exchange_service = currency_exchange_service

    async def pre_calculate(self, from_currency: str, to_currency: str, amount: float):
        currency_data = await self.currency_exchange_service.exchange_rate(
            from_currency=from_currency, to_currency=to_currency)
        if not currency_data.from_currency.lower() == from_currency \
                and currency_data.to_currency.lower() == to_currency:
            print("Tickers don't match")
            return
        return round(float(currency_data.exchange_rate) * amount, 2)

    @abstractmethod
    async def calculate(self, from_currency: str, to_currency: str, amount: float):
        pass
