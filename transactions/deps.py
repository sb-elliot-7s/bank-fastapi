from account.deps import get_account_collection
from database import database
from .transaction_repository import TransactionRepository
from fastapi import Depends

transaction_collection = database.transactions


async def get_transaction_collection():
    yield transaction_collection


async def get_account_and_transaction_collections(account_collection=Depends(get_account_collection),
                                                  transaction_collection=Depends(get_transaction_collection)):
    yield {
        'transaction_repository': TransactionRepository(transaction_collection=transaction_collection),
        'account_collection': account_collection
    }
