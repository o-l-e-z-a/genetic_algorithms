import abc


class BaseSelection(abc.ABC):
    """ Базовое представление отбора"""

    def __init__(self, individuals, fitness_function):
        self._individuals = individuals
        self._fitness_function = fitness_function

    @abc.abstractmethod
    def selection(self):
        """ Осуществление отбора"""


class TournamentSelection(BaseSelection):
    """ Турнирный отбор"""

    def selection(self):
        self._individuals.sort(key=self._fitness_function)
        return self._individuals[0]
