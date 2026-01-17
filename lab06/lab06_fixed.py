import asyncio

async def worker(inbox, outbox):
    while True:
        try:
            msg = await inbox.get()
            if msg is None:
                break
            await outbox.put(sorted(msg))
        except Exception as e:
            await outbox.put({"error": str(e)})

async def main():
    inbox = asyncio.Queue()
    outbox = asyncio.Queue()
    w = asyncio.create_task(worker(inbox, outbox))
    
    A = [9, 3, 7, 1, 5, 2, 8, 6, 4]
    mid = len(A) // 2
    
    await inbox.put(A[:mid])
    await inbox.put(A[mid:])
    
    # Зчитуємо оба результати 
    left = await outbox.get()
    right = await outbox.get()
    
    await inbox.put(None)
    await w
    
    print(f"Ліва частина: {left}")
    print(f"Права частина: {right}")

if __name__ == "__main__":
    asyncio.run(main())
