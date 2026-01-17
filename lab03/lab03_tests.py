import threading
import pytest
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

#Змінити на lab03_fixed для перевірки виправленого коду
from lab03_buggy import Account, TransferOperation


#Deadlock через випадковий порядок замків
def test_no_deadlock():
    def run_transfers():
        acc1, acc2 = Account("A", 1000), Account("B", 1000)
        op1, op2 = TransferOperation(acc1, acc2, 50), TransferOperation(acc2, acc1, 30)
        t1, t2 = threading.Thread(target=op1.run), threading.Thread(target=op2.run)
        t1.start(); t2.start()
        t1.join(timeout=1.0); t2.join(timeout=1.0)
        return not (t1.is_alive() or t2.is_alive())
    
    for _ in range(10):
        with ThreadPoolExecutor(max_workers=1) as ex:
            try:
                assert ex.submit(run_transfers).result(timeout=3.0), "Deadlock!"
            except FuturesTimeoutError:
                pytest.fail("Deadlock виявлено!")

# Результат операції повинен бути перевіряємим
def test_operation_returns_result():
    acc1, acc2 = Account("A", 100), Account("B", 100)
    op = TransferOperation(acc1, acc2, 30)
    result = op.run()
    assert result is not None, "run() повинен повертати результат операції"

#Валідація балансу
def test_balance_validation():
    acc1, acc2 = Account("A", 50), Account("B", 100)
    op = TransferOperation(acc1, acc2, 100)
    op.run()
    assert acc1.balance >= 0, f"Баланс від'ємний: {acc1.balance}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
