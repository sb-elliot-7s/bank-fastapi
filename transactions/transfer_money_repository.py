from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from common_enums import Currency
from .constants import TransactionType
from .interfaces.commission_interfaces import CommissionInterface
from .interfaces.repository_interfaces import TransferMoneyRepositoryInterface
from .schemas import MoneyTransactionSchema
from .common_repository import CommonRepository


class TransferMoneyRepository(TransferMoneyRepositoryInterface, CommonRepository):

    async def transfer_direct_money(self, sender_id: str, amount: float, currency: Currency,
                                    commission_service: CommissionInterface, receiver_account_id: str,
                                    description: Optional[str]) -> MoneyTransactionSchema:
        sender_account = await self.get_account_and_check_balance(amount, sender_id, currency)
        receiver_account = await self.get_account(
            _filter={'_id': ObjectId(receiver_account_id), 'currency': currency.value})
        return await self.update_accounts_balance(
            amount=amount, desc=description, sender_account=sender_account, currency=currency,
            receiver_account=receiver_account, transaction_type=TransactionType.TRANSFER,
            commission_service=commission_service, to_currency=currency)

    async def transfer_money_by_phone(self, user_collection, phone: int, sender_id: str, amount: float,
                                      description: Optional[str], commission_service: CommissionInterface,
                                      currency: Currency) -> MoneyTransactionSchema:
        sender_account = await self.get_account_and_check_balance(amount, sender_id, currency)
        if (user := await user_collection.find_one({'phone': phone})) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        receiver_account = await self.get_account({'user_id': str(user['_id']), 'currency': currency.value})
        return await self.update_accounts_balance(
            currency=currency, desc=description, amount=amount, sender_account=sender_account,
            receiver_account=receiver_account, transaction_type=TransactionType.PHONE,
            commission_service=commission_service, to_currency=currency)
