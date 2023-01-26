from typing import Any, Union, Callable, Type

from base_crossover import BaseCrossover
from base_fitness_function import BaseFitnessFunction
from base_individual import BaseIndividual, IndividualPrototype
from base_mutation import BaseMutation
from base_selection import BaseSelection
from models.goldberg.service import check_for_positive_int, check_probability
from service import get_random_index


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
        self.number_of_repetitions: int | None = None
        self.generation_size: int | None = None
        self.mutation_probability: int | None = None
        self.crossover_probability: int | None = None
        self.individual_prototype: IndividualPrototype | None = None
        self.mutation: BaseMutation | None = None
        self.crossover: BaseCrossover | None = None
        self.selection: BaseSelection | None = None
        self.fitness_function: BaseFitnessFunction | None = None
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
        random_index = get_random_index(end=99)
        if random_index < self.mutation_probability:
            self.mutation.mutation(individual)

    def start_selection(self, individuals: list[BaseIndividual]) -> list[BaseIndividual] | BaseIndividual:
        """ Запуск отбора"""


class GeneticaAlgorithmBuilder:
    def __init__(self, genetica_algorithm: BaseModel | None = None):
        if genetica_algorithm is None:
            self.genetica_algorithm = BaseModel()
        else:
            self.genetica_algorithm = genetica_algorithm

    def create_params(
            self,
            number_of_repetitions: int,
            generation_size: int,
            mutation_probability: int,
            crossover_probability: int
    ):
        self.genetica_algorithm.number_of_repetitions = check_for_positive_int(number_of_repetitions)
        self.genetica_algorithm.generation_size = check_for_positive_int(generation_size)
        self.genetica_algorithm.mutation_probability = check_probability(mutation_probability)
        self.genetica_algorithm.crossover_probability = check_probability(crossover_probability)
        return self

    def create_individual(self, individual: Type[BaseIndividual], *individual_args, **individual_kwargs):
        self.genetica_algorithm.individual_prototype = IndividualPrototype(
            individual,
            *individual_args,
            **individual_kwargs
        )
        return self

    def create_mutation(
            self,
            mutation: Type[BaseMutation],
            *mutation_args,
            **mutation_kwargs
    ):
        self.genetica_algorithm.mutation = mutation(*mutation_args, **mutation_kwargs)
        return self

    def create_crossover(
            self,
            crossover: Type[BaseCrossover],
            *crossover_args,
            **crossover_kwargs
    ):
        self.genetica_algorithm.crossover = crossover(*crossover_args, **crossover_kwargs)
        return self

    def create_selection(
            self,
            selection: Type[BaseSelection],
            fitness_function: BaseFitnessFunction,
            *selection_args,
            **selection_kwargs
    ):
        self.genetica_algorithm.selection = selection(
            fitness_function=fitness_function,
            *selection_args,
            **selection_kwargs)
        return self

    def add_fitness_function(
            self,
            fitness_function: BaseFitnessFunction
    ):
        self.genetica_algorithm.fitness_function = fitness_function
        return self

    def build(self):
        return self.genetica_algorithm
