"""lamport.py — Реалізація Лампортівського логічного годинника.
Ключові правила:
- Кожен процес має свій LC (ціле число, початково 0).
- Будь-яка локальна подія: LC := LC + 1.
- Перед відправленням повідомлення: LC := LC + 1; у повідомлення додається ts=LC.
- Під час приймання повідомлення з міткою t: LC := max(LC, t) + 1.
"""

from dataclasses import dataclass
from typing import Any, Tuple


@dataclass
class Message:
    src: int
    ts: int
    payload: Any = None


class LamportClock:
    def __init__(self, pid: int):
        self.pid = pid
        self.ts = 0  # логічний час

    def tick(self) -> int:
        """Правило: локальна подія."""
        self.ts += 1
        return self.ts

    def send(self, payload: Any = None) -> Message:
        """Правило: відправлення повідомлення."""
        self.ts += 1
        return Message(src=self.pid, ts=self.ts, payload=payload)

    def recv(self, msg: Message) -> int:
        """Правило: приймання повідомлення."""
        self.ts = max(self.ts, msg.ts) + 1
        return self.ts

    def order_key(self) -> Tuple[int, int]:
        """Повертає ключ впорядкування для події."""
        return (self.ts, self.pid)


def happens_before(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    """Відношення a → b за Лампортом з детермінованим tie-break."""
    return a < b
