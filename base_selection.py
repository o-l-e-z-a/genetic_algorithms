import abc

from base_individual import BaseIndividual


class BaseSelection(abc.ABC):
    """
    Базовое представление отбора
    """

    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    @abc.abstractmethod
    def selection(
            self,
            individuals: list[BaseIndividual],
            individual_count: int = 1
    ) -> list[BaseIndividual] | BaseIndividual:
        """ Осуществление отбора. Выбирает некоторое количество (часто 1) особей и возвращает их"""


class TournamentSelection(BaseSelection):
    """
    Турнирный отбор
    """

    def selection(
            self,
            individuals: list[BaseIndividual],
            individual_count: int = 1
    ) -> list[BaseIndividual]:
        return sorted(individuals, key=self.fitness_function)[:individual_count]
