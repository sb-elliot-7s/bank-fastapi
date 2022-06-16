import json
from .interfaces.auth_repository_interface import AuthRepositoriesInterface
from .schemas import CreateUserSchema
from .interfaces.password_service_interface import PasswordServiceInterface
from fastapi import HTTPException, status
from .interfaces.token_service_interface import TokenServiceInterface
from .interfaces.tfa_interface import TFAInterface
from configs import get_configs
from .app import push_service_topic


class AuthUserService:
    def __init__(self, repository: AuthRepositoriesInterface, password_service: PasswordServiceInterface,
                 token_service: TokenServiceInterface, tfa_service: TFAInterface = None):
        self._token_service = token_service
        self._repository = repository
        self._password_service = password_service
        self.tfa_service = tfa_service

    async def _authenticate(self, email: str, password: str):
        if not (user := await self._repository.get_user(field='email', value=email)) or \
                not await self._password_service.verify_password(plain_password=password,
                                                                 hashed_password=user['password']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Incorrect username or password')
        return user

    async def registration(self, user_data: CreateUserSchema):
        if await self._repository.get_user(field='email', value=user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='User with this email exists')
        hash_password = await self._password_service. \
            get_hashed_password(password=user_data.password)
        await self._repository.save_user(password=hash_password, **user_data.dict(exclude={'password'}))

    async def login(self, email: str, password: str) -> dict:
        user = await self._authenticate(email=email, password=password)
        code = self.tfa_service.generate_code()
        temporary_token = await self._token_service \
            .create_token(data={'sub': user['email']}, exp_time=get_configs().temporary_token_exp_time)
        await push_service_topic.send(value=json.dumps({'email': user['email'], 'code': code}).encode())
        return {'token': temporary_token}

    async def verify_code(self, code: str, user):
        if not self.tfa_service.verify_code(code=code):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Code not valid')
        token = await self._token_service \
            .create_token(data={'sub': user.email}, exp_time=get_configs().exp_time)
        return {'token': token}
