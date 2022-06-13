from database import database

account_collection = database.accounts


async def get_account_collection():
    yield account_collection
