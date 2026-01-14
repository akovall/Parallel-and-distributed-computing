import unittest
import threading
import time
import inspect

# Тести для багованої версії
class TestBuggedVersion(unittest.TestCase):
    
    def test_race_condition_in_bugged(self):
        import lab02bugged
        
        lab02bugged.balance = 1000
        
        threads = [
            threading.Thread(target=lab02bugged.transfer, args=(600, None)),
            threading.Thread(target=lab02bugged.transfer, args=(600, None))
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertGreaterEqual(lab02bugged.balance, 0,
            f" Баланс став від'ємним: {lab02bugged.balance}")
    
    def test_lock_not_used_in_bugged(self):
        import lab02bugged
        import dis
        import io
        import sys
        
       
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        dis.dis(lab02bugged.transfer)
        bytecode = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
      
        uses_lock = 'lock' in bytecode.lower() and ('acquire' in bytecode.lower() or 'SETUP_WITH' in bytecode or 'BEFORE_WITH' in bytecode)
        
        self.assertTrue(uses_lock,
            "Lock створено але не використовується в функції transfer")
    
    def test_unused_parameter_in_bugged(self):
        import lab02bugged
        
        params = list(inspect.signature(lab02bugged.transfer).parameters.keys())
        
        self.assertEqual(len(params), 1,
            f"Функція має зайві параметри: {params}. Очікувався лише 'amount'")


# Тести для виправленої версії
class TestFixedVersion(unittest.TestCase):
    
    def test_no_race_condition_in_fixed(self):
        import lab02fixed
        
        lab02fixed.balance = 1000
        
        threads = [
            threading.Thread(target=lab02fixed.transfer, args=(600,)),
            threading.Thread(target=lab02fixed.transfer, args=(600,))
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertGreaterEqual(lab02fixed.balance, 0,
            f" Баланс став від'ємним: {lab02fixed.balance}")
        self.assertEqual(lab02fixed.balance, 400,
            f"Очікувався баланс 400, отримано: {lab02fixed.balance}")
    
    
    def test_lock_used_in_fixed(self):
        import lab02fixed
        import dis
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        dis.dis(lab02fixed.transfer)
        bytecode = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        uses_lock = 'SETUP_WITH' in bytecode or 'BEFORE_WITH' in bytecode
        
        self.assertTrue(uses_lock,
            "Lock не використовується в функції transfer")
    
    
    def test_correct_signature_in_fixed(self):
        import lab02fixed
        
        params = list(inspect.signature(lab02fixed.transfer).parameters.keys())
        
        self.assertEqual(len(params), 1,
            f"Функція має неправильну кількість параметрів: {params}")
        self.assertEqual(params[0], 'amount',
            f"Параметр має називатися 'amount', отримано: {params[0]}")


if __name__ == "__main__":
    
    unittest.main(verbosity=2)
