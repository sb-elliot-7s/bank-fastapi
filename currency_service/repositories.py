import json

from .cache_service import CacheService
from .interfaces.repository_interface import CurrencyRepositoryInterface
from .schemas import CurrencyResponseSchema


class CurrencyRepositories(CurrencyRepositoryInterface):
    def __init__(self, currency_collection, cache_service: CacheService):
        self._cache_service = cache_service
        self._currency_collection = currency_collection

    async def save_currencies_to_db(self, documents: dict):
        await self._currency_collection.insert_one(document=documents)

    async def get_currencies(self, count: int):
        cache = await self._cache_service.get_from_cache(key='currency')
        if cache is None:
            currencies_raw = await self._currency_collection. \
                find({}, sort=[('created', -1)]) \
                .to_list(length=count)
            currencies = [CurrencyResponseSchema(**currency).dict() for currency in currencies_raw]
            await self._cache_service.set_to_cache(key='currency',
                                                   value=json.dumps(currencies, sort_keys=True, default=str),
                                                   exp_time=600)
            return currencies
        return json.loads(cache)
