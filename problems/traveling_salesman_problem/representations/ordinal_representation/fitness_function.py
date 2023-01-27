from fitness_functions.base_fitness_function import BaseFitnessFunction
from individuals.base_individual import BaseIndividual
from problems.traveling_salesman_problem.representations.ordinal_representation.ordinal_service import form_order_city_index


class OrdinalFitnessFunction(BaseFitnessFunction):
    def __init__(self, matrix):
        self.matrix = matrix

    def __call__(self, individual: BaseIndividual, *args, **kwargs) -> int:
        fitness = 0
        order_city_index = form_order_city_index(len(individual))

        travel_representation_genes = []
        for gen in individual.genes:
            el = order_city_index[gen]
            travel_representation_genes.append(el)
            order_city_index.remove(el)

        for city_index in range(len(individual) - 1):
            fitness += self.matrix[travel_representation_genes[city_index]][travel_representation_genes[city_index + 1]]
        fitness += self.matrix[travel_representation_genes[city_index + 1]][travel_representation_genes[0]]
        return fitness
