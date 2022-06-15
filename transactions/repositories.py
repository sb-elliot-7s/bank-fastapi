from datetime import datetime
from time import time
from typing import Optional
from fastapi import HTTPException, status
from common_enums import Currency
from .constants import TransactionType
from .interfaces.commission_interfaces import CalculateCommissionInterface
from .interfaces.repository_interface import TransactionRepositoryInterface
from database import client
from .schemas import ExchangeTransactionSchema, MoneyTransactionSchema, DepositWithdrawTransactionSchema
from .utils import TransactionUtils, TransactionData

from bson import ObjectId


class TransactionRepository(TransactionRepositoryInterface):
    def __init__(self, account_collection, transaction_collection):
        self._account_collection = account_collection
        self._transaction_collection = transaction_collection
        self._utils = TransactionUtils()

    async def _get_account(self, user_id: str, currency: Currency):
        filtered = {'user_id': user_id, 'currency': currency.value}
        if not (account := await self._account_collection.find_one(filter=filtered)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not found')
        return account

    async def _save_transaction(self, amount: float, sender_account_id: str, receiver_account_id: str,
                                currency: Currency, transaction_type: TransactionType,
                                description: Optional[str], amount_to_receiver_account: float = None,
                                **others: dict):
        document = {
            'amount': amount,
            'currency': currency.value,
            'transaction_type': transaction_type.value,
            'receiver_account_id': receiver_account_id,
            'sender_account_id': sender_account_id,
            'description': description,
            'unix_ts': time(),
            'transaction_datetime': datetime.utcnow(),
            'amount_to_receiver_account': amount_to_receiver_account,
            **others
        }
        result = await self._transaction_collection.insert_one(document=document)
        return await self._transaction_collection.find_one({'_id': ObjectId(result.inserted_id)})

    async def _update_balance(self, filtered: dict, update: dict):
        return await self._account_collection \
            .find_one_and_update(filter=filtered, update=update, return_document=True)

    async def deposit_or_withdraw_money(self, transaction_type: TransactionType, user_id: str, amount: float,
                                        currency: Currency) -> DepositWithdrawTransactionSchema:
        account = await self._get_account(user_id=user_id, currency=currency)
        async with await client.start_session() as session:
            async with session.start_transaction():
                if transaction_type == TransactionType.WITHDRAW:
                    await self._utils.check_balance(amount=amount, balance=account['balance'])
                _amount = -amount if transaction_type == TransactionType.WITHDRAW else amount
                updated_account = await self._update_balance(filtered={'_id': ObjectId(account['_id'])},
                                                             update={'$inc': {'balance': _amount}})
                transaction_data = await TransactionData().get_deposit_or_withdraw_data(
                    amount=amount, transaction_type=transaction_type, currency=currency,
                    account_before_update=account, account_after_update=updated_account)
                return await self._save_transaction(**transaction_data)

    async def _transfer(self, amount: float, currency: Currency, desc: Optional[str],
                        transaction_type: TransactionType, sender_account: dict, receiver_account: dict):
        transaction_data = await TransactionData().get_transfer_data(
            amount=amount, receiver_account=receiver_account, sender_account=sender_account, desc=desc,
            amount_to_receiver_account=amount, currency=currency, transaction_type=transaction_type)
        return await self._save_transaction(**transaction_data)

    async def _update_accounts_balance(self, sender_account: dict, amount: float, desc: Optional[str],
                                       currency: Currency, receiver_account: dict,
                                       transaction_type: TransactionType):
        async with await client.start_session() as session:
            async with session.start_transaction():
                await self._update_balance(filtered={'_id': ObjectId(sender_account['_id'])},
                                           update={'$inc': {'balance': -amount}})
                if (_ := await self._update_balance(filtered={'_id': ObjectId(receiver_account['_id'])},
                                                    update={'$inc': {'balance': amount}})) is not None:
                    return await self._transfer(
                        amount=amount, desc=desc, currency=currency, sender_account=sender_account,
                        transaction_type=transaction_type, receiver_account=receiver_account)

    async def transfer_money_by_phone(self, user_collection, phone: int, sender_id: str,
                                      amount: float, currency: Currency,
                                      description: Optional[str]) -> MoneyTransactionSchema:
        sender_account = await self._get_account(user_id=sender_id, currency=currency)
        await self._utils.check_balance(amount=amount, balance=sender_account['balance'])
        if (user := await user_collection.find_one({'phone': phone})) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
        receiver_account = await self._get_account(user_id=str(user['_id']), currency=currency)
        return await self._update_accounts_balance(
            currency=currency, desc=description, amount=amount, sender_account=sender_account,
            receiver_account=receiver_account, transaction_type=TransactionType.PHONE)

    async def transfer_direct_money(self, sender_id: str, amount: float,
                                    currency: Currency, receiver_account_id: str,
                                    description: Optional[str]) -> MoneyTransactionSchema:
        sender_account = await self._get_account(user_id=sender_id, currency=currency)
        await self._utils.check_balance(amount=amount, balance=sender_account['balance'])
        receiver_account = await self._account_collection.find_one({'_id': ObjectId(receiver_account_id),
                                                                    'currency': currency.value})
        return await self._update_accounts_balance(
            amount=amount, desc=description, sender_account=sender_account, currency=currency,
            receiver_account=receiver_account, transaction_type=TransactionType.TRANSFER)

    async def exchange_money(self, user_id: str, amount: float,
                             from_currency: Currency, to_currency: Currency,
                             commission_service: CalculateCommissionInterface) -> ExchangeTransactionSchema:
        from_account = await self._get_account(user_id=user_id, currency=from_currency)
        await self._utils.check_balance(amount=amount, balance=from_account['balance'])
        to_account = await self._get_account(user_id=user_id, currency=to_currency)
        async with await client.start_session() as session:
            async with session.start_transaction():
                await self._update_balance(
                    filtered={'_id': from_account['_id'], 'currency': from_currency.value},
                    update={'$inc': {'balance': -amount}})
                res = await commission_service.calculate(from_currency=from_currency.value,
                                                         to_currency=to_currency.value, amount=amount)
                await self._update_balance(filtered={'_id': to_account['_id'], 'currency': to_currency.value},
                                           update={'$inc': {'balance': res}})
                data = await TransactionData().get_exchange_data(
                    amount=amount, amount_to_receiver_account=res, description=None,
                    sender_account=from_account, receiver_account=to_account, currency=from_currency,
                    to_currency=to_currency, commission=commission_service.percent,
                    transaction_type=TransactionType.EXCHANGE)
                return await self._save_transaction(**data)
