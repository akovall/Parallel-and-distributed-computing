from lamport import LamportClock, Message
from typing import Any


class Process:
    def __init__(self, pid: int):
        self.clock = LamportClock(pid)
        self.inbox = []

    def local_event(self) -> int:
        return self.clock.tick()

    def send_to(self, other: "Process", payload: Any = None) -> Message:
        msg = self.clock.send(payload=payload)
        other.inbox.append(msg)
        return msg

    def recv_one(self) -> int:
        msg = self.inbox.pop(0)
        return self.clock.recv(msg)  
