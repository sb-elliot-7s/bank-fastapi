from fastapi import Depends
from currency_service.cache_service import CacheService
from currency_service.repositories import CurrencyRepositories
from database import database

currency_collection = database.currencies


async def get_currency_collection():
    yield currency_collection


async def get_currency_service(_currency_collection=Depends(get_currency_collection)):
    yield {
        'repository': CurrencyRepositories(
            currency_collection=_currency_collection, cache_service=CacheService()),
    }


async def query_depends(*, from_currency: str = 'usd', to_currency: str = 'rub', amount: float = 1.0):
    return {'from_currency': from_currency, 'to_currency': to_currency, 'amount': amount}
