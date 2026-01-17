import asyncio
import pytest

#Змінити на lab06_fixed для перевірки виправленого коду
from lab06_buggy import worker, main


class TestWorkerExceptionHandling:
    @pytest.mark.asyncio
    async def test_handles_invalid_data(self):
        inbox = asyncio.Queue()
        outbox = asyncio.Queue()
        w = asyncio.create_task(worker(inbox, outbox))
        
        await inbox.put([1, "a", None])
        await inbox.put(None)
        
        try:
            result = await asyncio.wait_for(outbox.get(), timeout=1.0)
            await w
            assert "error" in result
        except TypeError:
            pytest.fail("Worker впав без обробки винятку")


class TestMainFunction:
    @pytest.mark.asyncio
    async def test_main_reads_all_results(self, capsys):
        await main()
        captured = capsys.readouterr()
        #lab06_buggy виводить лише 1 частину, lab06_fixed - обидві
        output = captured.out
        assert output.count("[") >= 2, f"Очікувалось 2 результати, отримано: {output}"

    @pytest.mark.asyncio
    async def test_main_processes_all_data(self, capsys):
        await main()
        captured = capsys.readouterr()
        output = captured.out
        # Перевіряємо що всі елементи оброблені
        all_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for num in all_nums:
            assert str(num) in output, f"Елемент {num} відсутній у виводі: {output}"
