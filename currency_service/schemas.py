from datetime import datetime

from pydantic import BaseModel


class CurrencySchema(BaseModel):
    title: str
    bid: str
    ask: str
    change_in_value: str
    change_in_procent: str
    dt: str
    unix_ts: str


class CurrencyResponseSchema(BaseModel):
    created: datetime
    values: list[CurrencySchema]

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y-%d-%m %H:%M:%S')
        }
