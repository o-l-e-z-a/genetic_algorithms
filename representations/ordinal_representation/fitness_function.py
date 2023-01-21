from representations.ordinal_representation.ordinal_service import form_order_city_index


def ordinal_fitness_function(matrix, individual):
    """ Вычисление приспособленности"""
    fitness = 0
    order_city_index = form_order_city_index(len(individual))

    travel_representation_genes = []
    for gen in individual.genes:
        el = order_city_index[gen]
        travel_representation_genes.append(el)
        order_city_index.remove(el)

    for city_index in range(len(individual) - 1):
        fitness += matrix[travel_representation_genes[city_index]][travel_representation_genes[city_index + 1]]
    fitness += matrix[travel_representation_genes[city_index + 1]][travel_representation_genes[0]]
    return fitness
