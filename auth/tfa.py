from .interfaces.tfa_interface import TFAInterface
import pyotp
from configs import get_configs


class TFA(TFAInterface):
    def __init__(self):
        self.totp = pyotp.TOTP(get_configs().key_for_pyotp,
                               interval=get_configs().tfa_interval)

    def generate_code(self) -> str:
        return self.totp.now()

    def verify_code(self, code: str) -> bool:
        return self.totp.verify(otp=code)
