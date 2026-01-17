import pytest
from lamport import happens_before

#Змінити на lab04_fixed для перевірки виправленого коду
from lab04_fixed import Process  

class TestRecvOne:

    def test_recv_updates_clock(self):
        p1 = Process(1)
        p2 = Process(2)
        
        msg = p1.send_to(p2, "hello")
        assert msg.ts == 1
        
        ts_after_recv = p2.recv_one()
        
        assert ts_after_recv == 2, (
            f"Очікували ts=2, отримано {ts_after_recv}"
        )

    def test_happens_before_preserved(self):
        p1 = Process(1)
        p2 = Process(2)
        
        p1.local_event()
        msg = p1.send_to(p2, "data")
        key_send = (msg.ts, p1.clock.pid) 
        
        ts_recv = p2.recv_one() 
        key_recv = (ts_recv, p2.clock.pid) 
        
        assert happens_before(key_send, key_recv), (
            f"happens-before порушено: {key_send} < {key_recv}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
