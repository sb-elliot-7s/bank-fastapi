from .schemas import TransferPhoneSchema, DepositWithdrawSchema, TransferMoneySchema, ExchangeSchema
from .interfaces.commission_interfaces import CommissionInterface
from .interfaces.repository_interfaces import DepositOrWithdrawRepositoryInterface, \
    TransferMoneyRepositoryInterface, ExchangeMoneyRepositoryInterface


class DepositOrWithdrawService:
    def __init__(self, repository: DepositOrWithdrawRepositoryInterface):
        self._repository = repository

    async def deposit_or_withdraw_money(self, money: DepositWithdrawSchema, user_id: str):
        return await self._repository.deposit_or_withdraw_money(user_id=user_id, **money.dict())


class TransferMoneyService:
    def __init__(self, repository: TransferMoneyRepositoryInterface):
        self._repository = repository

    async def transfer_money(self, sender_id: str, transaction_data: TransferMoneySchema,
                             commission_service: CommissionInterface):
        return await self._repository.transfer_direct_money(
            sender_id=sender_id, **transaction_data.dict(), commission_service=commission_service)

    async def transfer_money_by_phone(self, user_collection, sender_id: str,
                                      commission_service: CommissionInterface,
                                      transaction_data: TransferPhoneSchema):
        return await self._repository \
            .transfer_money_by_phone(user_collection=user_collection, sender_id=sender_id,
                                     **transaction_data.dict(), commission_service=commission_service)


class ExchangeMoneyService:
    def __init__(self, repository: ExchangeMoneyRepositoryInterface):
        self._repository = repository

    async def exchange_money(self, user_id: str, exchange_data: ExchangeSchema,
                             commission_service: CommissionInterface):
        return await self._repository.exchange_money(commission_service=commission_service, user_id=user_id,
                                                     **exchange_data.dict())
