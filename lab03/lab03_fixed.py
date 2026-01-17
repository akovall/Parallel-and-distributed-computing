import threading
import time

class TransferOperation:
    def __init__(self, from_account, to_account, amount):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def run(self):
        #Фіксований порядок замків за id()
        if id(self.from_account) < id(self.to_account):
            lock1, lock2 = self.from_account.lock, self.to_account.lock
        else:
            lock1, lock2 = self.to_account.lock, self.from_account.lock

        #sleep() винесено за межі критичної секції
        time.sleep(0.01)
        
        with lock1:
            with lock2:
                #Перевірка балансу
                if self.from_account.balance >= self.amount:
                    self.from_account.balance -= self.amount
                    self.to_account.balance += self.amount
                    return True
                return False

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.lock = threading.Lock()

if __name__ == "__main__":
    account1 = Account("Alice", 100)
    account2 = Account("Bob", 200)

    op1 = TransferOperation(account1, account2, 50)
    op2 = TransferOperation(account2, account1, 30)

    t1 = threading.Thread(target=op1.run)
    t2 = threading.Thread(target=op2.run)

    t1.start()
    t2.start()

    #Очікування завершення потоків
    t1.join()
    t2.join()

    print(f"Alice: {account1.balance}, Bob: {account2.balance}")
