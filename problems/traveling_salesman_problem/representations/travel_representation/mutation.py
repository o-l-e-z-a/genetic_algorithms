from individuals.base_individual import BaseIndividual

from mitations.base_mutation import BaseMutation

from services.service import get_random_indices


class MutationExchange(BaseMutation):
    """ Мутация обменом """

    def get_indices(self, genes_length: int):
        index_1, index_2 = get_random_indices(end=genes_length - 1)
        return index_1, index_2

    def mutation(self, individual: BaseIndividual):
        index_1, index_2 = self.get_indices(len(individual))
        individual[index_1], individual[index_2] = individual[index_2], individual[index_1]
