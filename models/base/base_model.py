from typing import Any, Union, Callable

from base_crossover import BaseCrossover
from base_fitness_function import BaseFitnessFunction
from base_individual import BaseIndividual
from base_mutation import BaseMutation
from base_selection import BaseSelection


class BaseModel:
    """ Представление алгоритма Голдберга """

    def __init__(
            self,
            # number_of_repetitions: int,
            # generation_size: int,
            # mutation_probability: int,
            # crossover_probability: int,
            # individual_prototype,
            # mutation: BaseMutation,
            # crossover: BaseCrossover,
            # selection: BaseSelection,
            # fitness_function,
    ):
        self.number_of_repetitions = None
        self.generation_size = None
        self.mutation_probability = None
        self.crossover_probability = None
        self.individual_prototype = None
        self.mutation = None
        self.crossover = None
        self.selection = None
        self.fitness_function = None
        self._current_generation: list[BaseIndividual] = []
        self._new_generation: list[BaseIndividual] = []

    def start_genetic_algorithms(self):
        """ Запуск ГА"""

    def prepare_initial_generation(self):
        """ Подготовка начального поколения"""

    def get_best_individual(self):
        """ Получение лучшей приспособленности"""
        res = sorted(self._current_generation, key=self.fitness_function)[0]
        return res

    def get_new_repeat_count(self, repeat_count: int, new_value: Any, last_value: Any):
        """ Получение нового значения счетчика повторений"""
        return repeat_count + 1 if new_value == last_value else 0

    def form_new_generation(self):
        """ Задать новое поколение"""

    def start_crossover(self, parent_1: BaseIndividual, parent_2: BaseIndividual):
        """ Запуск кроссовера"""

    def start_mutation(self, individual: BaseIndividual):
        """ Запуск мутации"""

    def start_selection(self, individuals: list[BaseIndividual]) -> list[BaseIndividual] | BaseIndividual:
        """ Запуск отбора"""


class GeneticaAlgorithmBuilder:
    def __init__(self, genetica_algorithm=None):
        if genetica_algorithm is None:
            self.genetica_algorithm = BaseModel()
        else:
            self.genetica_algorithm = genetica_algorithm

    def build_params(
            self,
            number_of_repetitions,
            generation_size,
            mutation_probability,
            crossover_probability
    ):
        self.genetica_algorithm.number_of_repetitions = number_of_repetitions
        self.genetica_algorithm.generation_size = generation_size
        self.genetica_algorithm.genetica_algorithm.mutation_probability = mutation_probability
        self.genetica_algorithm.genetica_algorithm.crossover_probability = crossover_probability
        return self

    def build_individual(self, individual: BaseIndividual):
        self.genetica_algorithm.individual = individual
        return self

    def build_mutation(self, mutation: BaseMutation):
        self.genetica_algorithm.mutation = mutation
        return self

    def build_crossover(self, crossover: BaseCrossover):
        self.genetica_algorithm.crossover = crossover
        return self

    def build_selection(self, selection: BaseSelection):
        self.genetica_algorithm.selection = selection
        return self

    def build_fitness_function(self, fitness_function: BaseFitnessFunction):
        self.genetica_algorithm.fitness_function = fitness_function
        return self

    def build(self):
        return self.genetica_algorithm
