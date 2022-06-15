from datetime import datetime
from time import time
from typing import Optional
from common_enums import Currency
from .constants import TransactionType
from .interfaces.repository_interfaces import TransactionRepositoryInterface
from bson import ObjectId


class TransactionRepository(TransactionRepositoryInterface):
    def __init__(self, transaction_collection):
        self._transaction_collection = transaction_collection

    async def save_transaction(self, amount: float, sender_account_id: str, receiver_account_id: str,
                               currency: Currency, transaction_type: TransactionType, commission: float,
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
            'commission': commission,
            **others
        }
        result = await self._transaction_collection.insert_one(document=document)
        return await self._transaction_collection.find_one({'_id': ObjectId(result.inserted_id)})
