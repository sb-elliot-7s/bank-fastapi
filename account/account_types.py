from enum import Enum


class AccountType(Enum):
    BASIC = 'basic'
    MIDDLE = 'middle'
    PREMIUM = 'premium'

    @property
    def discount(self):
        return {AccountType.BASIC: 1, AccountType.MIDDLE: 0.5, AccountType.PREMIUM: 0.3}.get(self)
