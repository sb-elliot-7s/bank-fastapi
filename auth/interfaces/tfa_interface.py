from abc import ABC, abstractmethod


class TFAInterface(ABC):
    @abstractmethod
    def generate_code(self) -> str: pass

    @abstractmethod
    def verify_code(self, code: str) -> bool: pass
