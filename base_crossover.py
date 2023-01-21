import abc


class BaseCrossover(abc.ABC):
    """ Базовое представление кроссовера """

    def __init__(self, individuals, indices=None):
        self._parent_1, self._parent_2 = individuals
        self._genes_length = len(self._parent_1)
        self.get_indices(indices)

    @abc.abstractmethod
    def get_indices(self, indices):
        """ Получение границ(ы) для кросоввера"""

    @abc.abstractmethod
    def crossover(self, individuals):
        """ Осуществление кроссовера"""
