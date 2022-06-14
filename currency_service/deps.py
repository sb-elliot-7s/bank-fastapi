from database import database

currency_collection = database.currencies


async def get_currency_collection():
    yield currency_collection
