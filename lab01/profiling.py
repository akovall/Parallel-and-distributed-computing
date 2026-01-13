import time
import random
from multiprocessing import Pool

if __name__ == "__main__":
    data = [random.randint(1, 10000) for _ in range(100000)]

    print("ПОСЛІДОВНА")
    t0 = time.time()
    d = data.copy()
    t1 = time.time()
    r = sorted(d)
    t2 = time.time()
    total = t2 - t0
    print(f"Копіювання: {(t1-t0)/total*100:.1f}%")
    print(f"Сортування: {(t2-t1)/total*100:.1f}%")
    print(f"Всього: {total*1000:.1f} мс")

    print("\nПАРАЛЕЛЬНА (4 проц)")
    t0 = time.time()
    d = data.copy()
    t1 = time.time()
    chunks = [d[i*25000:(i+1)*25000] for i in range(4)]
    t2 = time.time()
    with Pool(4) as p:
        res = p.map(sorted, chunks)
    t3 = time.time()
    merged = []
    for c in res:
        merged.extend(c)
    t4 = time.time()
    final = sorted(merged)
    t5 = time.time()
    total = t5 - t0
    
    print(f"Копіювання: {(t1-t0)/total*100:.1f}%")
    print(f"Розбиття: {(t2-t1)/total*100:.1f}%")
    print(f"Pool.map: {(t3-t2)/total*100:.1f}%")
    print(f"Злиття: {(t4-t3)/total*100:.1f}%")
    print(f"Фін.сорт: {(t5-t4)/total*100:.1f}%")
    print(f"Всього: {total*1000:.1f} мс")
