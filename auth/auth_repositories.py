from typing import Optional
from time import time
from datetime import datetime
from .constants import Gender
from .interfaces.auth_repository_interface import AuthRepositoriesInterface
from utils import create_slug
from uuid import uuid4


class AuthUserRepository(AuthRepositoriesInterface):
    def __init__(self, collection):
        self._collection = collection

    async def save_user(self, first_name: str, last_name: str, password: str, email: str,
                        username: Optional[str], gender: Gender) -> None:
        slug = create_slug(text=username or str(uuid4()))
        document = {
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'email': email,
            'username': username,
            'gender': gender.value,
            'unix_ts': time(),
            'created': datetime.utcnow(),
            'slug': slug
        }
        await self._collection.insert_one(document=document)

    async def get_user(self, field: str, value: str):
        return await self._collection.find_one(filter={field: value})
