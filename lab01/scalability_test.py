import time
import random
from lab01 import sequential_sort, parallel_sort

def run_benchmark(data, num_processes, runs=10):
    times = []
    for _ in range(runs):
        data_copy = data.copy()
        start = time.time()
        if num_processes == 1:
            sequential_sort(data_copy)
        else:
            parallel_sort(data_copy, num_chunks=num_processes)
        end = time.time()
        times.append(end - start)
    return sum(times) / len(times)

if __name__ == "__main__":
    print("СИЛЬНА МАСШТАБОВАНІСТЬ")
    print("-" * 40)
    
    fixed_size = 100000
    test_data = [random.randint(1, 10000) for _ in range(fixed_size)]
    
    print(f"{'p':<5} | {'Tp (сек)':<10}")
    print("-" * 40)
    for p in [1, 2, 4, 8]:
        t = run_benchmark(test_data, p)
        print(f"{p:<5} | {t:<10.4f}")
    
    print("\nСЛАБКА МАСШТАБОВАНІСТЬ")
    print("-" * 40)
    
    base_size = 25000
    print(f"{'p':<5} | {'n':<10} | {'Tp (сек)':<10}")
    print("-" * 40)
    for p, size in [(1, 25000), (2, 50000), (4, 100000), (8, 200000)]:
        data = [random.randint(1, 10000) for _ in range(size)]
        t = run_benchmark(data, p)
        print(f"{p:<5} | {size:<10} | {t:<10.4f}")
