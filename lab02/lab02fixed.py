import threading
import time


balance = 1000

lock = threading.Lock()

def transfer(amount):
    global balance

    # Захоплюється блокування — тільки один потік може виконувати цей блок одночасно (це фікс)
    with lock:
        local_balance = balance
        
        time.sleep(0.01)
        
        if local_balance >= amount:
            # Виводиться повідомлення про перевірку балансу
            print(f"Потік {threading.current_thread().name} перевіряє баланс: {local_balance}")
            
            # Імітується затримка при обробці транзакції
            time.sleep(0.01)
            
            # Виконується списання коштів з глобального балансу
            balance -= amount
            # Виводиться повідомлення про успішний переказ
            print(f"Потік {threading.current_thread().name} переказав {amount}. Новий баланс: {balance}")
        else:
            # Виводиться повідомлення про відмову через недостатність коштів
            print(f"Потік {threading.current_thread().name} не зміг переказати {amount}. Недостатньо коштів.")


if __name__ == "__main__":
    t1 = threading.Thread(target=transfer, args=(600,), name="Потік-1")
    t2 = threading.Thread(target=transfer, args=(600,), name="Потік-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print(f"\nПідсумковий баланс: {balance}")
