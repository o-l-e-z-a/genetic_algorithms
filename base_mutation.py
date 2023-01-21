import abc


class BaseMutation(abc.ABC):
    """ Базовое представление мутации """

    def __init__(self, individual, indices=None):
        self.individual = individual
        self.get_indices(indices)

    @abc.abstractmethod
    def get_indices(self, indices):
        """ Получение точек мутации"""

    @abc.abstractmethod
    def mutation(self):
        """ Осуществление мутации """
