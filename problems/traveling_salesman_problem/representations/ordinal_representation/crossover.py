from crossovers.base_crossover import BaseCrossover
from individuals.base_individual import BaseIndividual
from services.service import get_random_index


class SinglePointCrossover(BaseCrossover):
    """ Представление одноточечного кроссовера"""

    def get_indices(self, genes_length: int):
        return get_random_index(end=genes_length - 2, start=1)

    def crossover(self, parent_1: BaseIndividual, parent_2: BaseIndividual) -> tuple[list, list]:
        index = self.get_indices(len(parent_1))
        child_1_genes = parent_2.genes[:index] + parent_1.genes[index:]
        child_2_genes = parent_1.genes[:index] + parent_2.genes[index:]
        return child_1_genes, child_2_genes
