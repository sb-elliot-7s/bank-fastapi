from enum import Enum


class TransactionType(Enum):
    TRANSFER = 'transfer'
    PHONE = 'phone'
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
