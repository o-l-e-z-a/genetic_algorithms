import random
import time


def get_random_indices(end, index=None):
    """Получение 2 случайных индексов (индекс 1 != индекс 2)"""
    if index:
        index_1, index_2 = index, random.randint(0, end)
    else:
        index_1, index_2 = random.randint(0, end), random.randint(0, end)

    while index_1 == index_2:  # пока индексы равны
        index_2 = random.randint(0, end)
    return index_1, index_2


def get_random_index(end, start=0):
    """ Получение случайного индекса"""
    index = random.randint(start, end)
    return index
