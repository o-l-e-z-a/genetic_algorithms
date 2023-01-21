from functools import partial
from multiprocessing import Pool
from pprint import pprint

# from matriсes.books_matrix import var as now_matrix
from matriсes.berlin_52 import now_matrix

from base_selection import TournamentSelection
from base_individual import IndividualWithRandomInitialGenes, IndividualWithFormedInitialGenes
from models.goldberg.goldberg_with_2_generation import GoldbergWithTwoGeneration
from models.goldberg.simple_goldberg import Goldberg

from representations.travel_representation.crossover import OrderedCrossover
from representations.travel_representation.fitness_function import travel_fitness_function
from representations.ordinal_representation.individual import OrdinalIndividualWithRandomInitialGenes
from representations.ordinal_representation.fitness_function import ordinal_fitness_function
from representations.ordinal_representation.mutation import SinglePointOrdinalMutation
from representations.travel_representation.mutation import MutationExchange


def run_GA(R, P, P_MUT, P_CROSS, model=None):
    """ Запуск генетического алгоритма"""
    first_generation_params = dict(
        number_of_repetitions=300,
        generation_size=300,
        mutation_probability=P_MUT,
        crossover_probability=P_CROSS,
        matrix=now_matrix,
        individual_type=IndividualWithFormedInitialGenes,
        mutation_type=MutationExchange,
        crossover_type=OrderedCrossover,
        selection_type=TournamentSelection,
        fitness_function=travel_fitness_function,
        individual_params={'matrix': now_matrix, 'key': '1'}
    )
    # goldberg = Goldberg(
    #     number_of_repetitions=R,
    #     generation_size=P,
    #     mutation_probability=P_MUT,
    #     crossover_probability=P_CROSS,
    #     matrix=now_matrix,
    #     individual_type=IndividualWithFormedInitialGenes,
    #     mutation_type=MutationExchange,
    #     crossover_type=OrderedCrossover,
    #     selection_type=TournamentSelection,
    #     fitness_function=travel_fitness_function,
    #     individual_params={'matrix': now_matrix, 'key': '1'}
    # )

    goldberg = GoldbergWithTwoGeneration(
        first_generation_model=Goldberg,
        first_generation_params=first_generation_params,
        number_of_repetitions=R,
        generation_size=P,
        mutation_probability=P_MUT,
        crossover_probability=P_CROSS,
        matrix=now_matrix,
        individual_type=IndividualWithFormedInitialGenes,
        mutation_type=MutationExchange,
        crossover_type=OrderedCrossover,
        selection_type=TournamentSelection,
        fitness_function=travel_fitness_function,
        individual_params={'matrix': [], 'key': '1'}
    )
    result = goldberg.start_genetic_algorithms()
    return result


def main():
    R = 1000
    P = 1000
    P_CROSS = 100
    P_MUT = 100
    results = []
    for i in range(1):
        res = run_GA(R, P, P_MUT, P_CROSS)
        results.append(res)
        print(res)
    # pool = Pool()
    # func = partial(run_GA, R, P, P_MUT, P_CROSS)
    # pool_lists = ['' for i in range(20)]
    # results = list(pool.map(func, pool_lists))
    # pool.terminate()
    results.sort(key=lambda x: x[1])
    pprint(results)


if __name__ == '__main__':
    main()
