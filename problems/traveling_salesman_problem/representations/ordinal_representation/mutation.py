from individuals.base_individual import BaseIndividual

from mitations.base_mutation import BaseMutation

from services.service import get_random_index


class SinglePointOrdinalMutation(BaseMutation):
    """ Одноточечная мутация для порядкового представления """

    def get_indices(self, genes_length: int):
        index = get_random_index(end=genes_length - 1)
        random_value = get_random_index(end=genes_length - index - 1)
        return index, random_value

    def mutation(self, individual: BaseIndividual):
        index, random_value = self.get_indices(len(individual))
        individual[index] = random_value
