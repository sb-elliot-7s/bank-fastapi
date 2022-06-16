from fastapi import Depends
from passlib.context import CryptContext

from auth.auth_repositories import AuthUserRepository
from auth.password_service import PasswordService
from auth.profile_repository import ProfileRepository
from auth.tfa import TFA
from auth.token_service import TokenService
from database import database

user_collection = database.users


async def get_user_collection():
    yield user_collection


async def get_auth_service(_user_collection=Depends(get_user_collection)):
    password_service = PasswordService(context=CryptContext(schemes=['bcrypt'], deprecated='auto'))
    token_service = TokenService()

    yield {
        'repository': AuthUserRepository(collection=user_collection),
        'password_service': password_service,
        'token_service': token_service,
        'tfa_service': TFA()
    }


async def get_profile_service_data(_user_collection=Depends(get_user_collection)):
    yield {
        'repository': ProfileRepository(user_collection=_user_collection)
    }
