from typing import Optional

from fastapi import APIRouter, status, Depends
from .schemas import CreateAccountSchema, AccountSchema
from .deps import get_account_collection
from permissions import Permission
from auth.token_service import TokenService
from .services import AccountService
from .repositories import AccountRepository
from fastapi.responses import JSONResponse

account_routers = APIRouter(prefix='/account', tags=['account'])


@account_routers.post('/', status_code=status.HTTP_201_CREATED,
                      response_model=AccountSchema, response_model_by_alias=False)
async def open_account(
        account_data: CreateAccountSchema,
        user=Depends(Permission(token_service=TokenService())),
        account_collection=Depends(get_account_collection)
):
    return await AccountService(repository=AccountRepository(
        account_collection=account_collection)
    ).open_account(account_data=account_data, user_id=user.id)


@account_routers.get('/all', status_code=status.HTTP_200_OK,
                     response_model=list[AccountSchema], response_model_by_alias=False)
async def get_all_accounts(limit: Optional[int] = 5, account_collection=Depends(get_account_collection),
                           user=Depends(Permission(token_service=TokenService()))):
    return await AccountService(repository=AccountRepository(
        account_collection=account_collection)
    ).get_all_accounts(user_id=user.id, limit=limit)


@account_routers.get('/{account_id}', status_code=status.HTTP_200_OK,
                     response_model=AccountSchema)
async def get_account(account_id: str, account_collection=Depends(get_account_collection),
                      user=Depends(Permission(token_service=TokenService())), ):
    return await AccountService(repository=AccountRepository(
        account_collection=account_collection)
    ).get_account(account_id=account_id, user_id=user.id)


@account_routers.delete('/{account_id}', status_code=status.HTTP_204_NO_CONTENT)
async def close_account(account_id: str, account_collection=Depends(get_account_collection),
                        user=Depends(Permission(token_service=TokenService()))):
    await AccountService(repository=AccountRepository(
        account_collection=account_collection)
    ).close_account(account_id=account_id, user_id=user.id)
    return JSONResponse({'detail': 'Account has been deleted'})
