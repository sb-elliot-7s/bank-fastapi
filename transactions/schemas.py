from typing import Optional

from pydantic import BaseModel, Field
from .constants import TransactionType
from datetime import datetime
from custom_objid import ObjID
from common_enums import Currency


class DescriptionSchema(BaseModel):
    description: Optional[str]


class ExchangeSchema(BaseModel):
    from_currency: Currency
    to_currency: Currency
    amount: float


class TransferPhoneSchema(DescriptionSchema, BaseModel):
    currency: Currency
    amount: float
    phone: int


class DepositWithdrawSchema(BaseModel):
    currency: Currency
    amount: float
    transaction_type: TransactionType


class TransferMoneySchema(DescriptionSchema, BaseModel):
    currency: Currency
    amount: float
    receiver_account_id: str


class TransactionSchema(BaseModel):
    id: ObjID = Field(alias='_id')
    amount: float
    currency: Currency
    transaction_type: TransactionType
    receiver_account_id: str
    sender_account_id: str
    description: Optional[str]
    unix_ts: float
    transaction_datetime: datetime
    amount_to_receiver_account: Optional[float]
    to_currency: Optional[Currency]
    commission: Optional[str]
    discount: Optional[float]

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M:%s'),
            ObjID: lambda x: str(x),
            float: lambda x: round(x, 2)
        }


class Address(BaseModel):
    country: str
    city: str
    street: str
    house: str


class InfoTransaction(BaseModel):
    balance_before_transaction: float
    balance_after_transaction: float


class DepositWithdrawTransactionSchema(TransactionSchema):
    is_atm: bool
    address_atm: Address
    result: InfoTransaction


class CurrencyInfoTransaction(InfoTransaction):
    currency: Currency


class MoneyTransactionSchema(TransactionSchema):
    balance_sender_account: CurrencyInfoTransaction
    balance_receiver_account: CurrencyInfoTransaction


class ExchangeTransactionSchema(TransactionSchema):
    to_currency: Optional[Currency]
    commission: Optional[str]
    balance_sender_account: CurrencyInfoTransaction
    balance_receiver_account: CurrencyInfoTransaction
