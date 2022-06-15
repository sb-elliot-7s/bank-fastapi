from enum import Enum


class TransactionType(Enum):
    TRANSFER = 'transfer'
    PHONE = 'phone'
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    EXCHANGE = 'exchange'


class CommissionType(Enum):
    WITHOUT_COMMISSION = 'without_commission'
    EXCHANGE_COMMISSION = 'exchange_commission'
    TRANSFER_COMMISSION = 'transfer_commission'
