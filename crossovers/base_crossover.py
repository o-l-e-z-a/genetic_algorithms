from individuals.base_individual import BaseIndividual


class BaseCrossover:
    """ Базовое представление кроссовера """

    def get_indices(self, *args, **kwargs):
        """ Получение границ(ы) для кросоввера"""

    def crossover(self, parent_1: BaseIndividual, parent_2: BaseIndividual) -> tuple[list, list]:
        """ Осуществление кроссовера"""
