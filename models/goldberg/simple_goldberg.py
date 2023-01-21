from functools import partial

from service import get_random_indices, get_random_index


class Goldberg:
    """ Представление алгоритма Голдберга """

    def __init__(self, number_of_repetitions, generation_size, mutation_probability, crossover_probability, matrix,
                 individual_type, mutation_type, crossover_type, selection_type, fitness_function, individual_params=None):
        self.number_of_repetitions = max(number_of_repetitions, 1)
        self.generation_size = max(generation_size, 2)
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.matrix = matrix
        self.individual_type = individual_type
        self.individual_params = individual_params if individual_params else {}
        self.mutation_type = mutation_type
        self.crossover_type = crossover_type
        self.selection_type = selection_type
        self.fitness_function = partial(fitness_function, self.matrix)
        self._current_generation = []
        self._new_generation = []

    def start_genetic_algorithms(self):
        """ Запуск ГА"""
        self.prepare_initial_generation()
        repeat_count, last_best_value, generation_count = 0, 0, -1
        while repeat_count != self.number_of_repetitions:
            best_individual = self.get_best_individual()
            new_best_value = int(self.fitness_function(best_individual))
            repeat_count = self.get_new_repeat_count(repeat_count, new_best_value, last_best_value)
            self.set_new_generation()
            self._current_generation = self._new_generation[:]
            self._new_generation = []
            generation_count += 1
            last_best_value = new_best_value
        else:
            return generation_count, new_best_value, best_individual

    def prepare_initial_generation(self):
        """ Подготовка начального поколения"""
        for i in range(self.generation_size):
            # прототип
            new_individual = self.individual_type(**self.individual_params, genes_length=len(self.matrix))
            new_individual.set_initial_genes()
            self._current_generation.append(new_individual)

    def get_best_individual(self):
        """ Получение лучшей приспособленности"""
        res = sorted(self._current_generation, key=self.fitness_function)[0]
        return res

    def get_new_repeat_count(self, repeat_count, new_value, last_value):
        """ Получение нового значения счетчика повторений"""
        return repeat_count + 1 if new_value == last_value else 0

    def set_new_generation(self):
        """ Задать новое поколение"""
        for index in range(self.generation_size):
            new_individual = self.get_new_individual(index)
            self._new_generation.append(new_individual)

    def get_new_individual(self, index):
        """ Получить новую особь"""
        random_index = get_random_index(end=99)
        if random_index < self.crossover_probability:
            new_individual = self.form_new_individual(index)
        else:
            new_individual = self._current_generation[index]
        return new_individual

    def form_new_individual(self, index):
        """ Сформировать новую особь"""
        parent_1, parent_2 = self.get_new_parents(index)
        child_1, child_2 = self.start_crossover([parent_1, parent_2])
        self.start_mutation(child_1)
        self.start_mutation(child_2)
        new_individual = self.start_selection([parent_1, child_1, child_2])
        return new_individual

    def get_new_parents(self, index):
        """ Получить новых родителей"""
        index_1, index_2 = get_random_indices(index=index, end=self.generation_size - 1)
        parent_1, parent_2 = self._current_generation[index_1], self._current_generation[index_2]
        return parent_1, parent_2

    def start_crossover(self, individuals):
        """ Запуск кроссовера"""
        crossover = self.crossover_type(individuals)
        child_1_genes, child_2_genes = crossover.crossover()
        child_1 = self.individual_type(**self.individual_params, genes=child_1_genes)
        child_2 = self.individual_type(**self.individual_params, genes=child_2_genes)
        return child_1, child_2

    def start_mutation(self, child):
        """ Запуск мутации"""
        random_index = get_random_index(end=99)
        if random_index < self.mutation_probability:
            mutation_child = self.mutation_type(child)
            mutation_child.mutation()

    def start_selection(self, individuals):
        """ Запуск отбора"""
        selection = self.selection_type(individuals, self.fitness_function)
        res = selection.selection()
        return res
