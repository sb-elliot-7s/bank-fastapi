from fastapi import APIRouter, status, Depends, Form
from passlib.context import CryptContext

from .schemas import CreateUserSchema, Token
from .deps import get_user_collection
from .auth_services import AuthUserService
from .auth_repositories import AuthUserRepository
from .password_service import PasswordService
from .token_service import TokenService


user_routers = APIRouter(prefix='/auth', tags=['auth'])

password_service = PasswordService(context=CryptContext(schemes=['bcrypt'], deprecated='auto'))
token_service = TokenService()


@user_routers.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration(user_data: CreateUserSchema, user_collection=Depends(get_user_collection)):
    repository = AuthUserRepository(collection=user_collection)
    return await AuthUserService(repository=repository,
                                 password_service=password_service,
                                 token_service=token_service) \
        .registration(user_data=user_data)


@user_routers.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(email: str = Form(...), password: str = Form(...),
                user_collection=Depends(get_user_collection)):
    repository = AuthUserRepository(collection=user_collection)
    return await AuthUserService(repository=repository,
                                 password_service=password_service,
                                 token_service=token_service) \
        .login(email=email, password=password)
