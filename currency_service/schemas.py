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


class ExchangeCurrencySchema(BaseModel):
    from_currency: str
    to_currency: str
    exchange_rate: str

    @classmethod
    def from_raw_object(cls, data: dict):
        from_currency = data.get('1. From_Currency Code')
        to_currency = data.get('3. To_Currency Code')
        exchange_rate = data.get('5. Exchange Rate')
        return cls(from_currency=from_currency, to_currency=to_currency, exchange_rate=exchange_rate)


class ExchangedResponseSchema(ExchangeCurrencySchema):
    result: float
