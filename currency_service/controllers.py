from fastapi import APIRouter, Depends, status, HTTPException

from .cache_service import CacheService
from .deps import get_currency_collection
from .schemas import CurrencyResponseSchema, ExchangedResponseSchema
from .services import CurrencyService
from .repositories import CurrencyRepositories

from .network_service import GetExchangeService

currency_router = APIRouter(prefix='/currency', tags=['currency'])


# or websocket
@currency_router.get('/', status_code=status.HTTP_200_OK, response_model=list[CurrencyResponseSchema])
async def currencies(count: int = 1, currency_collection=Depends(get_currency_collection)):
    return await CurrencyService(repository=CurrencyRepositories(
        currency_collection=currency_collection, cache_service=CacheService())
    ).get_currencies(count=count)


async def query_depends(*, from_currency: str = 'usd', to_currency: str = 'rub', amount: float = 1.0):
    return {'from_currency': from_currency, 'to_currency': to_currency, 'amount': amount}


@currency_router.get('/exchange', status_code=status.HTTP_200_OK, response_model=ExchangedResponseSchema)
async def get_exchanged(query: dict = Depends(query_depends)):
    if not (result := await GetExchangeService(cache_service=CacheService())
            .get_exchange(amount=query['amount'], from_currency=query['from_currency'],
                          to_currency=query['to_currency'])):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='something wrong')
    return result
