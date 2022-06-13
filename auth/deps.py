from database import database

user_collection = database.users


async def get_user_collection():
    yield user_collection
