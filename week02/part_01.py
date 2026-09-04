class NotEnoughMoneyError(Exception):
    pass
def withdraw(balance,amount):
    if amount < 0:
        raise ValueError(f"amount:{amount}不能小于零")
    if amount > balance:
        raise NotEnoughMoneyError(f"余额:{balance}不足,买不了{amount}的东西")
    print(f"剩余:{balance-amount}")
try:
    withdraw(100,-5)
except ValueError as e:
    print(e)
except NotEnoughMoneyError as e:
    print(e)
