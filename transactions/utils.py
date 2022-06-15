from typing import Optional

from fastapi import HTTPException, status

from common_enums import Currency
from .constants import TransactionType


class TransactionUtils:
    @staticmethod
    async def check_balance(amount: float, balance: float):
        if balance < amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough money')


class TransactionData:

    @staticmethod
    async def get_common_data(amount: float, amount_to_receiver_account: float, description: Optional[str],
                              currency: Currency, transaction_type: TransactionType, sender_account: dict,
                              receiver_account: dict, commission: float, ):
        return {
            'amount': amount,
            'amount_to_receiver_account': amount_to_receiver_account,
            'currency': currency,
            'description': description,
            'transaction_type': transaction_type,
            'sender_account_id': str(sender_account['_id']),
            'receiver_account_id': str(receiver_account['_id']),
            'commission': commission,
        }

    @staticmethod
    async def other_common_data(currency: Currency, to_currency: Currency,
                                sender_account: dict, receiver_account: dict, amount: float,
                                amount_to_receiver_account: float):
        return {
            'to_currency': to_currency.value,
            'balance_sender_account': {
                'currency': currency.value,
                'balance_before_transaction': round(sender_account['balance'], 2),
                'balance_after_transaction': round(sender_account['balance'], 2) - amount
            },
            'balance_receiver_account': {
                'currency': to_currency.value,
                'balance_before_transaction': round(receiver_account['balance'], 2),
                'balance_after_transaction': round(receiver_account['balance'],
                                                   2) + amount_to_receiver_account
            }
        }

    @staticmethod
    async def get_deposit_or_withdraw_data(amount: float, transaction_type: TransactionType,
                                           currency: Currency, account_before_update: dict,
                                           account_after_update: dict, commission: float):
        is_withdraw = transaction_type == TransactionType.WITHDRAW
        _amount = -amount if is_withdraw else amount
        return {
            'amount': _amount,
            'currency': currency,
            'transaction_type': transaction_type,
            'sender_account_id': str(account_after_update['_id']) if is_withdraw else 'ATM',
            'receiver_account_id': 'ATM' if is_withdraw else str(account_after_update['_id']),
            'description': None,
            'amount_to_receiver_account': _amount,
            'commission': commission,
            **{
                'is_atm': True,
                'address_atm': {'country': '', 'city': '', 'street': '', 'house': ''},
                'result': {
                    'balance_before_transaction': round(account_before_update['balance'], 2),
                    'balance_after_transaction': round(account_before_update['balance'], 2) + _amount}
            }
        }

    async def get_transfer_data(self, amount: float, currency: Currency, desc: Optional[str],
                                sender_account: dict, receiver_account: dict, to_currency: Currency,
                                amount_to_receiver_account: float, transaction_type: TransactionType,
                                commission: float):
        data = await self.get_common_data(
            amount=-amount, amount_to_receiver_account=amount_to_receiver_account, currency=currency,
            description=desc, transaction_type=transaction_type, sender_account=sender_account,
            receiver_account=receiver_account, commission=commission)
        other_data = await self.other_common_data(currency=currency, to_currency=to_currency,
                                                  sender_account=sender_account,
                                                  receiver_account=receiver_account, amount=amount,
                                                  amount_to_receiver_account=amount_to_receiver_account)
        return {**data, **other_data}

    # async def get_exchange_data(self, amount: float, amount_to_receiver_account: float,
    #                             description: Optional[str], currency: Currency, to_currency: Currency,
    #                             commission: float, sender_account: dict, receiver_account: dict,
    #                             transaction_type: TransactionType):
    #     data = await self.get_common_data(
    #         commission=commission, amount=-amount, amount_to_receiver_account=amount_to_receiver_account,
    #         description=description, currency=currency, transaction_type=transaction_type,
    #         sender_account=sender_account, receiver_account=receiver_account)
    #     other_data = await self.other_common_data(currency=currency, to_currency=to_currency,
    #                                               sender_account=sender_account,
    #                                               receiver_account=receiver_account, amount=amount,
    #                                               amount_to_receiver_account=amount_to_receiver_account)
    #     return {**data, **other_data, 'commission': commission}
