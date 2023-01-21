from base_crossover import BaseCrossover
from service import get_random_index


class SinglePointCrossover(BaseCrossover):
    """ Представление одноточечного кроссовера"""

    def get_indices(self, indices):
        self._index = indices if indices else get_random_index(end=self._genes_length - 2, start=1)

    def crossover(self):
        child_1_genes = self._parent_2.genes[:self._index] + self._parent_1.genes[self._index:]
        child_2_genes = self._parent_1.genes[:self._index] + self._parent_2.genes[self._index:]
        return child_1_genes, child_2_genes
