from fastapi import APIRouter, status, Depends
from .schemas import MoneySchema
from .schemas import CreateTransactionSchema, CreatePhoneTransactionSchema, ExchangeSchema
from .deps import get_transaction_collection
from permissions import Permission
from auth.token_service import TokenService
from .services import TransactionService
from .repositories import TransactionRepository
from account.deps import get_account_collection
from account.schemas import AccountSchema
from auth.deps import get_user_collection
from .constants import CommissionType
from .commission_services import WithoutCommission, Commission
from currency_service.network_service import CurrencyExchangeService

finance_router = APIRouter(prefix='/transactions', tags=['transactions'])


@finance_router.post('/')
async def transfer_money(
        transaction_data: CreateTransactionSchema,
        transaction_collection=Depends(get_transaction_collection),
        account_collection=Depends(get_account_collection),
        user=Depends(Permission(token_service=TokenService()))):
    await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transaction_collection)
    ).transfer_money(sender_id=user.id, transaction_data=transaction_data)


@finance_router.patch('/money', status_code=status.HTTP_200_OK,
                      response_model=AccountSchema, response_model_by_alias=False)
async def update_money_to_account(money: MoneySchema,
                                  transfer_collection=Depends(get_transaction_collection),
                                  account_collection=Depends(get_account_collection),
                                  user=Depends(Permission(token_service=TokenService()))):
    return await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transfer_collection)
    ).update_balance_in_account(user_id=user.id, money=money)


@finance_router.post('/phone')
async def transfer_money_by_phone(
        transaction_data: CreatePhoneTransactionSchema,
        transaction_collection=Depends(get_transaction_collection),
        account_collection=Depends(get_account_collection),
        user_collection=Depends(get_user_collection),
        user=Depends(Permission(token_service=TokenService()))):
    await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transaction_collection)
    ).transfer_money_by_phone(sender_id=user.id, transaction_data=transaction_data,
                              user_collection=user_collection)


COMMISSION_RATE = 50

commission_data = {
    CommissionType.WITHOUT_COMMISSIOn: WithoutCommission(currency_exchange_service=CurrencyExchangeService()),
    CommissionType.WITH_COMMISSION: Commission(currency_exchange_service=CurrencyExchangeService(),
                                               commission=COMMISSION_RATE)
}


@finance_router.post('/exchange')
async def exchange(exchange_data: ExchangeSchema,
        account_collection=Depends(get_account_collection),
        user=Depends(Permission(token_service=TokenService())),
        transaction_collection=Depends(get_transaction_collection),
):
    await TransactionService(repository=TransactionRepository(
        account_collection=account_collection, transaction_collection=transaction_collection
    )).exchange_money(
        user_id=user.id,
        exchange_data=exchange_data,
        commission_service=commission_data.get(CommissionType.WITHOUT_COMMISSIOn))
