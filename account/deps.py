from account.repositories import AccountRepository
from auth.token_service import TokenService
from database import database
from fastapi import Depends

from permissions import Permission

account_collection = database.accounts


async def get_account_collection():
    yield account_collection


async def get_account_repository(_account_collection=Depends(get_account_collection)):
    yield {'repository': AccountRepository(account_collection=_account_collection)}


async def get_user(user=Depends(Permission(token_service=TokenService()))):
    yield user
