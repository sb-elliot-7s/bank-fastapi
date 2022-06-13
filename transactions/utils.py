from fastapi import HTTPException, status


class TransactionUtils:
    @staticmethod
    async def check_balance(amount: float, balance: float):
        if balance < amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough money')
