from enum import Enum


class TransactionType(Enum):
    TRANSFER = 'transfer'
    PHONE = 'phone'
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    EXCHANGE = 'exchange'


class CommissionType(Enum):
    WITHOUT_COMMISSIOn = 'without_commission'
    WITH_COMMISSION = 'with_commission'
