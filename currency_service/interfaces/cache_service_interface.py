from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Union


class CacheServiceInterface(ABC):
    @abstractmethod
    async def get_from_cache(self, key: str): pass

    @abstractmethod
    async def set_to_cache(self, key: str,
                           value: Union[bytes, str, int, float], exp_time: Union[int, timedelta]): pass
