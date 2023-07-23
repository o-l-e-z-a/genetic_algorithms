from typing import Type

from crossovers.base_crossover import BaseCrossover

from fitness_functions.base_fitness_function import BaseFitnessFunction

from individuals.base_individual import BaseIndividual, IndividualPrototype

from mitations.base_mutation import BaseMutation

from selections.base_selection import BaseSelection

from models.base.base_model import BaseModel
from models.goldberg.service import check_for_positive_int, check_probability


class GeneticaAlgorithmBuilder:
    def __init__(self, genetica_algorithm: BaseModel | None = None):
        if genetica_algorithm is None:
            self.genetica_algorithm = BaseModel()
        else:
            self.genetica_algorithm = genetica_algorithm

    def create_params(
            self,
            number_of_repetitions: int,
            generation_size: int,
            mutation_probability: int,
            crossover_probability: int,
    ):
        self.genetica_algorithm.number_of_repetitions = check_for_positive_int(number_of_repetitions)
        self.genetica_algorithm.generation_size = check_for_positive_int(generation_size)
        self.genetica_algorithm.mutation_probability = check_probability(mutation_probability)
        self.genetica_algorithm.crossover_probability = check_probability(crossover_probability)
        return self

    def create_individual(self, individual: Type[BaseIndividual], *individual_args, **individual_kwargs):
        self.genetica_algorithm.individual_prototype = IndividualPrototype(
            individual,
            *individual_args,
            **individual_kwargs
        )
        return self

    def create_mutation(
            self,
            mutation: Type[BaseMutation],
            *mutation_args,
            **mutation_kwargs
    ):
        self.genetica_algorithm.mutation = mutation(*mutation_args, **mutation_kwargs)
        return self

    def create_crossover(
            self,
            crossover: Type[BaseCrossover],
            *crossover_args,
            **crossover_kwargs
    ):
        self.genetica_algorithm.crossover = crossover(*crossover_args, **crossover_kwargs)
        return self

    def create_selection(
            self,
            selection: Type[BaseSelection],
            fitness_function: BaseFitnessFunction,
            *selection_args,
            **selection_kwargs
    ):
        selection_kwargs['fitness_function'] = fitness_function
        self.genetica_algorithm.selection = selection(
            *selection_args,
            **selection_kwargs
        )
        return self

    def add_fitness_function(
            self,
            fitness_function: BaseFitnessFunction
    ):
        self.genetica_algorithm.fitness_function = fitness_function
        return self

    def build(self):
        return self.genetica_algorithm


class EliteBuilderMixin:
    def create_elite_count(self, elite_count: int):
        self.genetica_algorithm.elite_count = check_for_positive_int(elite_count)


class GeneticaAlgorithmWithTwoGenerationBuilder:
    def __init__(self):
        self.base_ga_builder = GeneticaAlgorithmBuilder()

    def create_params(
            self,
            number_of_repetitions: int,
            generation_size: int,
            mutation_probability: int,
            crossover_probability: int,
            first_generation_model: BaseModel,
    ):
        self.base_ga_builder.create_params(
            number_of_repetitions,
            generation_size,
            mutation_probability,
            crossover_probability
        )
        self.base_ga_builder.genetica_algorithm.first_generation_model = first_generation_model


class GeneticaAlgorithmWithTwoGenerationAndEliteBuilder(
    GeneticaAlgorithmWithTwoGenerationBuilder,
    GeneticaAlgorithmBuilder
):
    def create_params(self, *args, **kwargs):
        super().create_params(*args, **kwargs)
