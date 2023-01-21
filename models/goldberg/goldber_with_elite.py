from models.goldberg.simple_goldberg import Goldberg


class GoldbergWithElite(Goldberg):
    """ Представление алгоритма Голдберга с элитными особями """
    def __init__(self, elite_count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elite_count = elite_count

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

    def get_elites(self):
        """ Получить элиту"""
        elites = []
        fitness = [self.fitness_function(individual) for individual in self._current_generation]
        fitness.sort()
        elites_fitness = fitness[:self.elite_count]
        for index, individual in enumerate(self._current_generation):
            if self.fitness_function(individual) in elites_fitness:
                elites.append((index, individual))
        return elites[:self.elite_count]
