from individuals.base_individual import BaseIndividual
from models.base.base_model import BaseModel
from services.service import get_random_indices, get_random_index


class Goldberg(BaseModel):
    """ Представление алгоритма Голдберга """

    def start_genetic_algorithms(self):
        """ Запуск ГА"""
        self.prepare_initial_generation()
        repeat_count, last_best_value, generation_count = 0, 0, -1
        while repeat_count != self.number_of_repetitions:
            best_individual = self.get_best_individual()
            new_best_value = self.fitness_function(best_individual)
            repeat_count = self.get_new_repeat_count(repeat_count, new_best_value, last_best_value)
            self.form_new_generation()
            self._current_generation = self._new_generation[:]
            self._new_generation = []
            generation_count += 1
            last_best_value = new_best_value
        else:
            return generation_count, new_best_value, best_individual

    def prepare_initial_generation(self):
        """ Подготовка начального поколения"""
        for i in range(self.generation_size):
            new_individual = self.individual_prototype.get_new_individual()
            new_individual.set_initial_genes()
            self._current_generation.append(new_individual)

    def form_new_generation(self):
        """ Задать новое поколение"""
        for index in range(self.generation_size):
            new_individual = self.get_new_individual(index)
            self._new_generation.append(new_individual)

    def get_new_individual(self, index: int) -> BaseIndividual:
        """ Получить новую особь"""
        random_index = get_random_index(end=99)
        if random_index < self.crossover_probability:
            new_individual = self.form_new_individual(index)
        else:
            new_individual = self._current_generation[index]
        return new_individual

    def form_new_individual(self, index: int) -> BaseIndividual:
        """ Сформировать новую особь"""
        parent_1, parent_2 = self.get_new_parents(index)
        child_1, child_2 = self.start_crossover([parent_1, parent_2])
        self.start_mutation(child_1)
        self.start_mutation(child_2)
        new_individual = self.start_selection([parent_1, child_1, child_2])
        return new_individual

    def get_new_parents(self, index: int) -> tuple[BaseIndividual, BaseIndividual]:
        """ Получить новых родителей"""
        index_1, index_2 = get_random_indices(index=index, end=self.generation_size - 1)
        parent_1, parent_2 = self._current_generation[index_1], self._current_generation[index_2]
        return parent_1, parent_2

    def start_crossover(
            self,
            parent_1: BaseIndividual,
            parent_2: BaseIndividual
    ) -> tuple[BaseIndividual, BaseIndividual]:
        """ Запуск кроссовера"""
        child_1_genes, child_2_genes = self.crossover.crossover(parent_1, parent_2)
        child_1 = self.individual_prototype.get_new_individual()
        child_1.set_genes(child_1_genes)
        child_2 = self.individual_prototype.get_new_individual()
        child_2.set_genes(child_2_genes)
        return child_1, child_2

    def start_selection(self, individuals: list[BaseIndividual]) -> BaseIndividual:
        """ Запуск отбора"""
        [result] = self.selection.selection(individuals, individual_count=1)
        return result
