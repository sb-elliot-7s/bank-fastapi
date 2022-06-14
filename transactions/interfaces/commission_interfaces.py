from abc import ABC, abstractmethod


class CalculateCommissionInterface(ABC):
    @abstractmethod
    async def calculate(self, from_currency: str, to_currency: str, amount: float):
        pass
