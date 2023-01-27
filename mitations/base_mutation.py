import abc

from individuals.base_individual import BaseIndividual


class BaseMutation(abc.ABC):
    """ Базовое представление мутации """

    def get_indices(self, *args, **kwargs):
        """ Получение точек мутации"""

    @abc.abstractmethod
    def mutation(self, individual: BaseIndividual):
        """ Осуществление мутации """
        self.get_indices()
