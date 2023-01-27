import random
from math import inf


def get_key(key, gens):
    """ Увеличение длины ключа до длины генов """
    gens_length = len(gens)
    div = gens_length // len(key)
    mod = gens_length % len(key)
    key *= div
    key += key[:mod]
    return key


def find_lower_path_city(current_node, not_visited):
    """ Поиск минимального пути при помощи жадного алгоритма"""
    lowest_path = inf
    city_with_lowest_path = None
    for city, path in enumerate(current_node):
        if 0 < path < lowest_path and city in not_visited:
            lowest_path = path
            city_with_lowest_path = city
    return city_with_lowest_path


def find_most_high_path_city(current_node, not_visited):
    """ Поиск максимального пути при помощи жадного алгоритма"""
    most_high_path = -inf
    city_with_most_high_path = None
    for city, path in enumerate(current_node):
        if path > most_high_path and path > 0 and city in not_visited:
            most_high_path = path
            city_with_most_high_path = city
    return city_with_most_high_path


def random_path_city(current_node, not_visited):
    """ Поиск случайного пути при помощи жадного алгоритма"""
    random_path = random.choice(not_visited)
    return random_path


CHOICE_OF_ALGORITHMS = {'1': find_lower_path_city, '2': find_most_high_path_city, '3': random_path_city}


class FormStartGenes:
    """ Формирование начальных генов при помощи жадных эвристик"""

    def __init__(self, key, matrix, individual):
        self._key = get_key(key, individual)
        self._genes = []
        self._not_visited = list(range(len(individual)))
        self._key_index = 0
        self._matrix = matrix


    def get_formed_initial_genes(self, start_city=None):
        """ Формирование начальных генов с помощью жадных эвристик"""
        city = start_city if start_city else random.choice(self._not_visited)
        while len(self._not_visited) > 1:
            current_node = self.get_current_node(city)
            self.update_lists(city)
            city = self.get_next_city(current_node)
        else:
            self.update_lists(city)
        return self._genes

    def get_current_node(self, city):
        """ Получение текущего узла"""
        return self._matrix[city]

    def update_lists(self, city):
        """ Обновление списка генов и непосещённых городов """
        self._genes.append(city)
        self._not_visited.remove(city)

    def get_next_city(self, current_node):
        """ Получение следующего города"""
        city = CHOICE_OF_ALGORITHMS[self._key[self._key_index]](current_node, self._not_visited)
        self._key_index += 1
        return city
