#
# Task: Secure Bank Account
# Create a class BankAccount with attributes: owner, _balance.
# Methods:
#   - deposit(amount)
#   - withdraw(amount)
#   - get_balance() (getter)
# Prevent withdrawals beyond the available balance.
# Don't allow direct access to _balance.'''
#

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Amount deposited.")
        else:
            raise ValueError("No puede depositar esa cantidad.")
    def withdraw(self, amount):
        if amount >0 and amount <= self.__balance:
                self.__balance -= amount  
                print("Amount withdrawn")
        else:
            raise ValueError("No puede retirar esa cantidad.")
    def get_balance(self):
        return self.__balance
    
customer1 = BankAccount("Pedro",1000)
customer1.withdraw(500)
print(customer1.get_balance())