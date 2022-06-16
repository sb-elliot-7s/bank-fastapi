from typing import Optional
from fastapi import APIRouter, status, Depends
from .schemas import CreateAccountSchema, AccountSchema
from .deps import get_account_repository, get_user
from .services import AccountService
from fastapi.responses import JSONResponse

account_router = APIRouter(prefix='/account', tags=['account'])

response_data = {
    'open_account': {
        'status_code': status.HTTP_201_CREATED,
        'response_model': AccountSchema,
        'response_model_by_alias': False
    },
    'get_all_accounts': {
        'status_code': status.HTTP_200_OK,
        'response_model': list[AccountSchema],
        'response_model_by_alias': False
    },
    'get_account': {
        'status_code': status.HTTP_200_OK,
        'response_model': AccountSchema,
        'response_model_by_alias': False
    },
    'close_account': {
        'status_code': status.HTTP_204_NO_CONTENT
    }
}


@account_router.post('/', **response_data.get('open_account'))
async def open_account(data: CreateAccountSchema, repository=Depends(get_account_repository),
                       user=Depends(get_user)):
    return await AccountService(**repository).open_account(account_data=data, user_id=user.id)


@account_router.get('/all', **response_data.get('get_all_accounts'))
async def get_all_accounts(limit: Optional[int] = 5, repository=Depends(get_account_repository),
                           user=Depends(get_user)):
    return await AccountService(**repository).get_all_accounts(user_id=user.id, limit=limit)


@account_router.get('/{account_id}', **response_data.get('get_account'))
async def get_account(account_id: str, repository=Depends(get_account_repository), user=Depends(get_user)):
    return await AccountService(**repository).get_account(account_id=account_id, user_id=user.id)


@account_router.delete('/{account_id}', **response_data.get('close_account'))
async def close_account(account_id: str, repository=Depends(get_account_repository), user=Depends(get_user)):
    await AccountService(**repository).close_account(account_id=account_id, user_id=user.id)
    return JSONResponse({'detail': 'Account has been deleted'})
