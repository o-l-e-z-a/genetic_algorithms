from crossovers.base_crossover import BaseCrossover
from individuals.base_individual import BaseIndividual
from services.service import get_random_index, get_random_indices


class OrderedCrossover(BaseCrossover):
    """ Представление упорядоченного кроссовера """

    def crossover(self, parent_1: BaseIndividual, parent_2: BaseIndividual) -> tuple[list, list]:
        genes_length = len(parent_1)
        index_1, index_2 = self.get_indices(genes_length)
        child_1_genes = self.get_crossed_genes(parent_1, parent_2, index_1, index_2)
        child_2_genes = self.get_crossed_genes(parent_2, parent_1, index_1, index_2)
        return child_1_genes, child_2_genes

    def get_indices(self, genes_length: int):
        index_1, index_2 = get_random_indices(end=genes_length - 1)
        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        return index_1, index_2

    def get_crossed_genes(
            self,
            parent_1: BaseIndividual,
            parent_2: BaseIndividual,
            index_1: int,
            index_2: int
    ) -> list:
        """ Получение генов ребенка от двух родителей """
        genes_length = len(parent_1)
        result = [0 for i in range(genes_length)]
        result[index_1: index_2] = parent_1.genes[index_1: index_2]
        parent_2_list = parent_2.genes[index_2:] + parent_2.genes[:index_2]
        for gen in parent_1.genes[index_1: index_2]:
            if gen in parent_2_list:
                parent_2_list.pop(parent_2_list.index(gen))
        result[index_2:] = parent_2_list[:genes_length - index_2]
        result[:index_1] = parent_2_list[genes_length - index_2:]
        return result


class ChangesCrossover(BaseCrossover):
    """ Представление изменённого кроссовера """

    def crossover(self, parent_1: BaseIndividual, parent_2: BaseIndividual) -> tuple[list, list]:
        genes_length = len(parent_1)
        index = self.get_indices(genes_length)
        child_1_genes = self.get_crossed_genes(parent_1, parent_2, index)
        child_2_genes = self.get_crossed_genes(parent_2, parent_1, index)
        return child_1_genes, child_2_genes

    def get_indices(self, genes_length: int):
        index = get_random_index(start=1, end=genes_length - 2)
        return index

    def get_crossed_genes(self, parent_1: BaseIndividual, parent_2: BaseIndividual, index: int) -> list:
        """ Получение генов ребенка от двух родителей """
        result = []
        result.extend(parent_1.genes[:index])
        for gen in parent_2.genes[index:]:
            if gen not in result:
                result.append(gen)
        for gen in parent_1.genes[:index]:
            if gen not in result:
                result.append(gen)
        for gen in parent_1.genes[index:]:
            if gen not in result:
                result.append(gen)
        return result
