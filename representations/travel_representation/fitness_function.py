def travel_fitness_function(matrix, individual):
    """ Вычисление приспособленности"""
    fitness = 0
    for city_index in range(len(individual) - 1):
        fitness += matrix[individual.genes[city_index]][individual.genes[city_index + 1]]
    fitness += matrix[individual.genes[city_index + 1]][individual.genes[0]]
    return fitness
