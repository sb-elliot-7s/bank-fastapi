from typing import Optional

from pydantic import BaseModel, Field
from .constants import TransactionType
from datetime import datetime
from custom_objid import ObjID
from common_enums import Currency


class MoneySchema(BaseModel):
    currency: Currency
    amount: float
    transaction_type: TransactionType


class DescriptionSchema(BaseModel):
    description: Optional[str]


class CreateTransactionSchema(MoneySchema, DescriptionSchema, BaseModel):
    receiver_account_id: str


class CreatePhoneTransactionSchema(MoneySchema, DescriptionSchema, BaseModel):
    phone: int


class TransactionSchema(BaseModel):
    id: ObjID = Field(alias='_id')
    sender_account_id: str
    unix_ts: float
    transaction_datetime: datetime

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M:%s'),
            ObjID: lambda x: str(x)
        }
