from currency_service.network_service import CurrencyExchangeService
from .interfaces.commission_interfaces import CalculateCommissionInterface, CommissionInterface
from account.account_types import AccountType


class WithoutCommission(CalculateCommissionInterface):

    async def calculate(self, amount: float, account_type: AccountType,
                        from_currency: str = None, to_currency: str = None):
        return await self.pre_calculate(from_currency=from_currency, to_currency=to_currency, amount=amount)

    @property
    def percent(self): return f'{0.0}%'


class ExchangeCommission(CalculateCommissionInterface):

    def __init__(self, commission: float, currency_exchange_service: CurrencyExchangeService):
        self._commission = commission
        super().__init__(currency_exchange_service=currency_exchange_service)

    async def calculate(self, amount: float, account_type: AccountType,
                        from_currency: str = None, to_currency: str = None):
        result = await self.pre_calculate(from_currency=from_currency, to_currency=to_currency, amount=amount)
        fix = result * (self._commission / 100 * account_type.discount)
        # transfer fix money to bank account
        return round(result - fix, 2)

    @property
    def percent(self): return str(self._commission) + '%'


class TransferCommission(CommissionInterface):
    def __init__(self, commission: float):
        self._commission = commission

    async def calculate(self, amount: float, account_type: AccountType,
                        from_currency: str = None, to_currency: str = None):
        fix = amount * (self._commission / 100 * account_type.discount)
        # transfer fix money to bank account
        return round(amount - fix, 2)

    @property
    def percent(self): return str(self._commission) + '%'
