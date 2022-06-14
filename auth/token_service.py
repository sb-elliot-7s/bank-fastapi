import time

from .interfaces.token_service_interface import TokenServiceInterface
from jose import JWTError, jwt
from datetime import timedelta, datetime
from fastapi import HTTPException, status


class TokenService(TokenServiceInterface):

    async def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token=token, key=self.secret_key, algorithms=self.algorithm)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Not validate credentials')
        return payload

    async def create_token(self, data: dict, exp_time: int) -> str:
        payload = data.copy()
        expire_time = datetime.utcnow() + timedelta(minutes=exp_time)
        payload.update({'iat': time.time(), 'exp': expire_time})
        return jwt.encode(claims=payload, key=self.secret_key, algorithm=self.algorithm)
