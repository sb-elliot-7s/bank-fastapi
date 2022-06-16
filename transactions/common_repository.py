from typing import Optional
from bson import ObjectId

from account.account_types import AccountType
from common_enums import Currency
from fastapi import HTTPException, status
from database import client
from transactions.constants import TransactionType
from transactions.interfaces.commission_interfaces import CommissionInterface
from transactions.utils import TransactionUtils, TransactionData
from .interfaces.repository_interfaces import TransactionRepositoryInterface


class CommonRepository:
    def __init__(self, account_collection, transaction_repository: TransactionRepositoryInterface):
        self.transaction_repository = transaction_repository
        self._account_collection = account_collection
        self.utils = TransactionUtils()

    async def get_account(self, _filter: dict):
        if not (account := await self._account_collection.find_one(filter=_filter)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not found')
        return account

    async def update_balance(self, filtered: dict, updated: dict):
        return await self._account_collection \
            .find_one_and_update(filter=filtered, update=updated, return_document=True)

    async def _transfer(self, amount: float, currency: Currency, desc: Optional[str], sender_account: dict,
                        amount_to_receiver_account: float, transaction_type: TransactionType,
                        receiver_account: dict, to_currency: Currency, commission: float, discount: float):
        transaction_data = await TransactionData().get_transfer_data(
            commission=commission, amount=amount, receiver_account=receiver_account, desc=desc,
            sender_account=sender_account, amount_to_receiver_account=amount_to_receiver_account,
            currency=currency, transaction_type=transaction_type, to_currency=to_currency, discount=discount)
        return await self.transaction_repository.save_transaction(**transaction_data)

    async def update_accounts_balance(self, sender_account: dict, amount: float, desc: Optional[str],
                                      currency: Currency, receiver_account: dict, to_currency: Currency,
                                      transaction_type: TransactionType,
                                      commission_service: CommissionInterface):
        async with await client.start_session() as session:
            async with session.start_transaction():
                await self.update_balance(filtered={'_id': ObjectId(sender_account['_id'])},
                                          updated={'$inc': {'balance': -amount}})
                account_type = AccountType(sender_account['account_type'])
                res = await commission_service.calculate(
                    account_type=account_type, from_currency=currency.value,
                    to_currency=to_currency.value, amount=amount)
                if (_ := await self.update_balance(filtered={'_id': ObjectId(receiver_account['_id'])},
                                                   updated={'$inc': {'balance': res}})) is not None:
                    return await self._transfer(
                        amount=amount, desc=desc, currency=currency, sender_account=sender_account,
                        transaction_type=transaction_type, receiver_account=receiver_account,
                        amount_to_receiver_account=res, to_currency=to_currency,
                        commission=commission_service.percent, discount=account_type.discount)

    async def get_account_and_check_balance(self, amount: float, user_id: str, currency: Currency):
        account = await self.get_account(_filter={'user_id': user_id, 'currency': currency.value})
        await self.utils.check_balance(amount=amount, balance=account['balance'])
        return account
