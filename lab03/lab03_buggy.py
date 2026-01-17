import threading, time, random

class TransferOperation:
    def __init__(self, from_account, to_account, amount):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def run(self):
        # Імітуємо випадковий порядок отримання замків
        if random.random() < 0.5:
            lock1, lock2 = self.from_account.lock, self.to_account.lock
        else:
            lock1, lock2 = self.to_account.lock, self.from_account.lock

        with lock1:
            time.sleep(0.01)
            with lock2:
                self.from_account.balance -= self.amount
                self.to_account.balance += self.amount
                print(f"Transfer from {self.from_account.name} to {self.to_account.name} successful.")

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.lock = threading.Lock()

account1 = Account("Alice", 100)
account2 = Account("Bob", 200)

op1 = TransferOperation(account1, account2, 50)
op2 = TransferOperation(account2, account1, 30)

t1 = threading.Thread(target=op1.run)
t2 = threading.Thread(target=op2.run)

t1.start()
t2.start()

print("Launched threads. If a deadlock occurs, this message will appear, but the program will not finish.")
