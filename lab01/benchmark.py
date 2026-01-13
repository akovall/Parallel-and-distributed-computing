import time 
import random 
from lab01 import sequential_sort, parallel_sort  

if __name__ == "__main__":
    
    data_size = 100000  
    test_data = [random.randint(1, 10000) for _ in range(data_size)]  

    # Вимірювання часу послідовних версій
    print(f"Тестування на масиві з {data_size} елементів")
    print("=" * 70)
    
    
    times_sequential = []  
    print("\nПослідовна версія:")
    for i in range(10):     
        data_copy = test_data.copy() 
        start = time.time() 
        sequential_sort(data_copy) 
        end = time.time()  
        execution_time = end - start 
        times_sequential.append(execution_time)  
        print(f"  Запуск {i+1}: {execution_time:.4f} секунд")
    
  
    T1_average = sum(times_sequential) / len(times_sequential) 
    print(f"\nСереднє значення T1: {T1_average:.4f} секунд")

    
    # Вимірювання часу паралельних версій з різною кількістю процесів
    print("\n" + "=" * 70)
    print("\nПаралельні версії:")
    process_counts = [2, 4, 8]  
    results = {}  
    
    for num_processes in process_counts:  
        print(f"\n--- Кількість процесів: {num_processes} ---")
        times_parallel = []  
        
        for i in range(10): 
            data_copy = test_data.copy() 
            start = time.time() 
            parallel_sort(data_copy, num_chunks=num_processes) 
            end = time.time() 
            execution_time = end - start 
            times_parallel.append(execution_time) 
            print(f"  Запуск {i+1}: {execution_time:.4f} секунд")
        
        # Обчислення середнього Tp
        Tp_average = sum(times_parallel) / len(times_parallel)  
        results[num_processes] = Tp_average 
        print(f"  Середнє значення Tp: {Tp_average:.4f} секунд")
    
   
 


