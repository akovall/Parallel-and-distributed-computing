from multiprocessing import Pool  # Імпорт пулу процесів для паралельних обчислень

def sort_chunk(chunk):  # Функція для сортування однієї частини масиву
    return sorted(chunk)  # Повертає відсортовану частину

def parallel_sort(arr, num_chunks=4):  # Головна функція паралельного сортування
    size = len(arr)//num_chunks  # Обчислюємо розмір кожної частини
    chunks = [arr[i*size:(i+1)*size] for i in range(num_chunks)]  # Розбиваємо масив на частини
    with Pool(num_chunks) as p:  # Створюємо пул з num_chunks процесів
        sorted_chunks = p.map(sort_chunk, chunks)  # Паралельно сортуємо кожну частину
    # Злиття відсортованих частин
    result = []  # Створюємо порожній список для результату
    for c in sorted_chunks:  # Проходимо по кожній відсортованій частині
        result.extend(c)  # Додаємо елементи частини до результату
    return sorted(result)  # Повертаємо фінально відсортований масив

def sequential_sort(arr):  # Послідовна версія сортування
    return sorted(arr)  # Повертає відсортований масив
