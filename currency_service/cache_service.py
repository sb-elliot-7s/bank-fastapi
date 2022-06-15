from datetime import timedelta
from typing import Union
from .interfaces.cache_service_interface import CacheServiceInterface
import aioredis


class CacheService(CacheServiceInterface):

    def __init__(self):
        self.redis = aioredis.from_url(url='redis://localhost', decode_responses=True)

    async def get_from_cache(self, key: str):
        await self.redis.get(name=key)

    async def set_to_cache(self, key: str, value: Union[bytes, str, int, float],
                           exp_time: Union[int, timedelta]):
        await self.redis.set(name=key, value=value, ex=exp_time)
