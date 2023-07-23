import random

from individuals.base_individual import IndividualWithRandomInitialGenes, IndividualWithFormedInitialGenes

from problems.traveling_salesman_problem.representations.ordinal_representation.ordinal_service import (
    form_order_city_index,
)


class OrdinalIndividualWithRandomInitialGenes(IndividualWithRandomInitialGenes):
    """ Особь порядкового представления со случайными начальными генами """

    def set_initial_genes(self):
        order_city_index = form_order_city_index(len(self))
        for i in range(len(self)):
            random_choice = random.choice(order_city_index)
            random_index = order_city_index.index(random_choice)
            self._genes[i] = random_index
            order_city_index.pop(random_index)


class OrdinalIndividualWithFormedInitialGenes(IndividualWithFormedInitialGenes):
    """ Особь порядкового представления с начальными генами, сформированными с помощью жадных эвристик"""

    def set_initial_genes(self):
        super().set_initial_genes()
        order_city_index = form_order_city_index(len(self))
        genes = self.genes[:]
        for i in range(len(self)):
            order_index = order_city_index.index(genes.pop(0))
            self._genes[i] = order_index
            order_city_index.pop(order_index)
