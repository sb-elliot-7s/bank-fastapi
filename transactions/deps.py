from database import database

transaction_collection = database.transactions


async def get_transaction_collection():
    yield transaction_collection
