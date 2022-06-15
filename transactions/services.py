from .schemas import TransferPhoneSchema, DepositWithdrawSchema, TransferMoneySchema, ExchangeSchema
from .interfaces.repository_interface import TransactionRepositoryInterface
from .interfaces.commission_interfaces import CalculateCommissionInterface


class TransactionService:

    def __init__(self, repository: TransactionRepositoryInterface):
        self._repository = repository

    async def transfer_money(self, sender_id: str, transaction_data: TransferMoneySchema):
        return await self._repository.transfer_direct_money(sender_id=sender_id, **transaction_data.dict())

    async def deposit_or_withdraw_money(self, money: DepositWithdrawSchema, user_id: str):
        return await self._repository.deposit_or_withdraw_money(user_id=user_id, **money.dict())

    async def transfer_money_by_phone(self, user_collection, sender_id: str,
                                      transaction_data: TransferPhoneSchema):
        return await self._repository \
            .transfer_money_by_phone(user_collection=user_collection, sender_id=sender_id,
                                     **transaction_data.dict())

    async def exchange_money(self, user_id: str, exchange_data: ExchangeSchema,
                             commission_service: CalculateCommissionInterface):
        return await self._repository.exchange_money(commission_service=commission_service, user_id=user_id,
                                                     **exchange_data.dict())
