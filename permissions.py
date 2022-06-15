from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from auth.interfaces.token_service_interface import TokenServiceInterface
from auth.deps import get_user_collection
from auth.schemas import User


class Permission:
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='auth/login')

    def __init__(self, token_service: TokenServiceInterface):
        self._token_service = token_service

    async def __call__(self, user_collection=Depends(get_user_collection),
                       token: str = Depends(OAUTH2_SCHEME)):
        payload = await self._token_service.decode_token(token=token)
        if not (email := payload.get('sub')):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return User(**await user_collection.find_one(filter={'email': email}))
