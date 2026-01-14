import threading
import time

balance = 1000
lock = threading.Lock()

def transfer(amount, recipient_func):
    """Баггі версія: lock не використовується, є зайвий параметр"""
    global balance
    local_balance = balance

    time.sleep(0.01)

    if local_balance >= amount:
        print(f"Потік {threading.current_thread().name} перевіряє баланс: {local_balance}")
        
        time.sleep(0.01)
        
        balance -= amount
        print(f"Потік {threading.current_thread().name} переказав {amount}. Новий баланс: {balance}")
    else:
        print(f"Потік {threading.current_thread().name} не зміг переказати {amount}. Недостатньо коштів.")


if __name__ == "__main__":
    # Створюємо два потоки, які спробують переказати гроші одночасно
    t1 = threading.Thread(target=transfer, args=(600, None), name='Потік-1')
    t2 = threading.Thread(target=transfer, args=(600, None), name='Потік-2')

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"\nКінцевий баланс: {balance}")
