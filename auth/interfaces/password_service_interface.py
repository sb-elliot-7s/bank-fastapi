from abc import ABC, abstractmethod


class PasswordServiceInterface(ABC):
    @abstractmethod
    async def get_hashed_password(self, password: str) -> str: pass

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
