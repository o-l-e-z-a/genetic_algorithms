from multiprocessing import Pool

from individuals.base_individual import BaseIndividual
from models.base.base_model import BaseModel


class EliteMixin:
    """ Представление алгоритма Голдберга с элитными особями """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elite_count: int | None = None

    def set_new_generation(self):
        """ Задать новое поколение """
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
        """ Получить элиту """
        elites = []
        fitness = [self.fitness_function(individual) for individual in self._current_generation]
        fitness.sort()
        elites_fitness = fitness[:self.elite_count]
        for index, individual in enumerate(self._current_generation):
            if self.fitness_function(individual) in elites_fitness:
                elites.append((index, individual))
        return elites[:self.elite_count]


class TwoGenerationMixin:
    """ Представление алгоритма Голдберга с вторым поколением """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_generation_model: BaseModel | None = None

    def prepare_initial_generation(self):
        """ Подготовка начального поколения"""
        self._current_generation = [
            self.form_individual_genes_with_genetic_algorithm() for _ in range(self.generation_size)
        ]

    def prepare_initial_generation_multiprocessing(self):
        """ Подготовка начального поколения"""
        pool = Pool()
        function_to_pool = self.form_individual_genes_with_genetic_algorithm
        pool_arguments = [None for i in range(self.generation_size)]
        self._current_generation = list(pool.map(function_to_pool, pool_arguments))
        pool.terminate()

    def form_individual_genes_with_genetic_algorithm(self, _: None = None):
        """ Формирование одной особи с помощью ГА"""
        *_, new_individual = self.first_generation_model.start_genetic_algorithms()
        return new_individual


class TwoGenerationAndEliteMixinMixin(TwoGenerationMixin, EliteMixin):
    """ Модель Голдберга с вторым поколением и элитой"""
