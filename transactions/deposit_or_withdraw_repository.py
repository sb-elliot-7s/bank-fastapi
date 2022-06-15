from bson import ObjectId

from common_enums import Currency
from .constants import TransactionType
from .interfaces.repository_interfaces import DepositOrWithdrawRepositoryInterface
from .schemas import DepositWithdrawTransactionSchema
from database import client
from .utils import TransactionData
from .common_repository import CommonRepository


class DepositOrWithdrawRepository(DepositOrWithdrawRepositoryInterface, CommonRepository):

    async def deposit_or_withdraw_money(self, transaction_type: TransactionType, user_id: str, amount: float,
                                        currency: Currency) -> DepositWithdrawTransactionSchema:
        account = await self.get_account(_filter={'user_id': user_id, 'currency': currency.value})
        async with await client.start_session() as session:
            async with session.start_transaction():
                if transaction_type == TransactionType.WITHDRAW:
                    await self.utils.check_balance(amount=amount, balance=account['balance'])
                _amount = -amount if transaction_type == TransactionType.WITHDRAW else amount
                updated_account = await self.update_balance(filtered={'_id': ObjectId(account['_id'])},
                                                            updated={'$inc': {'balance': _amount}})
                transaction_data = await TransactionData().get_deposit_or_withdraw_data(
                    commission=0.0, amount=amount, transaction_type=transaction_type, currency=currency,
                    account_before_update=account, account_after_update=updated_account)
                return await self.transaction_repository.save_transaction(**transaction_data)
