from multiprocessing import Pool

from models.goldberg.goldber_with_elite import GoldbergWithElite
from models.goldberg.simple_goldberg import Goldberg


class GoldbergWithTwoGeneration(Goldberg):
    """ Представление алгоритма Голдберга с вторым поколением """

    def __init__(self, first_generation_model, first_generation_params, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_generation_params = first_generation_params
        self.first_generation_model = first_generation_model

    def prepare_initial_generation(self):
        """ Подготовка начального поколения"""
        pool = Pool()
        function_to_pool = self.form_individual_genes_with_GA
        pool_arguments = ['' for i in range(self.generation_size)]
        self._current_generation = list(pool.map(function_to_pool, pool_arguments))
        pool.terminate()


    def form_individual_genes_with_GA(self, _):
        """ Формирование одной особи с помощью ГА"""
        first_generation_model = self.first_generation_model(**self.first_generation_params)
        *_, new_individual = first_generation_model.start_genetic_algorithms()
        return new_individual
