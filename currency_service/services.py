from .interfaces.repository_interface import CurrencyRepositoryInterface


class CurrencyService:
    def __init__(self, repository: CurrencyRepositoryInterface):
        self.repository = repository

    async def get_currencies(self, count: int):
        return await self.repository.get_currencies(count=count)
