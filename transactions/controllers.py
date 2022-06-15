from fastapi import APIRouter, status, Depends
from .schemas import ExchangeSchema, TransferMoneySchema, TransferPhoneSchema, DepositWithdrawSchema, \
    ExchangeTransactionSchema, DepositWithdrawTransactionSchema, MoneyTransactionSchema
from .deps import get_transaction_collection
from permissions import Permission
from auth.token_service import TokenService
from .services import TransactionService
from .repositories import TransactionRepository
from account.deps import get_account_collection
from auth.deps import get_user_collection
from .constants import CommissionType
from .commission_services import WithoutCommission, Commission
from currency_service.network_service import CurrencyExchangeService

from currency_service.cache_service import CacheService

finance_router = APIRouter(prefix='/transactions', tags=['transactions'])


@finance_router.post('/', status_code=status.HTTP_201_CREATED, response_model=MoneyTransactionSchema)
async def transfer_money(
        transaction_data: TransferMoneySchema,
        transaction_collection=Depends(get_transaction_collection),
        account_collection=Depends(get_account_collection),
        user=Depends(Permission(token_service=TokenService()))):
    return await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transaction_collection)
    ).transfer_money(sender_id=user.id, transaction_data=transaction_data)


@finance_router.patch('/money', status_code=status.HTTP_200_OK,
                      response_model_by_alias=False, response_model=DepositWithdrawTransactionSchema)
async def deposit_and_withdraw_money(money: DepositWithdrawSchema,
                                     transfer_collection=Depends(get_transaction_collection),
                                     account_collection=Depends(get_account_collection),
                                     user=Depends(Permission(token_service=TokenService()))):
    return await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transfer_collection)
    ).deposit_or_withdraw_money(user_id=user.id, money=money)


@finance_router.post('/phone', status_code=status.HTTP_201_CREATED, response_model=MoneyTransactionSchema)
async def transfer_money_by_phone(
        transaction_data: TransferPhoneSchema,
        transaction_collection=Depends(get_transaction_collection),
        account_collection=Depends(get_account_collection),
        user_collection=Depends(get_user_collection),
        user=Depends(Permission(token_service=TokenService()))):
    return await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transaction_collection)
    ).transfer_money_by_phone(sender_id=user.id, transaction_data=transaction_data,
                              user_collection=user_collection)


COMMISSION_RATE = 50

commission_data = {
    CommissionType.WITHOUT_COMMISSIOn: WithoutCommission(
        currency_exchange_service=CurrencyExchangeService(cache_service=CacheService())),
    CommissionType.WITH_COMMISSION: Commission(
        currency_exchange_service=CurrencyExchangeService(cache_service=CacheService()),
        commission=COMMISSION_RATE)
}


@finance_router.post('/exchange',
                     status_code=status.HTTP_201_CREATED, response_model=ExchangeTransactionSchema)
async def exchange(exchange_data: ExchangeSchema,
                   account_collection=Depends(get_account_collection),
                   user=Depends(Permission(token_service=TokenService())),
                   transaction_collection=Depends(get_transaction_collection)):
    return await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transaction_collection
    )).exchange_money(
        user_id=user.id,
        exchange_data=exchange_data,
        commission_service=commission_data.get(CommissionType.WITH_COMMISSION))
