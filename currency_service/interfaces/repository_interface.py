from abc import ABC, abstractmethod


class CurrencyRepositoryInterface(ABC):
    @abstractmethod
    async def get_currencies(self, count: int) -> list[dict]: pass

    @abstractmethod
    async def save_currencies_to_db(self, documents: dict): pass
