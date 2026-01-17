import asyncio

async def worker(inbox, outbox):
    while True:
        msg = await inbox.get()
        if msg is None:
            break
        outbox.put_nowait(sorted(msg))

async def main():
    inbox = asyncio.Queue()
    outbox = asyncio.Queue()
    w = asyncio.create_task(worker(inbox, outbox))
    A = [9, 3, 7, 1, 5, 2, 8, 6, 4]
    mid = len(A) // 2
    await inbox.put(A[:mid])
    await inbox.put(A[mid:])
    await inbox.put(None)
    left = await outbox.get()
    print(left)
    await w

if __name__ == "__main__":
    asyncio.run(main())
