from common_enums import Currency
from .constants import TransactionType
from .interfaces.commission_interfaces import CommissionInterface
from .interfaces.repository_interfaces import ExchangeMoneyRepositoryInterface
from .schemas import ExchangeTransactionSchema
from .common_repository import CommonRepository


class ExchangeMoneyRepository(ExchangeMoneyRepositoryInterface, CommonRepository):

    async def exchange_money(self, commission_service: CommissionInterface, user_id: str, amount: float,
                             from_currency: Currency, to_currency: Currency) -> ExchangeTransactionSchema:
        from_account = await self.get_account_and_check_balance(amount, user_id, from_currency)
        to_account = await self.get_account(_filter={'user_id': user_id, 'currency': to_currency.value})
        return await self.update_accounts_balance(
            sender_account=from_account, amount=amount, desc='', currency=from_currency,
            receiver_account=to_account, transaction_type=TransactionType.EXCHANGE,
            commission_service=commission_service, to_currency=to_currency)
