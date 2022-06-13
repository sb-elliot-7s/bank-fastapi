from .interfaces.auth_repository_interface import AuthRepositoriesInterface
from .schemas import CreateUserSchema
from .interfaces.password_service_interface import PasswordServiceInterface
from fastapi import HTTPException, status
from .interfaces.token_service_interface import TokenServiceInterface


class AuthUserService:
    def __init__(self, repository: AuthRepositoriesInterface,
                 password_service: PasswordServiceInterface,
                 token_service: TokenServiceInterface):
        self._token_service = token_service
        self._repository = repository
        self._password_service = password_service

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
        await self._repository.save_user(password=hash_password,
                                         **user_data.dict(exclude={'password'}))

    async def login(self, email: str, password: str) -> dict:
        user = await self._authenticate(email=email, password=password)
        token = await self._token_service.create_token(data={'sub': user['email']})
        return {'token': token}
