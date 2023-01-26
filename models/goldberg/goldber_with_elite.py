from base_individual import BaseIndividual
from models.base.base_model import GeneticaAlgorithmBuilder
from models.goldberg.service import check_for_positive_int
from models.goldberg.simple_goldberg import Goldberg


class GoldbergWithElite(Goldberg):
    """ Представление алгоритма Голдберга с элитными особями """

    def __init__(self):
        super().__init__()
        self.elite_count: int | None = None

    def set_new_generation(self):
        """ Задать новое поколение"""
        elites = self.get_elites()
        for elite in elites:
            self._current_generation.pop(elite[0])
            self._current_generation.append(elite[1])
        for index in range(self.generation_size - self.elite_count):
            new_individual = self.get_new_individual(index)
            self._new_generation.append(new_individual)
        for elite in elites:
            self._new_generation.append(elite[1])

    def get_elites(self) -> list[tuple[int, BaseIndividual]]:
        """ Получить элиту"""
        elites = []
        fitness = [self.fitness_function(individual) for individual in self._current_generation]
        fitness.sort()
        elites_fitness = fitness[:self.elite_count]
        for index, individual in enumerate(self._current_generation):
            if self.fitness_function(individual) in elites_fitness:
                elites.append((index, individual))
        return elites[:self.elite_count]


class GeneticaAlgorithmWithEliteBuilder(GeneticaAlgorithmBuilder):
    def create_params(self, elite_count: int, *args, **kwargs):
        super().create_params(*args, **kwargs)
        self.genetica_algorithm.elite_count = check_for_positive_int(elite_count)
