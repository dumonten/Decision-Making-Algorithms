from numpy import random
from time import perf_counter

arr = []
dct = {}

t0 = perf_counter()
for i in range(1_000_0000):
    dct[i] = random.randint(0, 100)
t1 = perf_counter()
print(f"Добавление в словарь 100_000 элементов: {t1 - t0}с")

t0 = perf_counter()
for i in range(100_000):
    arr.append(random.randint(0, 100))
t1 = perf_counter()
print(f"Добавление в массив 100_000 элементов: {t1 - t0}с")

t0 = perf_counter()
for i in range(100_000 - 1, 0):
    del dct[i]
t1 = perf_counter()
print(f"Удаление из словаря 100_000 элементов: {t1 - t0}с")

t0 = perf_counter()
for i in range(100_000 - 1, 0):
    arr.pop()
t1 = perf_counter()
print(f"Удаление из массива 100_000 элементов: {t1 - t0}с")