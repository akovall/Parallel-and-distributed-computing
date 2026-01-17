import pytest
import sys
from unittest.mock import MagicMock

sys.modules['kafka'] = MagicMock()
sys.modules['kafka.errors'] = MagicMock()

#Змінити на lab05_buggy для перевірки багованого коду
from lab05_fixed import consume_task

try:
    from lab05_fixed import dead_letter_queue
    HAS_DLQ = True
except ImportError:
    dead_letter_queue = None
    HAS_DLQ = False

import inspect


class TestAutoCommitDisabled:
    def test_auto_commit_should_be_disabled(self):
        source = inspect.getsource(consume_task)
        has_auto_commit_false = 'enable_auto_commit=False' in source
        assert has_auto_commit_false, "enable_auto_commit має бути False"


class TestExplicitCommit:
    def test_explicit_commit_after_processing(self):
        source = inspect.getsource(consume_task)
        lines = source.split('\n')
        found_commit = False
        for i, line in enumerate(lines):
            if 'process_message(message)' in line:
                for j in range(i + 1, min(i + 5, len(lines))):
                    if 'consumer.commit()' in lines[j]:
                        found_commit = True
                        break
        assert found_commit, "Має бути явний commit() після обробки"


class TestConsumerGroupId:
    def test_single_group_id_for_all_consumers(self):
        source = inspect.getsource(consume_task)
        has_dynamic_group = 'group_id=f"' in source or "group_id=f'" in source
        assert not has_dynamic_group, "group_id не має бути динамічним"


class TestDeadLetterQueue:
    def test_dlq_implemented(self):
        assert HAS_DLQ, "DLQ має бути реалізована"
        source = inspect.getsource(consume_task)
        assert 'dead_letter_queue' in source, "Має використовуватись dead_letter_queue"


class TestNoRandomSeek:
    def test_no_random_seek(self):
        source = inspect.getsource(consume_task)
        has_seek = 'consumer.seek' in source
        has_random_condition = 'random.random()' in source and 'seek' in source
        assert not (has_seek and has_random_condition), "Не має бути випадкового seek()"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
