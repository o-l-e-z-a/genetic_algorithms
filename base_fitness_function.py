from typing import Any, Type

from base_individual import BaseIndividual


class BaseFitnessFunction:
    """ """

    def __call__(self, individual: BaseIndividual, *args, **kwargs) -> Any:
        """ вычисление приспособленности индивида"""


class FitnessFunctionFactory:
    @staticmethod
    def create_fitness_function(fitness_function: Type[BaseFitnessFunction], *args, **kwargs):
        return fitness_function(*args, **kwargs)

