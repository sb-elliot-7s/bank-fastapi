from abc import ABC, abstractmethod
from configs import get_configs


class TokenServiceInterface(ABC):
    def __init__(self):
        self.secret_key = get_configs().secret_key
        self.algorithm = get_configs().algorithm

    @abstractmethod
    async def decode_token(self, token: str) -> dict:
        pass

    @abstractmethod
    async def create_token(self, data: dict, exp_time: int) -> str:
        pass
