from fastapi import APIRouter, status, Depends, Form, Body
from passlib.context import CryptContext

from .schemas import CreateUserSchema, Token
from .deps import get_user_collection
from .auth_services import AuthUserService
from .auth_repositories import AuthUserRepository
from .password_service import PasswordService
from .token_service import TokenService

from .push_services import EmailPushService
from configs import get_configs
from .tfa import TFA
from permissions import Permission

auth_router = APIRouter(prefix='/auth', tags=['auth'])

password_service = PasswordService(context=CryptContext(schemes=['bcrypt'], deprecated='auto'))
token_service = TokenService()


@auth_router.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration(user_data: CreateUserSchema, user_collection=Depends(get_user_collection)):
    repository = AuthUserRepository(collection=user_collection)
    return await AuthUserService(repository=repository,
                                 password_service=password_service,
                                 token_service=token_service) \
        .registration(user_data=user_data)


@auth_router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(email: str = Form(...), password: str = Form(...),
                user_collection=Depends(get_user_collection)):
    repository = AuthUserRepository(collection=user_collection)
    return await AuthUserService(repository=repository,
                                 password_service=password_service,
                                 token_service=token_service,
                                 tfa_service=TFA()) \
        .login(email=email, password=password, context=EmailPushService(host=get_configs().yandex_hostname,
                                                                        port=get_configs().yandex_port,
                                                                        username=get_configs().yandex_mail,
                                                                        password=get_configs().yandex_password))


@auth_router.post('/confirm', status_code=status.HTTP_200_OK, response_model=Token)
async def confirm_code(code: str = Body(embed=True),
                       user=Depends(Permission(token_service=token_service)),
                       user_collection=Depends(get_user_collection)):
    repository = AuthUserRepository(collection=user_collection)
    return await AuthUserService(
        repository=repository,
        password_service=password_service,
        token_service=token_service,
        tfa_service=TFA()
    ).verify_code(code=code, user=user)
