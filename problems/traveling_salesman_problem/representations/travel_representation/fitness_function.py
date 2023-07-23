from fitness_functions.base_fitness_function import BaseFitnessFunction

from individuals.base_individual import BaseIndividual


class TravelFitnessFunction(BaseFitnessFunction):
    def __init__(self, matrix):
        self.matrix = matrix

    def __call__(self, individual: BaseIndividual, *args, **kwargs) -> int:
        fitness = 0
        for city_index in range(len(individual) - 1):
            fitness += self.matrix[individual.genes[city_index]][individual.genes[city_index + 1]]
        fitness += self.matrix[individual.genes[city_index + 1]][individual.genes[0]]
        return fitness
