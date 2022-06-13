from .schemas import CreateAccountSchema
from .interfaces.repository_interface import AccountRepositoryInterface
from fastapi import HTTPException, status


class AccountService:
    def __init__(self, repository: AccountRepositoryInterface):
        self._repository = repository

    async def open_account(self, account_data: CreateAccountSchema, user_id: str):
        result = await self._repository \
            .open_account(user_id=user_id, **account_data.dict(exclude_none=True))
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Account not found')
        return result

    async def get_all_accounts(self, user_id: str, limit: int):
        return await self._repository.get_all_accounts(user_id=user_id, limit=limit)

    async def get_account(self, account_id: str, user_id: str):
        return await self._repository.get_account(account_id=account_id, user_id=user_id)

    async def close_account(self, account_id: str, user_id: str):
        return await self._repository.close_account(account_id=account_id, user_id=user_id)
