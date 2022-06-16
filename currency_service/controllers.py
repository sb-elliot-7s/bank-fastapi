from fastapi import APIRouter, Depends, status, HTTPException
from .cache_service import CacheService
from .deps import query_depends, get_currency_service
from .schemas import CurrencyResponseSchema, ExchangedResponseSchema
from .services import CurrencyService
from .network_service import GetExchangeService

currency_router = APIRouter(prefix='/currency', tags=['currency'])

response_data = {
    'currencies': {
        'status_code': status.HTTP_200_OK,
        'response_model': list[CurrencyResponseSchema]
    },
    'get_exchanged': {
        'status_code': status.HTTP_200_OK,
        'response_model': ExchangedResponseSchema
    }
}


# or websocket
@currency_router.get('/', **response_data.get('currencies'))
async def currencies(count: int = 1, values=Depends(get_currency_service)):
    return await CurrencyService(**values).get_currencies(count=count)


@currency_router.get('/exchange', **response_data.get('get_exchanged'))
async def get_exchanged(query: dict = Depends(query_depends)):
    if not (result := await GetExchangeService(cache_service=CacheService()).get_exchange(**query)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='something wrong')
    return result
