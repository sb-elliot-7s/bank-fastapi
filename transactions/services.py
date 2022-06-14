from .schemas import MoneySchema
from .schemas import CreateTransactionSchema, CreatePhoneTransactionSchema, ExchangeSchema
from .interfaces.repository_interface import TransactionRepositoryInterface


class TransactionService:

    def __init__(self, repository: TransactionRepositoryInterface):
        self._repository = repository

    async def transfer_money(self, sender_id: str, transaction_data: CreateTransactionSchema):
        return await self._repository.transfer_direct_money(sender_id=sender_id, **transaction_data.dict())

    async def update_balance_in_account(self, money: MoneySchema, user_id: str):
        return await self._repository.update_balance(user_id=user_id, **money.dict())

    async def transfer_money_by_phone(self, user_collection, sender_id: str,
                                      transaction_data: CreatePhoneTransactionSchema):
        return await self._repository \
            .transfer_money_by_phone(user_collection=user_collection, sender_id=sender_id,
                                     **transaction_data.dict())

    async def exchange_money(self, user_id: str, exchange_data: ExchangeSchema):
        return await self._repository.exchange_money(user_id=user_id, **exchange_data.dict())
