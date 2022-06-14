from datetime import datetime
from typing import Optional
from time import time
from common_enums import Currency
from .constants import TransactionType
from .interfaces.repository_interface import TransactionRepositoryInterface
from database import client
from fastapi import HTTPException, status
from bson import ObjectId
from account.schemas import AccountSchema
from .utils import TransactionUtils

from .interfaces.commission_interfaces import CalculateCommissionInterface


class TransactionRepository(TransactionRepositoryInterface):
    def __init__(self, transaction_collection, account_collection):
        self._account_collection = account_collection
        self._transaction_collection = transaction_collection
        self.utils = TransactionUtils()

    async def _get_account(self, user_id: str, currency: Currency):
        filtered = {'user_id': user_id, 'currency': currency.value}
        if not (account := await self._account_collection.find_one(filter=filtered)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not found')
        return account

    async def _update_balance(self, amount: float, account_id: str, transaction_type: TransactionType):
        transaction_types = (transaction_type.DEPOSIT, transaction_type.TRANSFER, transaction_type.PHONE)
        amount = amount if transaction_type in transaction_types else - amount
        return await self._account_collection \
            .find_one_and_update(filter={'_id': ObjectId(account_id)}, update={'$inc': {'balance': amount}},
                                 return_document=True)

    async def _save_transaction(self, amount: float, currency: Currency, sender_account_id: str,
                                receiver_account_id: str, transaction_type: TransactionType,
                                description: Optional[str], amount_rate: float = None):
        document = {
            'amount': amount,
            'currency': currency.value,
            'transaction_type': transaction_type.value,
            'receiver_account_id': receiver_account_id,
            'sender_account_id': sender_account_id,
            'description': description,
            'unix_ts': time(),
            'transaction_datetime': datetime.utcnow(),
            'to_receiver_account_amount': amount_rate
        }
        await self._transaction_collection.insert_one(document=document)

    async def _transfer(self, amount: float, sender_account_id: str, receiver_account_id: str,
                        transaction_type: TransactionType, currency: Currency, description: Optional[str]):
        async with await client.start_session() as session:
            async with session.start_transaction():
                data = {'amount': -amount, 'account_id': sender_account_id,
                        'transaction_type': transaction_type}
                _ = await self._update_balance(**data)
                receiver_account = await self._account_collection.find_one_and_update(
                    filter={'currency': currency.value, '_id': ObjectId(receiver_account_id)},
                    update={'$inc': {'balance': amount}}, return_document=True
                )
                if receiver_account is not None:
                    transaction_data = {
                        'amount': amount, 'currency': currency, 'transaction_type': transaction_type,
                        'sender_account_id': sender_account_id,
                        'receiver_account_id': receiver_account['_id'], 'description': description
                    }
                    await self._save_transaction(**transaction_data)

    async def transfer_direct_money(self, sender_id: str, amount: float, currency: Currency,
                                    receiver_account_id: str, description: Optional[str],
                                    transaction_type: TransactionType):
        sender_account = await self._get_account(user_id=sender_id, currency=currency)
        await self.utils.check_balance(amount=amount, balance=sender_account['balance'])
        await self._transfer(amount=amount, sender_account_id=sender_account['_id'],
                             receiver_account_id=receiver_account_id, transaction_type=transaction_type,
                             currency=currency, description=description)

    async def transfer_money_by_phone(self, user_collection, phone: int, sender_id: str, amount: float,
                                      currency: Currency, description: Optional[str],
                                      transaction_type: TransactionType):
        sender_account = await self._get_account(user_id=sender_id, currency=currency)
        await self.utils.check_balance(amount=amount, balance=sender_account['balance'])
        if (user := await user_collection.find_one({'phone': phone})) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
        receiver_account = await self._get_account(user_id=str(user['_id']), currency=currency)
        await self._transfer(amount=amount, sender_account_id=sender_account['_id'],
                             receiver_account_id=receiver_account['_id'], transaction_type=transaction_type,
                             currency=currency, description=description)

    async def update_balance(self, user_id: str, amount: float, currency: Currency,
                             transaction_type: TransactionType) -> AccountSchema:
        account = await self._get_account(user_id=user_id, currency=currency)
        async with await client.start_session() as session:
            async with session.start_transaction():
                if transaction_type == TransactionType.WITHDRAW:
                    await self.utils.check_balance(amount=amount, balance=account['balance'])
                data = {'amount': amount, 'account_id': account['_id'], 'transaction_type': transaction_type}
                updated_account = await self._update_balance(**data)
                transaction_data = {
                    'amount': amount, 'currency': currency, 'transaction_type': transaction_type,
                    'sender_account_id': updated_account['_id'],
                    'receiver_account_id': updated_account['_id'],
                    'description': None
                }
                await self._save_transaction(**transaction_data)
                return updated_account

    async def exchange_money(self, user_id: str, amount: float, from_currency: Currency,
                             to_currency: Currency, commission_service: CalculateCommissionInterface):
        from_account = await self._get_account(user_id=user_id, currency=from_currency)
        await self.utils.check_balance(amount=amount, balance=from_account['balance'])
        to_account = await self._get_account(user_id=user_id, currency=to_currency)
        async with await client.start_session() as session:
            async with session.start_transaction():
                await self._account_collection.update_one(
                    filter={'_id': from_account['_id'], 'currency': from_currency.value},
                    update={'$inc': {'balance': -amount}}
                )
                res = await commission_service.calculate(from_currency=from_currency.value,
                                                         to_currency=to_currency.value, amount=amount)
                await self._account_collection.update_one(
                    filter={'_id': to_account['_id'], 'currency': to_currency.value},
                    update={'$inc': {'balance': res}}
                )
                await self._save_transaction(amount=amount, currency=from_currency, sender_account_id=user_id,
                                             receiver_account_id=user_id, description=None, amount_rate=res,
                                             transaction_type=TransactionType.EXCHANGE)
