from datetime import datetime
from typing import Optional
from uuid import uuid4

from bson import ObjectId
from fastapi import HTTPException, status

from utils import create_slug
from .interfaces.repository_interface import AccountRepositoryInterface
from .schemas import AccountSchema
from common_enums import Currency


class AccountRepository(AccountRepositoryInterface):
    def __init__(self, account_collection):
        self._account_collection = account_collection

    async def _get_account_by(self, account_id: str, user_id: str):
        if not (account := await self._account_collection
                .find_one(filter={'_id': ObjectId(account_id), 'user_id': user_id})):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Account not found')
        return account

    async def open_account(self, *, balance: Optional[float] = None,
                           currency: Currency,
                           user_id: str) -> Optional[AccountSchema]:
        slug = create_slug(text=str(uuid4()))
        document = {
            'balance': balance or 0.0,
            'currency': currency.value,
            'user_id': user_id,
            'slug': slug,
            'date_opened': datetime.now()
        }
        result = await self._account_collection.insert_one(document=document)
        if not (account := await self._get_account_by(account_id=result.inserted_id,
                                                      user_id=user_id)):
            return None
        return account

    async def close_account(self, account_id: str, user_id: str) -> None:
        account = await self._get_account_by(account_id=account_id, user_id=user_id)
        _ = await self._account_collection.delete_one({'_id': account['_id']})

    async def get_account(self, account_id: str, user_id: str) -> AccountSchema:
        return await self._get_account_by(account_id=account_id, user_id=user_id)

    async def get_all_accounts(self, user_id: str, limit: int = 10) -> list[AccountSchema]:
        accounts = await self._account_collection \
            .find({'user_id': user_id}) \
            .sort('date_opened', -1) \
            .to_list(limit)
        return accounts
