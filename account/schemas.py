from typing import Optional

from pydantic import BaseModel, Field
from custom_objid import ObjID
from datetime import datetime
from common_enums import Currency


class CurrencySchema(BaseModel):
    currency: Currency


class CreateAccountSchema(CurrencySchema, BaseModel):
    balance: Optional[float]


class AccountSchema(CreateAccountSchema):
    id: ObjID = Field(alias='_id')
    slug: str
    date_opened: datetime
    # img_thumbnail: str
    user_id: str

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M'),
            ObjID: lambda x: str(x)
        }
