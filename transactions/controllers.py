from fastapi import APIRouter, status, Depends
from .schemas import ExchangeSchema, TransferMoneySchema, TransferPhoneSchema, DepositWithdrawSchema, \
    ExchangeTransactionSchema, DepositWithdrawTransactionSchema, MoneyTransactionSchema
from .deps import get_account_and_transaction_collections
from permissions import Permission
from auth.token_service import TokenService
from .services import DepositOrWithdrawService, ExchangeMoneyService, TransferMoneyService
from auth.deps import get_user_collection
from .constants import CommissionType
from .commission_services import WithoutCommission, ExchangeCommission, TransferCommission
from currency_service.network_service import CurrencyExchangeService
from .exchange_repository import ExchangeMoneyRepository
from .deposit_or_withdraw_repository import DepositOrWithdrawRepository
from .transfer_money_repository import TransferMoneyRepository

from currency_service.cache_service import CacheService

finance_router = APIRouter(prefix='/transactions', tags=['transactions'])

EXCHANGE_COMMISSION_RATE = 20.0
TRANSFER_COMMISSION_RATE = 10.0

commission_data = {
    CommissionType.WITHOUT_COMMISSION: WithoutCommission(
        currency_exchange_service=CurrencyExchangeService(cache_service=CacheService())),
    CommissionType.EXCHANGE_COMMISSION: ExchangeCommission(
        currency_exchange_service=CurrencyExchangeService(cache_service=CacheService()),
        commission=EXCHANGE_COMMISSION_RATE),
    CommissionType.TRANSFER_COMMISSION: TransferCommission(commission=TRANSFER_COMMISSION_RATE)
}

response_model = {
    'exchange_response': ExchangeTransactionSchema,
    'transfer_response': MoneyTransactionSchema,
    'deposit_response': DepositWithdrawTransactionSchema,
}
response_attrs = {
    'status_code': status.HTTP_201_CREATED,
    'response_model_by_alias': False
}


@finance_router.post('/', response_model=response_model.get('transfer_response'), **response_attrs)
async def transfer_money(
        transaction_data: TransferMoneySchema, collections=Depends(get_account_and_transaction_collections),
        user=Depends(Permission(token_service=TokenService()))):
    return await TransferMoneyService(repository=TransferMoneyRepository(**collections)) \
        .transfer_money(sender_id=user.id, transaction_data=transaction_data,
                        commission_service=commission_data.get(CommissionType.TRANSFER_COMMISSION))


@finance_router.patch('/money', response_model=response_model.get('deposit_response'), **response_attrs)
async def deposit_and_withdraw_money(
        money: DepositWithdrawSchema, user=Depends(Permission(token_service=TokenService())),
        collections=Depends(get_account_and_transaction_collections)):
    return await DepositOrWithdrawService(repository=DepositOrWithdrawRepository(**collections)) \
        .deposit_or_withdraw_money(money=money, user_id=user.id)


@finance_router.post('/phone', response_model=response_model.get('transfer_response'), **response_attrs)
async def transfer_money_by_phone(
        transaction_data: TransferPhoneSchema, collections=Depends(get_account_and_transaction_collections),
        user_collection=Depends(get_user_collection), user=Depends(Permission(token_service=TokenService()))):
    return await TransferMoneyService(repository=TransferMoneyRepository(**collections)) \
        .transfer_money_by_phone(sender_id=user.id, transaction_data=transaction_data,
                                 user_collection=user_collection,
                                 commission_service=commission_data.get(CommissionType.TRANSFER_COMMISSION))


@finance_router.post('/exchange', response_model=response_model.get('exchange_response'), **response_attrs)
async def exchange(
        exchange_data: ExchangeSchema, collections=Depends(get_account_and_transaction_collections),
        user=Depends(Permission(token_service=TokenService()))):
    return await ExchangeMoneyService(repository=ExchangeMoneyRepository(**collections)) \
        .exchange_money(user_id=user.id, exchange_data=exchange_data,
                        commission_service=commission_data.get(CommissionType.EXCHANGE_COMMISSION))
