from typing import Any

from crossovers.base_crossover import BaseCrossover

from fitness_functions.base_fitness_function import BaseFitnessFunction

from individuals.base_individual import BaseIndividual, IndividualPrototype

from mitations.base_mutation import BaseMutation

from selections.base_selection import BaseSelection

from services.service import get_random_index


class BaseModel:
    """ Представление алгоритма Голдберга """

    def __init__(self) -> None:
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
