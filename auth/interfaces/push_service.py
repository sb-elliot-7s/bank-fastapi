from abc import ABC, abstractmethod


class PushService(ABC):
    @abstractmethod
    async def send(self, to_client, message: str) -> None: pass
