import json

from .interfaces.repository_interface import CurrencyRepositoryInterface
import aioredis
from .schemas import CurrencyResponseSchema


class CurrencyRepositories(CurrencyRepositoryInterface):
    def __init__(self, currency_collection):
        self._currency_collection = currency_collection

    async def save_currencies_to_db(self, documents: dict):
        await self._currency_collection.insert_one(document=documents)

    async def get_currencies(self, count: int):
        key = 'currency'
        redis = aioredis.from_url(url='redis://localhost', decode_responses=True)
        cache = await redis.get(key)
        if cache is None:
            currencies_raw = await self._currency_collection.find({}, sort=[('created', -1)]) \
                .to_list(length=count)
            currencies = [CurrencyResponseSchema(**a).dict() for a in currencies_raw]
            await redis.set(name=key, value=json.dumps(currencies, sort_keys=True, default=str), ex=60)
            return currencies
        return json.loads(cache)
