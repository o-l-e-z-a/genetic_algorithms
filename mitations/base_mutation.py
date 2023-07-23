from individuals.base_individual import BaseIndividual


class BaseMutation:
    """ Базовое представление мутации """

    def get_indices(self, *args, **kwargs):
        """ Получение точек мутации"""

    def mutation(self, individual: BaseIndividual):
        """ Осуществление мутации """
