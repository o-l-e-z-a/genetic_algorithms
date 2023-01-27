import abc
from individuals.base_individual import BaseIndividual


class BaseCrossover(abc.ABC):
    """ Базовое представление кроссовера """

    @abc.abstractmethod
    def get_indices(self, *args, **kwargs):
        """ Получение границ(ы) для кросоввера"""

    @abc.abstractmethod
    def crossover(self, parent_1: BaseIndividual, parent_2: BaseIndividual) -> tuple[list, list]:
        """ Осуществление кроссовера"""
