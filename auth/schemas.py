from datetime import datetime
from typing import Optional
from .constants import Gender
from pydantic import BaseModel, EmailStr, Field

from custom_objid import ObjID


class BaseUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    gender: Gender
    username: Optional[str]
    phone: Optional[int]


class CreateUserSchema(BaseUserSchema):
    password: str = Field(..., min_length=8)


class UpdateProfileSchema(BaseModel):
    username: Optional[str]
    birth_date: Optional[datetime]
    phone: Optional[int]


class User(UpdateProfileSchema, BaseUserSchema):
    id: ObjID = Field(alias='_id')
    unix_ts: float
    slug: str
    created: datetime

    class Config:
        json_encoders = {
            ObjID: lambda x: str(x),
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M')
        }


class Token(BaseModel):
    token: str
