from fastapi import APIRouter, Depends, status
from .deps import get_currency_collection
from .schemas import CurrencyResponseSchema
from .services import CurrencyService
from .repositories import CurrencyRepositories

from .network_service import CurrencyExchangeService

currency_router = APIRouter(prefix='/currency', tags=['currency'])


# or websocket
@currency_router.get('/', status_code=status.HTTP_200_OK, response_model=list[CurrencyResponseSchema])
async def currencies(count: int = 1, currency_collection=Depends(get_currency_collection)):
    return await CurrencyService(repository=CurrencyRepositories(
        currency_collection=currency_collection)
    ).get_currencies(count=count)


@currency_router.get('/exc', status_code=status.HTTP_200_OK)
async def currencies(from_currency: str = 'usd', to_currency: str = 'rub'):
    return await CurrencyExchangeService().exchange_rate(from_currency=from_currency, to_currency=to_currency)
