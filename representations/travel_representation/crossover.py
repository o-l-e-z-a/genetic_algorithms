from base_crossover import BaseCrossover
from service import get_random_index, get_random_indices


class OrderedCrossover(BaseCrossover):
    """ Представление упорядоченного кроссовера """

    def crossover(self):
        child_1_genes = self.get_crossed_genes()
        self._parent_1, self._parent_2 = self._parent_2, self._parent_1
        child_2_genes = self.get_crossed_genes()
        return child_1_genes, child_2_genes

    def get_indices(self, indices):
        self._index_1, self._index_2 = indices if indices else get_random_indices(end=self._genes_length - 1)
        if self._index_1 > self._index_2:
            self._index_1, self._index_2 = self._index_2, self._index_1

    def get_crossed_genes(self):
        """ Получение генов ребенка от двух родителей """
        result = [0 for i in range(self._genes_length)]
        result[self._index_1: self._index_2] = self._parent_1.genes[self._index_1: self._index_2]
        parent_2_list = self._parent_2.genes[self._index_2:] + self._parent_2.genes[:self._index_2]
        for gen in self._parent_1.genes[self._index_1: self._index_2]:
            if gen in parent_2_list:
                parent_2_list.pop(parent_2_list.index(gen))
        result[self._index_2:] = parent_2_list[:self._genes_length - self._index_2]
        result[:self._index_1] = parent_2_list[self._genes_length - self._index_2:]
        return result


class ChangesCrossover(BaseCrossover):
    """ Представление изменённого кроссовера """
    def get_indices(self, indices):
        self._index = indices if indices else get_random_index(start=1, end=self._genes_length - 2)

    def crossover(self):
        child_1_genes = self.get_crossed_genes()
        self._parent_1, self._parent_2 = self._parent_2, self._parent_1
        child_2_genes = self.get_crossed_genes()
        return child_1_genes, child_2_genes

    def get_crossed_genes(self):
        """ Получение генов ребенка от двух родителей """
        result = []
        result.extend(self._parent_1.genes[:self._index])
        for gen in self._parent_2.genes[self._index:]:
            if gen not in result:
                result.append(gen)
        for gen in self._parent_1.genes[:self._index]:
            if gen not in result:
                result.append(gen)
        for gen in self._parent_1.genes[self._index:]:
            if gen not in result:
                result.append(gen)
        return result
