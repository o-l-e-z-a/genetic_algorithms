from multiprocessing import Pool

from models.base.base_model import BaseModel, GeneticaAlgorithmBuilder
from models.goldberg.goldber_with_elite import GoldbergWithElite
from models.goldberg.simple_goldberg import Goldberg


class GoldbergWithTwoGeneration(Goldberg):
    """ Представление алгоритма Голдберга с вторым поколением """

    def __init__(self):
        super().__init__()
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


class GoldbergWithTwoGenerationAndElite(GoldbergWithTwoGeneration, GoldbergWithElite):
    """ Модель Голдберга с вторым поколением и элитой"""


class GeneticaAlgorithmWithTwoGenerationBuilder(GeneticaAlgorithmBuilder):
    def create_params(self, first_generation_model: BaseModel, *args, **kwargs):
        super().create_params(*args, **kwargs)
        self.genetica_algorithm.first_generation_model = first_generation_model


class GeneticaAlgorithmWithTwoGenerationAndEliteBuilder(
    GeneticaAlgorithmWithTwoGenerationBuilder,
    GeneticaAlgorithmBuilder
):
    def create_params(self, *args, **kwargs):
        super().create_params(*args, **kwargs)
